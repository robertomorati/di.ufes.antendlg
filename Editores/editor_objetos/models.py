# -*- coding: utf-8 -*-
'''
Created on 16/09/2013

Models para o Ambiente de Autoria de DLG

@author: Roberto Guimaraes Morati Junior
'''

from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import User 
from django.utils.translation import gettext as _
#from imagekit.models import ImageSpecField

'''
Class TipoObjeto 

Representa o tipo de um objeto, ou seja, o autor da aventura ao criar um objeto irá relacionar este objeto a um tipo.
Por exemplo, o objeto Cascumpus é do tipo de objeto Monstro.

@param tipo: representa o nome do tipo de objeto
@param descricao: apresenta uma descrição do tipo de objeto
@param posicoes_geograficas: remete a quantidade de posições geográficas que um objeto de um dado tipo poderá assumi. 
                             Por exemplo, objeto do tipo Limite do Labirinto, esse objeto pode assumir 4 posições geográficas. 
                             Assim delimitando a área do geografica do jogo, por meio de uma sugestão.
'''
class TipoObjeto(models.Model):
    tipo = models.CharField(max_length=30)
    descricao = models.CharField(max_length=100)
    posicoes_geograficas = models.IntegerField(max_length=3,default=1, help_text=u"Delimita a quantidade de posições geográficas da instância do objeto.")
    
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
    
    #def get_objeto(self):
    #    return  self.related_object.get_accessor_name().select_related().count()
    #@permalink
    #def get_absolute_url(self):
    #     return reverse('criar_tipo_objeto/', (), [self.pk])
    #    class Meta:
    #    verbose_name = 'lista de tipos'

'''
Icone é uma imagem que representa o objeto durante o momento de autoria.
Em outras palavras, quanto o objeto é arrastado para o mapa, a imagem do icone é copiada para o marcador do google maps.

@param nome: é o nome da imagem de autoria.
@param icone: é o diretorio para imagem do icone

Pendências: Redimensionar o icone para tamanho padrão.

'''
class Icone (models.Model):
    nome =  models.CharField(max_length=30,)
    icone = models.ImageField(upload_to ='imagens/icones/', help_text="Ícone do objeto.", blank=True,)
    
    #retorna o icone (dir)
    def __unicode__(self):
        return u'%s' % (self.icone)

    #def get_attribute_icone(self):
    #    return u'%s' % (self.icone)
    
    #verifica se ícone nao esta sendo utilizado por algum objeto
    def delete(self, *args, **kwargs):
        if not self.icones.all():
            storage, path = self.icone.storage, self.icone.path
            super(Icone, self).delete(*args, **kwargs)
            return storage.delete(path)
        raise ValidationError(u"Não é possível remover este ícone pois existem objetos relacionados à ele!")


    
'''
Sugestao é um elemente de percepção para a instância do objeto. 
A sugestão indica para o jogador que o mesmo está próximo de um perigo. 
Por exemplo, a proximidade com o Cascumpus pode ser indicada por um áudio de rugido.

@param tipo: a sugestão pode ser de três tipos: áudio, como um rugido do Cascumpus; imagem: fumaça do fogo; e texto, uma mensagem.
@param sugestao: url da sugestão.
@param proximidade: é a distância que o jogador tem que estar da sugestão para que ele tenha percepção da mesma.   

Pendências nessa classe: Identificar tipos de arquivos.
'''
class Sugestao(models.Model):
    TEXTO = 0
    AUDIO = 1
    IMAGEM = 2 
    TIPO_IMAGEMS = (
        (0, 'Texto'),
        (1, 'Áudio'),
        (2, 'Imagem'),)
    tipo = models.CharField(max_length=1, choices=TIPO_IMAGEMS ,default=TEXTO)
    sugestao = models.FileField(upload_to ='sugestao/', help_text="Sugestão para tomada de decisão.", )
    proximidade = models.IntegerField(max_length=3,default=1)
    
    def __unicode__(self):
        return u'%s' % (self.sugestao) 
   
 
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
    #img = models.ImageField(upload_to='../media/imagens/',verbose_name="Imagem Autoria")
    
    def _unicode_(self):
        return u'%s' % (self.nome)



'''
Dialogo permite a criacao de um dialogo para o objeto do tipo personagem
Pendências nessa classe: Tratamento do XML para representar o diálogo.
Classe removida do modelo. 
Não existe a necessidade do diálogo ser separado da instância do objeto.

'''
#class Dialogo(models.Model):
#    dialogo = models.TextField('dialogo', blank=True)
#    descricao = models.CharField(max_length=100)
    
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
    #autores = models.ManyToManyField(Autor, related_name="autores_aventura",)
    
    #def set_auto(self, id):
    #    self.autor = id

#class AventuraForm(forms.ModelForm):
#        def __init__(self, *args, **kwargs):
#            super(AventuraForm, self).__init__(*args, **kwargs)
#            self.fields['fim'].widget = forms.DateField(widget=SelectDateWidget(years=range(date.today().year, 2099)),)
#        class Meta:
#            model = Aventura
    
'''
InstanciaObjeto representa um objeto que é arrastado para o mapa da aventura
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
    DES = 0
    AVATAR = 1
    AGENTE = 2 
    TIPO_ENCENACAO = (
        (0, 'Desativado'),
        (1, 'Avatar'),
        (2, 'Agente'),)
    nome = models.CharField(max_length=30)
    proximidade = models.IntegerField(max_length=3,default=1)
    visivel = models.BooleanField(default=True, help_text=u"Informa se o objeto está visivel na aventura.")
    encenacao = models.CharField(max_length=1, choices=TIPO_ENCENACAO ,default=DES,help_text=u"Indica o tipo de encenação que é possível com a instância do objeto.")
    objeto = models.ForeignKey(Objeto, related_name="instancias_objeto",blank=True,default="",)
    sugestao = models.ForeignKey(Sugestao, related_name="sugestao_objeto", blank=True, default="", null=True, )
    aventura = models.ForeignKey(Aventura, related_name="aventura_inst_obj", blank=True, default="", null=True,)
    instancia_cont = models.IntegerField(max_length=3,default=0,)
    dialogo = models.TextField('dialogo', blank=True)
    #dialogo = models.ForeignKey(Dialogo, related_name="dialogo",blank=True,)
    #posicao_geografica_ = models.ManyToManyField(PosicaoGeografica, related_name="pos_geo_inst_objeto",) 
    #pos possui a instnacia do objeto, pois dependendo do tipo de objeto, esse poderá ter n POS
    #sugestao_objeto =  models.ForeignKey(Sugestao, related_name="sugestao_instancia_objeto", )
    
    def _unicode_(self):
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
    
    
''''
Imagem é uma classe que representa a imagem para o objeto, no momento de autoria e do jogo.
Classe removida.
'''
#class ImagemObjeto(models.Model):
#    imagem = models.ImageField(upload_to='/obejtos/imagens/', verbose_name="Imagem Autoria")
#    descricao = models.CharField(max_length=100)

'''
TipoImagem representa o tipo de imagem para a instância de objeto.
           a imagem pode ser 2D ou 3D. 
           2D - uso do google maps para jogar
           3D - uso da camera do dispositivo móvel.
@param tipo: tipo de imnagem cadastrada
@param img: url da imagem 
'''
class TipoImagem(models.Model):
    IMG_MAP = 0
    IMG_CAM = 1 
    TIPO_IMAGEMS = (
        (0, 'Imagem 2D'),
        (1, 'Imagem 3D'),)
    tipo = models.CharField(max_length=1, choices=TIPO_IMAGEMS ,default=IMG_MAP)
    img = models.FileField(upload_to ='imagens/img_play/',null=True, blank=True)
    descricao = models.CharField(max_length=100, default="")
    
    #def _unicode_(self):
    #    return u'%s' % (self.tipo)    


'''
NivelAutor: na aventura um autor pode ser o principal, com direito de excluir a aventura ou secundario, com direito de apenas editar a aventura

@param autor: id do autor registrado em uma determinada aventura 
@param aventura: aventura para qual o autor estar cadastrado
@param nivel: nivel de autorização do autor para a aventura  

Pedencia: Classe não utilizada no momento. 
          Permitir a aventura ter autores secundarios e primarios. 
'''
class NivelAutor(models.Model):
    PRINCIPAL = 0
    SECUNDARIO = 1
    NIVEL_AUTOR = (
        (0, 'Principal'),
        (1, 'Secundário'),)
    #autor = models.ForeignKey(Autor, related_name="autor", blank=False,)
    #aventura =  models.ForeignKey(Aventura, related_name="aventura", blank=False,)
    #nivel = models.CharField(max_length=1, choices=NIVEL_AUTOR ,default=PRINCIPAL)
