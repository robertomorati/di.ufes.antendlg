# -*- coding: utf-8 -*-
'''
Created on 04/12/2013

@author: Roberto Guimarães Morati Junior
'''
from django.conf.urls import patterns, url
from core.views import MissaoListView,MissaoCreateView,MissaoUpdateView,MissaoDeleteView, CondicaoInstanciaObjetoCreateView
from core.views import CondicaoDeleteView,CondicaoInstanciaObjetoUpdateView
from core.views import CondicaoJogadorInstanciaListView, CondicaoJogadorInstanciaCreateView,CondicaoJogadorInstanciaUpdateView
from core.views import CondicaoDialogoInstanciaListView, CondicaoDialogoInstanciaCreateView, CondicaoDialogoInstanciaUpdateView
from core.views import CondicoesMissaoListView,CondicaoObjetoListView, CondicaoJogadorObjetoListView, CondicaoJogadorObjetoCreateView, CondicaoJogadorObjetoUpdateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',                           
    #urls para missao
    url(r'^missao/$', MissaoListView.as_view(), name='missao_list_view'),
    url(r'^missao/criar_missao/$', MissaoCreateView.as_view(), name='missao_create_view'),
    url(r'^missao/update_missao/(?P<pk>\w+)/$', MissaoUpdateView.as_view(), name='missao_update_view',),
    url(r'^missao/delete_missao/(?P<pk>\w+)/$', MissaoDeleteView.as_view(), name='missao_delete_view',),
    #url(r'^get_lista_tipo_objeto/$', TipoObjetoGetJsonView.as_view(), name='tipo_objeto_get_view'),

    #urls gerais
    url(r'^condicoes/delete_condicao/(?P<pk>\w+)/$', CondicaoDeleteView.as_view(), name='condicao_delete_view'),
    url(r'^condicoes/listar_concicoes_missao/(?P<pk>\w+)/$', CondicoesMissaoListView.as_view(), name='condicoes_missao_list_view'),
    
    #urls para condições entre objetos
    url(r'^condicoes_objeto/$', CondicaoObjetoListView.as_view(), name='condicao_objeto_list_view'),
    url(r'^condicoes_objeto/criar_condicao/$', CondicaoInstanciaObjetoCreateView.as_view(), name='condicao_objeto_create_view'),
    url(r'^condicoes_objeto/update_condicao/(?P<pk>\w+)/$', CondicaoInstanciaObjetoUpdateView.as_view(), name='condicao_objeto_update_view'),
    
    #urls para condições entre objetos
    url(r'^condicoes_jogador_instancia/$', CondicaoJogadorInstanciaListView.as_view(), name='condicao_jogador_instancia_list_view'),
    url(r'^condicoes_jogador_instancia/criar_condicao/$', CondicaoJogadorInstanciaCreateView.as_view(), name='condicao_jogador_create_view'),
    url(r'^condicoes_jogador_instancia/update_condicao/(?P<pk>\w+)/$', CondicaoJogadorInstanciaUpdateView.as_view(), name='condicao_jogador_update_view'),
    
    #urls para condições entre objetos
    url(r'^condicoes_jogador_objeto/$', CondicaoJogadorObjetoListView.as_view(), name='condicao_jogador_objeto_list_view'),
    url(r'^condicoes_jogador_objeto/criar_condicao/$', CondicaoJogadorObjetoCreateView.as_view(), name='condicao_jogador_objeto_create_view'),
    url(r'^condicoes_jogador_objeto/update_condicao/(?P<pk>\w+)/$', CondicaoJogadorObjetoUpdateView.as_view(), name='condicao_jogador_objeto_update_view'),
 
    
    #urls para condições que envolvam dialogos
    url(r'^condicoes_dialogo/$', CondicaoDialogoInstanciaListView.as_view(), name='condicao_dialogo_list_view'),
    url(r'^condicoes_dialogo/criar_condicao/$', CondicaoDialogoInstanciaCreateView.as_view(), name='condicao_dialogo_create_view'),
    url(r'^condicoes_dialogo/update_condicao/(?P<pk>\w+)/$', CondicaoDialogoInstanciaUpdateView.as_view(), name='condicao_dialogo_update_view'),
 
)