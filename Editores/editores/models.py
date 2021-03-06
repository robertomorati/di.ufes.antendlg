# -*- coding: utf-8 -*-
'''
Created on 16/09/2013

Modelo para o ambiente AutEnvLDG

Class with  com the nomenclature nameOfClassAtiva represent the state of the game.

Normal nomenclature for classes is: nameOfClass, for example InstanceObject

@author: Roberto Guimaraes Morati Junior
'''

from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import User 
from django.utils.translation import gettext as _
from core.choices_models import TIPO_SUGESTAO,AVENTURA_CONSTRUCAO
#from imagekit.models import ImageSpecField


class MySQLBooleanField(models.BooleanField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if isinstance(value, bool):
            return value
        return bytearray(value)[0]

    def get_db_prep_value(self, value):
        return '\x01' if value else '\x00'

'''
Class TipoObjeto 

Representa o tipo de um objeto, ou seja, o autor da aventura ao criar um objeto irá relacionar este objeto a um tipo.
Por exemplo, o objeto Cascumpus é do tipo de objeto Monstro.

@param tipo: representa o nome do tipo de objeto
@param descricao: descrição do tipo de objeto
@param posicoes_geograficas: remete a quantidade de posições geográficas que a instância de um objeto de um dado tipo poderá assumir. 
                             Por exemplo, objeto do tipo Limite do Labirinto, esse objeto pode assumir 4 posições geográficas. 
                             Assim delimitando a área do geografica do jogo, por meio de uma sugestão.
@param publico: quando True, esse atributo referece a possibilidade do Tipo de Objeto criado pelo autor ser visivel para outras aventuras.
'''
class TipoObjeto(models.Model):
    tipo = models.CharField(max_length=30)
    descricao = models.CharField(max_length=100)
    posicoes_geograficas = models.IntegerField(max_length=3,default=1, help_text=u"Delimita a quantidade de posições geográficas da instância do objeto.")
    publico = models.BooleanField(default=True) 
    
    #return o tipo
    def __unicode__(self):
        return u'%s' % (self.tipo)
    
    # return o bool do dialogo
    def get_attribute_dialogo(self):
        return u'%d'%(self.dialogo)
    
    #verifica se o tipo de objeto não possui objetos do seu tipo
    def delete(self):
        if not self.objetos.all():
            return super(TipoObjeto, self).delete()
        raise ValidationError(u"Não é possível remover este tipo de objeto pois existem objetos relacionados à ele!")
    

'''
Icone é uma imagem que representa o objeto durante o momento de autoria.
Em outras palavras, quanto o objeto é arrastado para o mapa, a imagem do icone é copiada para o marcador do google maps.

@param nome: é o nome da imagem de autoria.
@param icone: é o diretorio para imagem do icone

Pendências: Redimensionar o icone para tamanho padrão.
'''
class Icone (models.Model):
    nome =  models.CharField(max_length=30,)
    icone = models.ImageField(upload_to ='imagens/icones/', help_text="Ícone do Objeto", blank=True,)
    
    #retorna o icone (dir)
    def __unicode__(self):
        return u'%s' % (self.icone)
        #return u'<img class="avatar" src="%s" alt="avatar">' % (self.icone)

    def get_nome_icone(self):
        return u'%s' % (self.nome)
    
    #verifica se ícone nao esta sendo utilizado por algum objeto
    def delete(self, *args, **kwargs):
        if not self.icones.all():
            storage, path = self.icone.storage, self.icone.path
            super(Icone, self).delete(*args, **kwargs)
            return storage.delete(path)
        raise ValidationError(u"Não é possível remover este ícone pois existem objetos relacionados à ele!")
    
    #deleta imagem antiga
    def save(self, *args, **kwargs):
        try:
            this = Icone.objects.get(id=self.id)
            if this.icone != self.icone:
                this.icone.delete(save=False)
        except: pass # when new photo then we do nothing, normal case          
        super(Icone, self).save(*args, **kwargs)

    
'''
Sugestao é um elemente de percepção para a instância do objeto. 
A sugestão indica para o jogador que o mesmo está próximo de um perigo. 
Por exemplo, a proximidade com o Cascumpus pode ser indicada por um áudio de rugido.

@param tipo: a sugestão pode ser de três tipos: áudio, como um rugido do Cascumpus; imagem: fumaça do fogo; e texto, uma mensagem.
@param sugestao: url da sugestão.
@param proximidade: é a distância que o jogador tem que estar da sugestão para que ele tenha percepção da mesma.   

Pendências nessa classe: Identificar tipos de arquivos e atualizar a forma de criar sugestões.
'''
class Sugestao(models.Model):
    nome = models.CharField(max_length=30,default="", )
    tipo = models.CharField(max_length=10, choices=TIPO_SUGESTAO, default=u'STX', )
    sugestao = models.FileField(upload_to ='sugestao/', help_text="Sugestão para tomada de decisão.",default="", )
    proximidade = models.IntegerField(max_length=3,default=1)
    publico = models.BooleanField(default=True,)
    
    def __unicode__(self):
        return u'%s' % (self.nome) 
   
    #verifica se sugestao nao esta sendo utilizado por alguma instancia
    def delete(self, *args, **kwargs):
        if not self.sugestoes.all():
            storage, path = self.sugestao.storage, self.sugestao.path
            super(Sugestao, self).delete(*args, **kwargs)
            return storage.delete(path)
        raise ValidationError(u"Não é possível remover esta sugestão pois existem instâncias de objetos que fazem uso da mesma!")
    
    #deleta o arquivo antigo
    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Sugestao.objects.get(id=self.id)
            if this.sugestao != self.sugestao:
                this.sugestao.delete(save=False)
        except: pass # when new photo then we do nothing, normal case          
        super(Sugestao, self).save(*args, **kwargs)
        
'''
Sugestão de Arquivos


class SugestaoFile(Sugestao, models.Model):
    sugestao = models.FileField(upload_to ='sugestao/', help_text="Sugestão para tomada de decisão.",default="", )
    descricao = models.CharField(max_length=100)
    
    #verifica se sugestao nao esta sendo utilizado por alguma instancia
    def delete(self, *args, **kwargs):
        if not self.sugestoes.all():
            storage, path = self.sugestao.storage, self.sugestao.path
            super(SugestaoFile, self).delete(*args, **kwargs)
            return storage.delete(path)
        raise ValidationError(u"Não é possível remover esta sugestão pois existem instâncias de objetos que fazem uso da mesma!")
    
    #deleta o arquivo antigo
    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = SugestaoFile.objects.get(id=self.id)
            if this.sugestao != self.sugestao:
                this.sugestao.delete(save=False)
        except: pass # when new photo then we do nothing, normal case          
        super(SugestaoFile, self).save(*args, **kwargs)

'''
'''
Sugestão do Tipo Texto

class SugestaoMensagem(Sugestao,models.Model):
    mensagem = models.CharField(max_length=250)
'''   
    
'''
Objeto tem um tipo de objeto. O objeto representa algo como, placa, fruta, perigo ou personagens que são instânciados na aventura.

@param nome: nome do objeto criado
@param descricao: descrição do objeto.
@param quantidade: quantida de instânciados que pode ter do respectivo objeto no mapa.
@param coletavel: informa se o objeto pode ser coletado na aventura pelo jogador.
@param tipo_objeto: informa o tipo de objeto ao qual o objeto está vinculado
@param incone_objeto: representa a imagem do objeto no momento de autoria    
@param dialogo: representa possibilidade daquele objeto ter ou não um diálogo. 
    
Pendências: Adicionar propriedade publico/privado.
'''
class Objeto (models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.CharField(max_length=100)
    quantidade = models.IntegerField(max_length=100,default=1)
    coletavel = models.BooleanField(default=False, help_text=u"Informa se o objeto pode ser coletado durante a aventura.")
    tipo_objeto = models.ForeignKey(TipoObjeto, related_name="objetos",)
    icone_objeto = models.ForeignKey(Icone, related_name="icones", default="", )
    dialogo = models.BooleanField(default=True, help_text=u"Delimita se a instancia de um objeto pode ter um dialogo.")
    #publico = models.BooleanField(default=True, help_text=u"Delimita se esse objeto será publico para outras aventuras.")
    
    #img = models.ImageField(upload_to='../media/imagens/',verbose_name="Imagem Autoria")
    
    def _unicode_(self):
        return u'%s' % (self.nome)
    
    def get_nome_objeto(self):
        return u'%s' % (self.nome)

  
'''
Autor - é o individuo que cria a aventura.
O autor herda User do Django.

@param dica_senha: dica de senha
@param nickname: apelido do autor
@param icone_autor: imagem do usuario para cadastro   
'''
class Autor(User, models.Model):
    #username = models.OneToOneField(User, related_name="autor",)
    dica_senha = models.CharField(max_length=200, verbose_name="Dica de Senha",default="",blank=True,)
    nickname = models.CharField(max_length=100, verbose_name="Nickname",default="",blank=True,)
    icone_autor = models.ImageField(upload_to ='avatar_autor/', help_text="Avatar do autor.", default="", blank=True,)
    
    #retorna o dir do autor
    def __unicode__(self):
        return u'%s' % (self.icone_autor)


'''
Aventura - representa um jogo criado. Por exemplo, o ALDloc II é uma aventura baseada na concepção do ALD em 3D.

@param nome: nome da aventura
@param descricao: o que é aa aventura?
@param inicio: data de inicio da aventura
@param fim: data de fim da aventura
@param latitude:
@param longitude: 
       localidade da aventura
@param autor: autor da aventura 
'''
class Aventura(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome da aventura",)
    descricao =  models.CharField(max_length=200, verbose_name="Descrição da aventura",)
    inicio = models.DateField(_("Data Inicio"), default=date.today)
    fim = models.DateField(_("Data Fim"), default=date.today,)
    latitude = models.FloatField(blank=True,default=0.0)
    longitude = models.FloatField(blank=True,default=0.0)
    autor = models.ForeignKey(User, related_name="Autor",default="", blank=True,)
    autoria_estado = models.CharField(max_length=10, choices=AVENTURA_CONSTRUCAO, default=u'AI', )
    #autores = models.ManyToManyField(Autor, related_name="autores_aventura",)
    
    def __unicode__(self):
        return u'%s' % (self.nome)
    
    
'''
TipoImagem representa o tipo de imagem para a instância de objeto.
           a imagem pode ser 2D ou 3D. 
           2D - uso do google maps para jogar
           3D - uso da camera do dispositivo móvel.
           
@param tipo: tipo de imnagem cadastrada
@param img: url da imagem 
'''
class TipoImagem(models.Model):
    IMG_MAP = 'IM'
    IMG_CAM = 'IC' 
    TIPO_IMAGEMS = (
        (IMG_MAP, 'Imagem Google Maps'),
        (IMG_CAM, 'Imagem Câmera'),)
    nome_img = models.CharField(max_length=30,  verbose_name="Nome da Imagem",default="",)
    tipo = models.CharField( max_length=10, choices=TIPO_IMAGEMS ,default=IMG_MAP)
    img_play = models.FileField(_("Imagem"),  upload_to ='imagens/img_play/',null=True, blank=True)
    descricao = models.CharField( max_length=100, default="", )
    
    def __unicode__(self):
        return u'%s' % (self.nome_img)
    
    def get_nome_tipo_imagem(self):
        return u'%s' % (self.nome_img)
    
    #verifica se sugestao nao esta sendo utilizado por alguma instancia
    def delete(self, *args, **kwargs): 
        if self.tipo == 'IM':
            if not self.imagem_mapa.all():#two times
                storage, path = self.img_play.storage, self.img_play.path
                super(TipoImagem, self).delete(*args, **kwargs)
                return storage.delete(path)
        elif self.tipo == 'IC':
            if not self.imagem_camera.all():#two times
                storage, path = self.img_play.storage, self.img_play.path
                super(TipoImagem, self).delete(*args, **kwargs)
                return storage.delete(path)
        raise ValidationError(u"Não é possível remover está imagem pois existem instâncias de objetos que fazem uso da mesma!")
    
    #deleta o arquivo antigo
    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = TipoImagem.objects.get(id=self.id)
            if this.img_play != self.img_play:
                this.img_play.delete(save=False)
        except: pass # when new photo then we do nothing, normal case          
        super(TipoImagem, self).save(*args, **kwargs)   
    
 


'''
InstanciaObjeto representa um objeto que é arrastado para o mapa da aventura.

@param nome:nome da instancia do objeto
@param proximidade: distância que o jogador deve estar do objeto para que possa ver o mesmo
@param visivel: este atributo permite indicar se determinado objeto deve estar visivel na aventura, para o jogador.
@param encenacao: indica se o objeto pode ser controlado por outro jogador ou por um agente.
@param posicao_geografica: relacao da instancia com a sua posicao geografica. 
       Como já visto em TipoObjeto, uma instância pode ter mais de uma POS, assim, mudando o tipo de marcador.
@param sugestao: descrito anteriormente.

Pendencias Finalizadas: Rever o atributo sugestão; Adicionar relação com a aventura;
'''
class InstanciaObjeto(models.Model):
    DESABILITADO = 'DS'
    AVATAR = 'AV'
    AGENTE = 'AG' 
    TIPO_ENCENACAO = (
        (DESABILITADO, 'Desabilitado'),
        (AVATAR, 'Avatar'),
        (AGENTE, 'Agente'),)
    nome = models.CharField(max_length=30)
    proximidade = models.IntegerField(max_length=3,default=1)
    visivel = models.BooleanField(default=True, help_text=u"Informa se o objeto está visivel na aventura.")
    encenacao = models.CharField(max_length=14, choices=TIPO_ENCENACAO ,blank=True,default=DESABILITADO,help_text=u"Indica o tipo de encenação que é possível com a instância do objeto.")
    objeto = models.ForeignKey(Objeto, related_name="instancias_objeto",blank=True,default="",)
    sugestao_objeto = models.ForeignKey(Sugestao, related_name="sugestoes", blank=True, default="", null=True, )
    aventura = models.ForeignKey(Aventura, related_name="aventura_inst_obj", blank=True, default="", null=True,)
    dialogo = models.TextField('dialogo', blank=True)
    imagem_mapa = models.ForeignKey(TipoImagem,related_name="tipo_imagem_mapa", blank=True, default="", null=True, )
    imagem_camera = models.ForeignKey(TipoImagem,related_name="tipo_imagem_camera", blank=True, default="", null=True, )
    
    #dialogo = models.ForeignKey(Dialogo, related_name="dialogo",blank=True,)
    #posicao_geografica_ = models.ManyToManyField(PosicaoGeografica, related_name="pos_geo_inst_objeto",) 
    #pos possui a instnacia do objeto, pois dependendo do tipo de objeto, esse poderá ter n POS
    #sugestao_objeto =  models.ForeignKey(Sugestao, related_name="sugestao_instancia_objeto", )
    
    def __unicode__(self):
        return u'%s' % (self.nome)
    
    def get_nome_instancia(self):
        return u'%s' % (self.nome)

'''
Posições Geográficas para instâncias de objetos.
@param latitude
@param  longitude
@param altitude: para objetos em 3D apresentados por meio da camera do dispositivo move, como por exemplo com o uso do Wikitude.
@param instancia_objeto: representa a relação com a instancia que possui esta posicao. 
'''
class PosicaoGeografica(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    instancia_objeto = models.ForeignKey(InstanciaObjeto, related_name="pos_inst_objeto",blank=True,default="",)
    #instancia_objeto = models.ManyToManyField(InstanciaObjeto, related_name="pos_inst_objeto",blank=True,) 

    
    def get_nome_instancia(self,posn):
        nomepos = "POS " + str(posn)
        return u'%s' % (nomepos)


'''
Jogador - representar um jogador cadastrado com seu dispositivo movel

@param dica_senha: dica de senha
@param nickname:   
'''
class Jogador( models.Model):
    dica_senha = models.CharField(max_length=200, verbose_name="Dica de Senha",default="",blank=True,)
    nickname = models.CharField(max_length=100, verbose_name="Nickname",default="",blank=True,)
    distancia = models.IntegerField(max_length=10,default=500,)
    icone_jogador = models.ImageField(upload_to ='avatar_jogador/', help_text="Avatar do jogador.", default="", blank=True,)
    
    def __unicode__(self):
        return u'%s' % (self.nickname)
    
        

'''
class AventuraAtiva - representa um aventura que está ativa, ou seja, uma aventura que poderá ser jogada.

@param aventura: representa a aventura que foi ativada. 
@param publica: se esse atributo for False, significa que o jogador irá precisar da chave de acesso.
@param joadores_aventura_ativa: jogadores vinculados a aventura ativa
@param chave_acesso: chave para acessar uma aventura com publico como False
'''
class AventuraAtiva(models.Model):
    instancia = models.IntegerField(max_length=2,default=1,)
    aventura = models.ForeignKey(Aventura, related_name="aventura", blank=True, default="", null=True, )
    publica = models.BooleanField(default=True, help_text=u"Informa se a aventura ativa é de livre acesso.")
    joadores_aventura_ativa =  models.ManyToManyField(Jogador, related_name="jogadores_aventura_ativa", blank=True, default="", null=True, )
    chave_acesso = models.CharField(max_length=10,default="",blank=True,)#XPTO2014

    #inicio = models.DateField(_("Data Inicio"), default=date.today)
    #fim = models.DateField(_("Data Fim"), default=date.today,)
    #latitude = models.FloatField(blank=True,default=0.0)
    #longitude = models.FloatField(blank=True,default=0.0)
    #jogador = models.ForeignKey(User, related_name="Jogador",default="", blank=True,)


'''
PosInstanciaAtiva - representa instâncias de aventuras que estão ativas, ou seja, aventuras sendo jogadas. 

@param    latitude,longitude e altitude: inicialmente possui as posiçòes de uma aventura criada. São alteradas no decorrer do jogo.
@param    instancia_objeto_ativa: referência a uma instância de objeto
@param    aventura_ativa_instacia: referência a  aventura ativa
'''
class PosInstanciaAtiva(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    instancia_objeto_ativa = models.ForeignKey(InstanciaObjeto, related_name="instancia_objeto_ativa",blank=True,default="",)
    aventura_ativa_instancia = models.ForeignKey(AventuraAtiva, related_name="aventura_ativa_instancia",blank=True,default="",)
     
'''
Avatar - representa os persongens criados para uma determinada aventura.
'''  
class Avatar(models.Model):
    nome = models.CharField(max_length=30)
    #latitude = models.FloatField(default="0",)
    #longitude = models.FloatField(default="0",)
    avatar = models.ImageField(upload_to ='imagens/avatares_jogadores/', help_text="Avatar", blank=True,)
    publico = models.BooleanField(default=False, help_text=u"Informa se o avatar pode ser utilizado em outras aventuras.")
    #aventureiro = models.ForeignKey(Autor, related_name="aventureiro",blank=True,default="",) #autor
    aventureiro = models.ForeignKey(Jogador, related_name="aventureiro",blank=True,default="",null=True,)
    aventura_avatar = models.ForeignKey(Aventura, related_name="aventura_avatar",blank=True,default="",null=True,)
    inst_objeto = models.ForeignKey(InstanciaObjeto, related_name="inst_objeto",null=True,blank=True,default=None,)#caso seja possivel o avatar controlar alguma isntância de objeto
    
    
    #retorna o icone (dir)
    def __unicode__(self):
        return u'%s' % (self.avatar)
        #return u'<img class="avatar" src="%s" alt="avatar">' % (self.icone)

    def get_nome_avatar(self):
        return u'%s' % (self.nome)
    
    #verifica se um avatar está ou não sendo utilizado em alguma condição. 
    def delete(self, *args, **kwargs):
        if not self.prefixo_cj_avateres.all():
            storage, path = self.avatar.storage, self.avatar.path
            super(Avatar, self).delete(*args, **kwargs)
            return storage.delete(path)
        if not self.prefixo_cd_avateres.all():
            storage, path = self.avatar.storage, self.avatar.path
            super(Avatar, self).delete(*args, **kwargs)
            return storage.delete(path)
        raise ValidationError(u"Não é possível remover este avatar pois existem  condições que fazem uso do mesmo!")
    
    #deleta imagem antiga
    def save(self, *args, **kwargs):
        try:
            this = Avatar.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except: pass # when new photo then we do nothing, normal case          
        super(Avatar, self).save(*args, **kwargs)

'''
class AvatarAtivo  -  persistencia dos dados de um avatar ativo

@param latitude, longitude - guarda a posição ao qual o jogado parou na aventura
'''
class AvatarAtivo(models.Model):
    aventura_ativa_avatar = models.ForeignKey(AventuraAtiva, related_name="aventura_ativa_avatar",null=True,blank=True,default=None,)
    latitude = models.FloatField(default="0",)
    longitude = models.FloatField(default="0",)
    avatar = models.ForeignKey(Avatar, related_name="avatar_ativo",null=True,blank=True,default=None,)
    
'''
Enredo - elemento apresentado ao jogador quando o mesmo toma uma decisão.

@param nome: nome do enredo
@param tipo: tipo do enredo
@param enredo: elemento que representa o enredo
@param descricao: qual a finalidade do enredo na aventura    
'''
class Enredo(models.Model):
    #TEXTO = 'STX'
    #AUDIO = 'SAU'
    #IMGC = 'IMGC' 
    #IMGM = 'IMGM' 
    #TIPO_SUGESTAO = (
    #    (TEXTO, 'Texto'),
    #    (AUDIO, 'Áudio'),
    #    (IMGC, 'Imagem Câmera'),
    #    (IMGM, 'Imagem Mapa'),)
    nome = models.CharField(max_length=30,default="", )
    #tipo = models.CharField(max_length=10, choices=TIPO_SUGESTAO ,default=TEXTO)
    #enredo = models.FileField(upload_to ='enredo/', help_text="Elemente que auxilia na contextualição da tomada de decisão..",default="", )
    descricao = models.CharField(max_length=200, default="")
    aventura = models.ForeignKey(Aventura,verbose_name="Aventura",related_name="aventura_enredo", blank=True, default="", null=True, )
    
    #verifica se o enredo esta sendo utilizado por Condições Missão
    def delete(self, *args, **kwargs): 
        
        #recupera id
        id_enredo = self.id
        
        object = EnredoFile.objects.all().filter(enredo_ptr_id=id_enredo)
        
        buffer = ''
        for obj in object:
            buffer = obj 
        
        if isinstance(buffer, EnredoFile):
            if not self.enredos.all():#two times
                storage, path = buffer.enredo_file.storage, buffer.enredo_file.path
                super(Enredo, buffer).delete(*args, **kwargs)
                return storage.delete(path)
            raise ValidationError(u"Não é possível remover este enredo, pois o mesmo está sendo utilizado!")
        
        if not self.enredos.all():#two times
            return super(Enredo, self).delete(*args, **kwargs)
        raise ValidationError(u"Não é possível remover este enredo, pois o mesmo está sendo utilizado!")
    
    def __unicode__(self):
        return u'%s' % (self.nome)
    
    def get_nome_enredo(self):
        return u'%s' % (self.nome)
 


#Classes a serem adicionadas
'''
class EnredoFile - representa uma imagem ou áudio
'''
class EnredoFile(Enredo, models.Model):
    AUDIO = 'SAU'
    IMGC = 'IMGC' 
    IMGM = 'IMGM' 
    TIPO_SUGESTAO = (
        (AUDIO, 'Áudio'),
        (IMGC, 'Imagem Câmera'),
        (IMGM, 'Imagem Mapa'),)
    tipo = models.CharField(max_length=10, choices=TIPO_SUGESTAO ,default=AUDIO)
    enredo_file = models.FileField(upload_to ='enredo/', help_text="Elemente que auxilia na contextualição da tomada de decisão..",default="", ) 

    
    #deleta o arquivo antigo
    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = EnredoFile.objects.get(id=self.id)
            if this.enredo_file != self.enredo_file:
                this.enredo_file.delete(save=False)
        except: pass # when new photo then we do nothing, normal case          
        super(EnredoFile, self).save(*args, **kwargs)  

'''
class EnredoInstancia - Uma instancia como enredo
'''
class EnredoInstancia(Enredo, models.Model):
    enredo_instancia = models.ForeignKey(InstanciaObjeto, related_name="enredo_instancia",blank=True,default="",)

'''
class class EnredoMensagem - uma mensagem como enredo
'''    
class EnredoMensagem(Enredo,models.Model):
    enredo_mensagem = models.CharField(max_length=200, default="")


'''
CondicoesMissao - representa uma composicao de condicoes para uma missao

@paran nomeComposica: nome da composicao de condicoes
@param missao: relacao com a missao 

'''
#class CondicoesMissao(models.Model):
#    nomeComposicao = models.CharField(max_length=30,default="", )
    #missao =  models.ForeignKey(Missao,verbose_name="Missão",related_name="missoes", blank=True, default="", null=True, )
    
'''
Missao - representa algo que o jogador deve fazer. Uma missão possui um conjunto de 1 - n condições para ser completada.

@param nome: nome da missao
@param descricao: descricao da missao
@param enredo: enredo apresentado na conclusao da missao
@param condicoes: condicoes necessárias para a missão
'''
class Missao(models.Model):
    nome = models.CharField(max_length=30,default="", )
    descricao = models.CharField(max_length=200,verbose_name="Descrição",default="descreva o objetivo da missão",)
    #tempo = models.TimeField(_(u"Tempo para Missão"),null=True,)#auto_now_add=True,
    #tempo = models.IntegerField(_(u"Tempo para Missão"),null=True,)
    tempo = models.IntegerField(_(u"Tempo para Missão"),null=True,)
    enredo = models.ForeignKey(Enredo,verbose_name="Enredo", related_name="enredo_missao", blank=True, default="", null=True, )
    #condicoes =  models.ForeignKey(CondicoesMissao,verbose_name="Condições para Missão",related_name="condicoes", blank=True, default="", null=True, )
    aventuras = models.ForeignKey(Aventura,verbose_name="Aventura",related_name="aventuras", blank=True, default="", null=True, )
 
    def __unicode__(self):
        return u'%s' % (self.nome)
    
    def get_nome_missao(self):
        return u'%s' % (self.nome)
    
 
'''
class MissaoAtiva - representa persistencia de dados de ma missão ativa

@param missao: missao que foi ativa
@param aventura_ativa_missao: aventura ativa
@param estado_missao: qndo True a missão foi completada
'''
class MissaoAtiva(models.Model):
    missao = models.ForeignKey(Missao,related_name="missao",blank=True, default="", null=True, )
    aventura_ativa_missao = models.ForeignKey(AventuraAtiva,related_name="aventura_ativa_missao",blank=True, default="", null=True,) 
    estado_missao = models.BooleanField(default=False)  



'''
Condicao - classe que representa atributos comuns para os três tipos de conções definidas no trabalho.

@param nome: nome da condicao - retirado por enquanto
@param ligacao: faz a ligacao "semantica" na visao do autor para prefixo e sufixo.
@param enredo: elemento que serve como feedback para o jogador   
'''
class Condicao(models.Model):
    GET_OBJ = 'GET_OBJ'#jogador pegou objeto
    START_TALK = 'START_TALK'#jogador começou um dialogo
    JOIN_OBJ = 'JOIN_OBJ'#jogador tentou combinar dois itens 
    LIGACAO = (
        (GET_OBJ, 'possui'),
        (START_TALK, 'conversou'),
        (JOIN_OBJ, 'combinou'),)
    AND = 'AND'#jogador pegou objeto
    OR = 'OR'# começou um dialogo
    OPERADOR = (
        (AND, 'AND'),
        (OR, 'OR'),)
    nome = models.CharField(max_length=30,default="", )
    operador = models.CharField(max_length=10, verbose_name="Operador Lógico", choices=OPERADOR ,default=AND)
    ligacao = models.CharField(max_length=20, verbose_name="Ligação", choices=LIGACAO ,default=GET_OBJ)
    enredo = models.ForeignKey(Enredo,verbose_name="Enredo", related_name="enredos", blank=True, default="", null=True, )
    missao = models.ForeignKey(Missao,verbose_name="Missão",related_name="condicoes_missao", blank=True, default="", null=True, )
    
    def get_ligacao(self):   
        if self.ligacao == "GET_OBJ":
            return u'possui'
        elif self.ligacao == "START_TALK":
            return u'conversou'
        else:
            return u'combinou'
    
    #def get_ligacao(self):
    #    if self.object
    #    return u'%s' % (self.nome)
        
    
'''
class CondicaoAtiva - condicao ativa

@param condicao: representa a condicacao que foi ativa
@param missao_ativa: ligacao com a missao ativa
@param aventura_ativa_condicao: representa a aventura que foi ativa
@param estado_condicao: presenta a estado da condicao
'''
class CondicaoAtiva(models.Model):
    condicao = models.ForeignKey(Condicao,related_name="condicao",blank=True, default="", null=True,) 
    missao_ativa = models.ForeignKey(MissaoAtiva,related_name="missao_ativa",blank=True, default="", null=True, )
    aventura_ativa_condicao = models.ForeignKey(AventuraAtiva,related_name="aventura_ativa_condicao",blank=True, default="", null=True,) 
    estado_condicao = models.BooleanField(default=False) 
    
    
       
'''
CondicaoInstanciaObjeto - representa a necessidade de relação entre dois objetos para satisfazer uma condição.

@param prefixo: nesta condicao refere-se a uma instancia de objeto
@param sufixo: nesta condicao refere-se a uma outra instancia de objeto 

Exemplo: instancia de objeto combinada com outra: tesouro combinou Caixa. Ou seja, tesouro esta na caixa.
'''
class CondicaoInstanciaObjeto(Condicao, models.Model):
    prefixo = models.ForeignKey(InstanciaObjeto,verbose_name="Instâncias de Objetos",related_name="prefixo_co_inst_obj", blank=True, default="", null=True, )
    sufixo = models.ForeignKey(InstanciaObjeto,verbose_name="Instâncias de Objetos", related_name="sufixo_co_inst_obj", blank=True, default="", null=True, )
    

'''
CondicaoJogadorInstancia - estabelece a condicao entre um Avatar de um jogador e um item (instancia Objeto)

@param prefixo: representa os avatares cadastrados naquela aventura
@param sufixo: representa as instancias de onjetos
'''
class CondicaoJogadorInstancia(Condicao, models.Model):
    prefixo = models.ForeignKey(Avatar,verbose_name="Avatares",related_name="prefixo_cji_avateres", blank=True, default="", null=True, )
    sufixo = models.ForeignKey(InstanciaObjeto,verbose_name="Instâncias de Objetos", related_name="sufixo_cji_inst_obj", blank=True, default="", null=True, )
    #quantidade = models.IntegerField(max_length=3,default=1)
 
'''
CondicaoJogadorObjeto - estabelece a condicao entre um Avatar de um jogador e Objeto

@param prefixo: representa os avatares cadastrados naquela aventura
@param sufixo: representa os objetos
@param  quantidade: representa a quantidade de objetos 
'''
class CondicaoJogadorObjeto(Condicao, models.Model):
    prefixo = models.ForeignKey(Avatar,verbose_name="Avatares",related_name="prefixo_cjo_avateres", blank=True, default="", null=True, )
    sufixo = models.ForeignKey(Objeto,verbose_name="Objetos", related_name="sufixo_cjo__obj", blank=True, default="", null=True, )
    quantidade = models.IntegerField(max_length=3,default=1)
 
     
'''
CondicaoDialogo - representa a condição que envolve tipos de dialogo, que são Dialogo Inicial, Dialogo Final, confirmação e negacao.

@param prefixo: representa os avatares dos jogadores
'''
class CondicaoDialogoInstancia(Condicao, models.Model):
    DIALOGO_INICIAL = 'DIALOGO_INICIAL'#inicia o dialogo
    DIALOGO_FINAL = 'DIALOGO_FINAL'#finaliza o dialogo
    ACEITO = 'ACEITO'#aceita algo dito pelo npc
    NEGACAO = 'NEGACAO'#aceita algo dito pelo npc 
    ESTADOS_DIALOGO = (
        (DIALOGO_INICIAL, u'Diálogo Inicial'),
        (DIALOGO_FINAL, u'Diálogo Final'),
        (ACEITO, u'Confirmação'),
        (NEGACAO, u'Negação'),)
    prefixo = models.ForeignKey(Avatar,verbose_name="Avatares",related_name="prefixo_cd_avateres", blank=True, default="", null=True, )
    sufixo =  models.CharField(max_length=20, choices=ESTADOS_DIALOGO ,default=DIALOGO_INICIAL)
    referencia_sufixo = models.ForeignKey(InstanciaObjeto,verbose_name="Instâncias de Objetos", related_name="ref_sufixo_cd_inst_obj", blank=True, default="", null=True, )
    
'''
NivelAutor: na aventura um autor pode ser o principal, com direito de excluir a aventura ou secundario, com direito de apenas editar a aventura

@param autor: id do autor registrado em uma determinada aventura 
@param aventura: aventura para qual o autor estar cadastrado
@param nivel: nivel de autorização do autor para a aventura  

Pedencia: Classe não utilizada no momento. 

class NivelAutor(models.Model):
    PRINCIPAL = 'Principal'
    SECUNDARIO = 'Secundário'
    NIVEL_AUTOR = (
        (PRINCIPAL, 'Principal'),
        (SECUNDARIO, 'Secundário'),)
    autor = models.ForeignKey(Autor, related_name="autor", blank=True, default="", null=True, )
    aventura_autor =  models.ForeignKey(Aventura, related_name="aventura_autor", blank=True, default="", null=True, )
    nivel = models.CharField(max_length=1, choices=NIVEL_AUTOR ,default=PRINCIPAL)
'''
    
'''
Agente - classe responsavem por conter o nome do agente e o tipo de comportamento.
'''
class Agente(models.Model):
    AGRESSIVO = 'Agressivo'
    PASSIVO = 'Passivo'
    COLABORATIVO = 'Colaborativo'
    COMPETIDOR = 'Competidor'
    COMPORTAMENTO = (
        (AGRESSIVO, 'Agressivo'),
        (PASSIVO, 'Passivo'),
        (COLABORATIVO, 'Colaborativo'),
        (COMPETIDOR, 'Competidor'),)
    nome = models.CharField(max_length=30,default="", )
    instancia =  models.ForeignKey(InstanciaObjeto, related_name="instancia", blank=True, default="", null=True, )
    proximidade = models.IntegerField(max_length=3,default=1)
    comportamento = models.CharField(max_length=15, choices=COMPORTAMENTO ,default=AGRESSIVO)
    aventura_agente = models.ForeignKey(Aventura, related_name="aventura_agente",blank=True,default="",null=True,)
    
'''
Comportamento - após acriação do agente, o autor deve criar e editar informações inerentes ao comportmento de agente definido
'''
class Comportamento(models.Model):
    pos_inicial =  models.ForeignKey(PosicaoGeografica, related_name="pos_inicial", blank=True, default="", null=True, )
    agente = models.ForeignKey(Agente, related_name="agente", blank=True, default="", null=True, )
    

'''
Agressivo
'''
class Agressivo(Comportamento, models.Model):
    item =  models.ForeignKey(InstanciaObjeto, related_name="instancia_agressivo", blank=True, default="", null=True, )
    avatar_vit = models.ForeignKey(Avatar,related_name="avatar_vit", blank=True, default="", null=True,)

'''
Passivo
'''
class Passivo(Comportamento, models.Model):
    #avatar_vit = models.ForeignKey(Avatar,related_name="avatar_vit", blank=True, default="", null=True,)
    pass


'''
Colaborativo
'''
class Colaborativo(Comportamento, models.Model):
    avatar_col = models.ForeignKey(Avatar,related_name="avatar_col", blank=True, default="", null=True,)
    obstaculoscl =  models.ManyToManyField(InstanciaObjeto, through='Mensagem', related_name="obstaculoscl", blank=True, default="", null=True, )
   
'''
Competitivo
'''
class Competitivo(Comportamento, models.Model):
    avatar_comp = models.ForeignKey(Avatar,related_name="avatar_comp", blank=True, default="", null=True,)
    obstaculoscp =  models.ManyToManyField(InstanciaObjeto, through='Mensagem', related_name="obstaculoscp", blank=True, default="", null=True, )
    
'''
Mensagem - mensagem usada nos agente Colaborativos e Competitivos
'''
class Mensagem(models.Model):
    mensagem = models.CharField(max_length=200,default="", )
    instancia_objeto =  models.ForeignKey(InstanciaObjeto, related_name="instancia_objeto", blank=True, default="", null=True, )
    colaborativo =  models.ForeignKey(Colaborativo, related_name="colaborativo", blank=True, default="", null=True, )
    competitivo =  models.ForeignKey(Competitivo, related_name="competitivo", blank=True, default="", null=True, )
    

'''
Mochila -  os itens do avatar do jogador são guardados na mochila

@param instancia_mochila: instancias guardadas na mochila.
                          Quando uma instância de objeto é guarda na mochila,
                          sua posicao em PosDinamicInstancia (lat,log e alt são nulas)
@param avatar_mochila: o avatar que possui a respectiva mochila 
'''
class Mochila(models.Model):
    instancia_mochila =  models.ManyToManyField(InstanciaObjeto, related_name="instancia_mochila", blank=True, default="", null=True, )   
    avatar_mochila =  models.ForeignKey(AvatarAtivo, related_name="avatar_mochila", blank=True, default="", null=True, )
    
    
'''
Mensagemcp - mensagem usada nos agente Colaborativos e Competitivos
'''
#class Mensagemcp(models.Model):
#    mensagem = models.CharField(max_length=200,default="", )
#    competitivo =  models.ForeignKey(Competitivo, related_name="competitivo", blank=True, default="", null=True, )

'''
Dialogo permite a criacao de um dialogo para o objeto do tipo personagem
Pendências nessa classe: Tratamento do XML para representar o diálogo.
Classe removida do modelo. 
Não existe a necessidade do diálogo ser separado da instância do objeto.

'''
#class Dialogo(models.Model):
#    dialogo = models.TextField('dialogo', blank=True)
#    descricao = models.CharField(max_length=100)
    
''''
Imagem é uma classe que representa a imagem para o objeto, no momento de autoria e do jogo.
Classe removida.
'''
#class ImagemObjeto(models.Model):
#    imagem = models.ImageField(upload_to='/obejtos/imagens/', verbose_name="Imagem Autoria")
#    descricao = models.CharField(max_length=100)



