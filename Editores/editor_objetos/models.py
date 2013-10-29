# -*- coding: utf-8 -*-
'''
Created on 16/09/2013

Models para o Editor de Objetos

@author: Roberto Guimaraes Morati Junior
'''

from django.db import models
#from south.creator.actions import DeleteField
#from django.views.generic.edit import DeleteView
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import User 
#from django.contrib.auth.models import User, make_password, is_password_usable, check_password
from django.utils.translation import gettext as _
from django.template.defaultfilters import default
from pkg_resources import require
#from imagekit.models import ImageSpecField

'''
Class TipoObjeto 
Representa o tipo de um objeto, ou seja, o autor da aventura ao criar um objeto irá selecionar um tipo para o objeto.
Por exemplo, o objetos Cascumpus é do tipo de objeto Monstro.
@param tipo: tem o nome do tipo de objeto,
@param descricao: apresenta uma descrição do tipo de objeto
@param posicoes_geograficas: remete a quantidade de posições geográficas que um objeto de um dado tipo poderá assumi. 
                             Por exemplo, objeto do tipo Limite do Labirinto, esse objeto pode assumir 4 posições geográficas. 
                             Assim delimitando a área do geografica do jogo.
@param dialogo:esse parametro indica se um objeto do tipo pode ou não ter um diálogo. 
'''
class TipoObjeto(models.Model):
    tipo = models.CharField(max_length=30)
    descricao = models.CharField(max_length=100)
    posicoes_geograficas = models.IntegerField(max_length=3,default=1, help_text=u"Delimita a quantidade de posições geográficas da instância do objeto.")
    dialogo = models.BooleanField(default=True, help_text=u"Delimita se a instancia de um objeto pode ter um dialogo.")
    
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
Sugestao é um elemente de percepção para a instância do objeto. A sugestão indica para o jogador que o mesmo está próximo de um perigo, como o Cascumpus.
@param tipo: a sugestão pode ser de três tipos: audio, como um rugido do Cascumpus; imagem: fumaça do fogo; 
@param sugestao: é a sugestão armazenada.
@param proximidade: é a distância que o jogador tem que estar da sugestão para que ele tenha percepção da mesma.   

Pendências nessa classe: Identificar tipos de arquivos.
'''
class Sugestao(models.Model):
    TEXTO = 0
    AUDIO = 1
    IMAGEM = 2 
    TIPO_IMAGEMS = (
        (0, 'Imagem Autoria'),
        (1, 'Imagem 2D'),
        (2, 'Imagem 3D'),)
    tipo = models.CharField(max_length=1, choices=TIPO_IMAGEMS ,default=TEXTO)
    sugestao = models.FileField(upload_to ='sugestao/', help_text="Sugestão para instância objeto.", blank=True,)
    proximidade = models.IntegerField(max_length=3,default=1)    
    
'''
Objeto possui TipoObjeto e o Objeto, sendo instanciado na aventura quando arrastado para o mapa.
@param nome: nome do objeto criado
@param descricao: qual o papel do objeto? 
@param quantidade: quantida de instânciados que pode ter do respectivo objeto no mapa
@param coletavel: informa se o objeto pode ser coletado na aventura pelo jogador
@param tipo_objeto: informa o tipo de objeto ao qual o objeto está vinculado
@param incone_objeto: representa a imagem do objeto no momento de autoria    
    
  Adicionar propriedade publico/privado.
'''
class Objeto (models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.CharField(max_length=100)
    quantidade = models.IntegerField(max_length=100,default=1)
    coletavel = models.BooleanField(default=False, help_text=u"Informa se o objeto pode ser coletado durante a aventura.")
    tipo_objeto = models.ForeignKey(TipoObjeto, related_name="objetos",)
    icone_objeto = models.ForeignKey(Icone, related_name="icones", default="", )
    #img = models.ImageField(upload_to='../media/imagens/',verbose_name="Imagem Autoria")
    
    def _unicode_(self):
        return u'%s' % (self.nome)



'''
Dialogo permite a criacao de um dialogo para o objeto do tipo personagem

Pendências nessa classe: Tratamento do XML para representar o diálogo.

'''
class Dialogo(models.Model):
    dialogo = models.TextField('dialogo', blank=True)
    descricao = models.CharField(max_length=100)
    
'''
Posições Geográficas para instâncias de objetos.
@param latitude
@param  longitude
@param altitude: para objetos em 3D apresentados por meio da camera do dispositivo movel.

'''
class PosicaoGeografica(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    
    
'''
InstanciaObjeto representa um objeto que é arrastado para o mapa da aventura
@param nome:nome da instancia do objeto
@param proximidade: distância que o jogador deve estar do objeto para que possa ver o mesmo
@param visivel: este atributo permite indicar se determinado objeto deve estar visivel na aventura em um dado momento.
@param encenacao: indica se o objeto pode ser controlado por outro jogador.
@param dialogo: representa a relação da instancia do o seu dialogo.
@param posicao_geografica: relacao da instancia com a sua posicao geografica.
@param sugestao: descrito anteriormente.

Pendencias: Rever o atributo sugestão; Adicionar relação com a aventura;
'''
class InstanciaObjeto(models.Model):
    nome = models.CharField(max_length=30)
    proximidade = models.IntegerField(max_length=3,default=1)
    visivel = models.BooleanField(default=True, help_text=u"Informa se o objeto está visivel na aventura.")
    encenacao = models.BooleanField(default=True, help_text=u"Indica se o objeto pode ser controlado por outro jogador.")
    dialogo = models.ForeignKey(Dialogo, related_name="dialogo_objeto",)
    posicao_geografica_ = models.ManyToManyField(PosicaoGeografica, related_name="pos_geo_inst_objeto",)
    sugestao = models.ForeignKey(Sugestao, related_name="sugestao_objeto", blank=True, default="Selecione a sugestão." )
    #sugestao_objeto =  models.ForeignKey(Sugestao, related_name="sugestao_instancia_objeto", )
    
    def _unicode_(self):
        return u'%s' % (self.nome)

    
''''
Não está sendo utilizado.
Imagem é uma classe que representa a imagem para o objeto, no momento de autoria e do jogo
'''
class ImagemObjeto(models.Model):
    imagem = models.ImageField(upload_to='/obejtos/imagens/', verbose_name="Imagem Autoria")
    descricao = models.CharField(max_length=100)

'''
TipoImagem representa o tipo de imagem, sendo uma imagem para autoria. 2D ou 3D
'''
class TipoImagem(models.Model):
    IMG_AUTORIA = 0
    IMG_MAP = 1
    IMG_CAM = 2 
    TIPO_IMAGEMS = (
        (0, 'Imagem Autoria'),
        (1, 'Imagem 2D'),
        (2, 'Imagem 3D'),)
    tipo = models.CharField(max_length=1, choices=TIPO_IMAGEMS ,default=IMG_AUTORIA)
    descricao = models.CharField(max_length=100)
    
    #def _unicode_(self):
    #    return u'%s' % (self.tipo)    

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
NivelAutor: na aventura um autor pode ser o principal, com direito de excluir a aventura ou secundario, com direito de apenas editar a aventura

@param autor: id do autor registrado em uma determinada aventura 
@param aventura: aventura para qual o autor estar cadastrado
@param nivel: nivel de autorização do autor para a aventura  
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