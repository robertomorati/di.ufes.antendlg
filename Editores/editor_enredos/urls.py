# -*- coding: utf-8 -*-
'''
Created on 04/12/2013

@author: Roberto Guimarães Morati Junior
'''
from django.conf.urls import patterns, url
from core.views import EnredoListView,EnredoCreateView,EnredoUpdateView,EnredoDeleteView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',                           
    #urls para tipo de objeto
    url(r'^enredos/$', EnredoListView.as_view(), name='enredo_list_view'),
    url(r'^enredos/criar_enredo/$', EnredoCreateView.as_view(), name='enredo_create_view'),
    url(r'^enredos/update_enredo/(?P<pk>\w+)/$', EnredoUpdateView.as_view(), name='enredo_update_view',),
    url(r'^enredos/delete_enredo/(?P<pk>\w+)/$', EnredoDeleteView.as_view(), name='enredo_delete_view',),
    #url(r'^get_lista_tipo_objeto/$', TipoObjetoGetJsonView.as_view(), name='tipo_objeto_get_view'),
 
)