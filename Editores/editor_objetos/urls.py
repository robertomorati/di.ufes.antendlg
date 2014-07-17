# -*- coding: utf-8 -*-
'''
Created on 18/09/2013

@author: Roberto Guimarães Morati Junior
'''
from django.conf.urls import patterns, url
from core.views import TipoObjetoUpdateView, TipoObjetoCreateView, TipoObjetoListView, TipoObjetoDeleteView, TipoObjetoGetJsonView,\
    CondicaoAtivaCreateView
from core.views import ObjetoCreateView, ObjetoUpdateView, ObjetoListView, ObjetoDeleteView, ObjetoGetJsonView
from core.views import IconeCreateView, IconeListView, IconeUpdateView, IconeDeleteView, IconeGetJsonView
from core.views import GMapView, MsgShowView, PosicaoGeograficaCreateView, PosicaoGeograficaUpdateView, PosicaoGeograficaGetJsonView, PosicaoGeograficaDeleteView
from core.views import AventuraListView, AventuraCreateView, AventuraUpdateView, AventuraDeleteView, AventuraGetJsonView, AventuraAtivarView, AventuraUpdatePositionView
from core.views import InstanciaObjetoCreateView, InstanciaObjetoGetJsonView, InstanciaObjetoUpdateView, InstanciaObjetoDeleteView, AventuraDesativarView
from core.views import SugestaoListView, SugestaoCreateView, SugestaoUpdateView, SugestaoDeleteView
from core.views import TipoImagemListView, TipoImagemCreateView, TipoImagemUpdateView, TipoImagemDeleteView
from core.views import PosInstanciaAtivaCreateView, AvatarAtivoCreateView, MissaoAtivaCreateView, CondicaoAtivaCreateForm

from core.views import AventuraAtivaListView, AtivarAventuraView, AventuraAtivaUpdateView,AventuraAtivaDeleteView

from django.contrib import admin
admin.autodiscover()



#from django.conf.urls import url, patterns, include
#from rest_framework import viewsets, routers

# Routers provide an easy way of automatically determining the URL conf.#
#router = routers.DefaultRouter()
#router.register(r'aventuras', AventuraViewSet)



urlpatterns = patterns('',        
                       
    #url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),     
    #url(r'^api-auth/aventuras/$', AventuraViewSet.as_view(), name='aventuras-resource'),  
    
    #urls para tipo de objeto
    url(r'^tipo_objeto/$', TipoObjetoListView.as_view(), name='tipo_objeto_list_view'),
    url(r'^tipo_objeto/criar_tipo_objeto/$', TipoObjetoCreateView.as_view(), name='tipo_objeto_create_view'),
    url(r'^tipo_objeto/(?P<pk>\w+)/$', TipoObjetoUpdateView.as_view(), name='tipo_objeto_update_view',),
    url(r'^tipo_objeto/delete_tipo_objeto/(?P<pk>\w+)/$', TipoObjetoDeleteView.as_view(), name='tipo_objeto_delete_view',),
    url(r'^get_lista_tipo_objeto/$', TipoObjetoGetJsonView.as_view(), name='tipo_objeto_get_view'),
    
    #urls para objeto
    url(r'^objeto/$', ObjetoListView.as_view(), name='objeto_list_view'),
    url(r'^objeto/criar_objeto/$', ObjetoCreateView.as_view(), name='objeto_create_view'),
    #url(r'^objeto/update_objeto/$', ObjetoUpdateView.as_view(), name='objeto_update_view',),
    url(r'^objeto/update_objeto/(?P<pk>\w+)/$', ObjetoUpdateView.as_view(), name='objeto_update_view',),
    url(r'^objeto/delete_objeto/(?P<pk>\w+)/$', ObjetoDeleteView.as_view(), name='objeto_delete_view',),
    url(r'^objeto/get_lista_objetos/(?P<pk>\w+)/$', ObjetoGetJsonView.as_view(), name='objeto_get_json_view'),
    
    #urls para icones do objeto
    url(r'^icones/$', IconeListView.as_view(), name='icone_list_view'),
    url(r'^icones/criar_icone/$', IconeCreateView.as_view(), name='icone_create_view'),
    url(r'^icones/update_icone/(?P<pk>\w+)/$', IconeUpdateView.as_view(), name='icone_update_view',),
    url(r'^icones/delete_icone/(?P<pk>\w+)/$', IconeDeleteView.as_view(), name='icone_delete_view',),
    url(r'^get_url_icone/(?P<pk>\w+)/$', IconeGetJsonView.as_view(), name='icon_get_json_url_view'),

    #urls para aventura
    #lista aventuras ativas
    url(r'^aventura/(?P<pk>\d+)/$', AventuraListView.as_view(), name='aventura_list_view',),
    url(r'^aventura/ativar_aventura/(?P<pk>\w+)/$', AventuraAtivarView.as_view(), name='aventura_ativar_edicao_view',),#editar remete a criação da aventura
    url(r'^aventura/desativar_aventura/(?P<pk>\w+)/$', AventuraDesativarView.as_view(), name='aventura_desativar_edicao_view',),#editar remete a criação da aventura
    url(r'^aventura/criar_aventura/(?P<pk>\w+)/$', AventuraCreateView.as_view(), name='aventura_create_view',),
    url(r'^aventura/update_aventura/(?P<pk>\w+)/$', AventuraUpdateView.as_view(), name='aventura_update_view',),
    url(r'^aventura/delete_aventura/(?P<pk>\w+)/$', AventuraDeleteView.as_view(), name='aventura_delete_view',),
    url(r'^get_json_aventura/(?P<pk>\w+)/$', AventuraGetJsonView.as_view(), name='aventura_get_json_url_view',),
    #atualiza posicao da aventura
    url(r'^aventura/aventuras_ativas/$', AventuraAtivaListView.as_view(), name='avtentura_ativas_list_view',),
    url(r'^aventura_instancia/ativar_aventura_jogar/$', AtivarAventuraView.as_view(), name='ativar_aventura_create_view',),
    url(r'^aventura_instancia/update_aventura_ativa/(?P<pk>\d+)/$', AventuraAtivaUpdateView.as_view(), name='aventura_ativa_update_view',),
    url(r'^aventura_instancia/delete_aventura_ativa/(?P<pk>\d+)/$', AventuraAtivaDeleteView.as_view(), name='aventura_ativa_delete_view',),
    url(r'^set_json_aventura/(?P<pk>\w+)/$', AventuraUpdatePositionView.as_view(), name='aventura_set_json_view',),


    #views para instancia de objeto
    url(r'^instancia_objeto/create_instancia/$', InstanciaObjetoCreateView.as_view(), name='instancia_objeto_view'),#cria a isntancia por meio de json
    url(r'^instancia_objeto/get_instancia/(?P<pk>\w+)/$', InstanciaObjetoGetJsonView.as_view(), name='instancia_objeto_getjson_view'),#cria a isntancia por meio de json
    url(r'^instancia_objeto/update_instancia/(?P<pk>\w+)/$', InstanciaObjetoUpdateView.as_view(), name='instancia_objeto_update_view'),
    url(r'^instancia_objeto/delete_instancia/(?P<pk>\w+)/$', InstanciaObjetoDeleteView.as_view(), name='instancia_objeto_delete_view'),
    
    #urlviews para POS
    url(r'^posicao_geografica/create_pos/$', PosicaoGeograficaCreateView.as_view(), name='posicao_geografica_create_view'),
    url(r'^posicao_geografica/update_pos/(?P<pk>\w+)/$', PosicaoGeograficaUpdateView.as_view(), name='posicao_geografica_update_view'),
    url(r'^posicao_geografica/get_json_pos/(?P<pk>\w+)/$', PosicaoGeograficaGetJsonView.as_view(), name='posicao_geografica_get_json_view'),
    url(r'^posicao_geografica/delete_pos/(?P<pk>\w+)/$', PosicaoGeograficaDeleteView.as_view(), name='posicao_geografica_get_json_view'),
    
    #urls para sugestões
    url(r'^sugestoes/$', SugestaoListView.as_view(), name='sugestao_list_view'),
    url(r'^sugestoes/criar_sugestoes/$', SugestaoCreateView.as_view(), name='sugestao_create_view'),
    url(r'^sugestoes/update_sugestoes/(?P<pk>\w+)/$', SugestaoUpdateView.as_view(), name='sugestao_update_view'),
    url(r'^sugestoes/delete_sugestoes/(?P<pk>\w+)/$', SugestaoDeleteView.as_view(), name='sugestao_delete_view'),
    
    
    #urls para TipoImagem
    url(r'^tipo_imagem/$', TipoImagemListView.as_view(), name='tipo_imagem_list_view'),
    url(r'^tipo_imagem/criar_tipo_imagem/$', TipoImagemCreateView.as_view(), name='tipo_imagem_create_view'),
    url(r'^tipo_imagem/update_tipo_imagem/(?P<pk>\w+)/$', TipoImagemUpdateView.as_view(), name='tipo_imagem_update_view'),
    url(r'^tipo_imagem/delete_tipo_imagem/(?P<pk>\w+)/$', TipoImagemDeleteView.as_view(), name='tipo_imagem_delete_view'),
    

    #urls para pagina do google maps
    url(r'^gmaps/$', GMapView.as_view(), name='gmaps_view'),
    url(r'^gmap/msg/$', MsgShowView.as_view(), name='posicao_aventura_view'),#msg que posicao da aventura foi alterada
    #url(r'^gmaps/$', GMapView.as_view(), name='gmaps_view'), com id da aventura
    
    
    #urls relacionadas a ativacao de aventuras
    url(r'^estado_aventura/create_instances_activates/$', PosInstanciaAtivaCreateView.as_view(), name='instances_activates_view'),
    url(r'^estado_aventura/create_avatars_activates/$', AvatarAtivoCreateView.as_view(), name='avatars_activates_view'),
    url(r'^estado_aventura/create_missions_activates/$', MissaoAtivaCreateView.as_view(), name='missions_activates_view'),
     url(r'^estado_aventura/create_conditions_activates/$', CondicaoAtivaCreateView.as_view(), name='conditions_activates_view')
)
