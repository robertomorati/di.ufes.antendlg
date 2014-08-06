# -*- coding: utf-8 -*-
'''
Created on 18/09/2013

@author: Roberto Guimarães Morati Junior
'''
from django.conf.urls import patterns, url

from core.views import AventuraListView, AventuraCreateView, AventuraUpdateView
from core.views import AventuraDesativarView, AventuraDeleteView, AventuraGetJsonView, AventuraAtivarView, AventuraUpdatePositionView

from core.views import PosInstanciaAtivaCreateView, AvatarAtivoCreateView, MissaoAtivaCreateView, AventuraAutoriaEstadoUpdateView

from core.views import AventuraAtivaListView, AtivarAventuraView, AventuraAtivaUpdateView,AventuraAtivaDeleteView,CondicaoAtivaCreateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',                               
  
    #urls para aventura
    #lista aventuras ativas
    
    url(r'^aventura/update_estado_autoria/(?P<pk>\d+)/$', AventuraAutoriaEstadoUpdateView.as_view(), name='autoria_estado_update_view',),
    url(r'^aventura/(?P<pk>\d+)/$', AventuraListView.as_view(), name='aventura_list_view'),
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
    
    #urls relacionadas a ativacao de aventuras
    url(r'^estado_aventura/create_instances_activates/$', PosInstanciaAtivaCreateView.as_view(), name='instances_activates_view'),
    url(r'^estado_aventura/create_avatars_activates/$', AvatarAtivoCreateView.as_view(), name='avatars_activates_view'),
    url(r'^estado_aventura/create_missions_activates/$', MissaoAtivaCreateView.as_view(), name='missions_activates_view'),
    url(r'^estado_aventura/create_conditions_activates/$', CondicaoAtivaCreateView.as_view(), name='conditions_activates_view')
    
    
)
