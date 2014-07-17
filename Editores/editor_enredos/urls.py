# -*- coding: utf-8 -*-
'''
Created on 04/12/2013

@author: Roberto Guimarães Morati Junior
'''
from django.conf.urls import patterns, url
from core.views import EnredoInstanciaListView,EnredoInstanciaCreateView,EnredoDeleteView 
from core.views import EnredoFileCreateView, EnredoFileListView,EnredoMensagemCreateView,EnredoMessageListView
from core.views import EnredoFileUpdateView, EnredoInstanciaUpdateView,EnredoMensagemUpdateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',                           
    #urls para tipo de objeto
    url(r'^enredos/lista_enredo_file/$', EnredoFileListView.as_view(), name='enredo_file_list_view'),
    url(r'^enredos/lista_enredo_instancia/$', EnredoInstanciaListView.as_view(), name='enredo_instancia_list_view'),
    url(r'^enredos/lista_enredo_mensagem/$', EnredoMessageListView.as_view(), name='enredo_mensagem_list_view'),
    
    url(r'^enredos/criar_enredo_file/$', EnredoFileCreateView.as_view(), name='enredo_file_create_view'),
    url(r'^enredos/criar_enredo_instancia/$', EnredoInstanciaCreateView.as_view(), name='enredo_instancia_create_view'),
    url(r'^enredos/criar_enredo_mensagem/$', EnredoMensagemCreateView.as_view(), name='enredo_mensagem_create_view'),
   
    url(r'^enredos/update_enredo_file/(?P<pk>\w+)/$', EnredoFileUpdateView.as_view(), name='enredo_file_update_view',),
    url(r'^enredos/update_enredo_instancia/(?P<pk>\w+)/$', EnredoInstanciaUpdateView.as_view(), name='enredo_instancia_update_view',),
    url(r'^enredos/update_enredo_mensagem/(?P<pk>\w+)/$', EnredoMensagemUpdateView.as_view(), name='enredo_mensagem_update_view',),
    
    
    url(r'^enredos/delete_enredo/(?P<pk>\w+)/$', EnredoDeleteView.as_view(), name='enredo_delete_view',),
    #url(r'^get_lista_tipo_objeto/$', TipoObjetoGetJsonView.as_view(), name='tipo_objeto_get_view'),
 
)