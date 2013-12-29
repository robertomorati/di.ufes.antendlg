# -*- coding: utf-8 -*-
'''
Created on 04/12/2013

@author: Roberto Guimarães Morati Junior
'''
from django.conf.urls import patterns, url
from core.views import AvataresListView, AvataresCreateView, AvataresUpdateView, AvataresDeleteView, AvataresListInstancesView, AvataresUpdateRolesView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',                           
    #urls para tipo de objeto
    url(r'^avatares/$', AvataresListView.as_view(), name='avatar_list_view'),
    url(r'^avatares/criar_avatar/$', AvataresCreateView.as_view(), name='avatar_create_view'),
    url(r'^avatares/update_avatar/(?P<pk>\w+)/$', AvataresUpdateView.as_view(), name='avatar_update_view',),
    url(r'^avatares/delete_avatar/(?P<pk>\w+)/$', AvataresDeleteView.as_view(), name='avatar_delete_view',),
    #url(r'^get_lista_tipo_objeto/$', TipoObjetoGetJsonView.as_view(), name='tipo_objeto_get_view'),
    
    url(r'^papeis/$', AvataresListInstancesView.as_view(), name='avatar_list_instances_view'),
    url(r'^papeis/role/(?P<pk>\w+)/$', AvataresUpdateRolesView.as_view(), name='avatar_update_roles__view',),
 
)