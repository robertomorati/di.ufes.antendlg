# -*- coding: utf-8 -*-
'''
Created on 23/01/2014

@author: Roberto Guimaraes Morati Junior
'''
from django.conf.urls import patterns, url
from core.views import AgentesListView, AgenteCreateView,AgressivoCreateView,AgenteSessionView,AgressivoUpdateView,AgenteUpdateView, ComportamentoOldDeleteView, PassivoCreateView
from core.views import PassivoUpdateView, ColaborativoCreateView, ColaborativoUpdateView, InstanciasCreateView,ListInstances, InstanciasUpdateView, CompetitivoCreateView,CompetitivoUpdateView
from core.views import AgenteDeleteView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',  
                                                
    #urls para agentes
    url(r'^agente/$', AgentesListView.as_view(), name='agente_list_view'),
    url(r'^agente/criar_agente/$', AgenteCreateView.as_view(), name='agente_create_view'),
    url(r'^agente/update_agente/(?P<pk>\w+)/$', AgenteUpdateView.as_view(), name='agente_update_view'),
    url(r'^agente/agente_session/(?P<pk>\w+)/$', AgenteSessionView.as_view(), name='agente_session_view'),
    url(r'^agente/delete_agente/(?P<pk>\w+)/$', AgenteDeleteView.as_view(), name='agente_delete_view',),
    
    #urls para comportamentos
    
    # deleção de compotamento
    url(r'^agente/delete_comportamento/(?P<pk>\w+)/$', ComportamentoOldDeleteView.as_view(), name='comportamento_delete_view'),
     
    #agressivo
    url(r'^agente/criar_comportamento_agressivo/$', AgressivoCreateView.as_view(), name='agressivo_create_view'),
    url(r'^agente/update_comportamento_agressivo/(?P<pk>\w+)/$',AgressivoUpdateView.as_view(), name='agressivo_update_view'),
    
    #passivo
    url(r'^agente/criar_comportamento_passivo/$', PassivoCreateView.as_view(), name='passivo_create_view'),
    url(r'^agente/update_comportamento_passivo/(?P<pk>\w+)/$',PassivoUpdateView.as_view(), name='passivo_update_view'),
    
    #colaborativo
    url(r'^agente/create_comportamento_colaborativo/$',ColaborativoCreateView.as_view(), name='colaborativo_create_view'),
    url(r'^agente/update_comportamento_colaborativo/(?P<pk>\w+)/$',ColaborativoUpdateView.as_view(), name='colaborativo_update_view'),
    
    #colaborativo
    url(r'^agente/create_comportamento_competitivo/$',CompetitivoCreateView.as_view(), name='competitivo_create_view'),
    url(r'^agente/update_comportamento_competitivo/(?P<pk>\w+)/$',CompetitivoUpdateView.as_view(), name='competitivo_update_view'),
    
    
    #urls para add instancias com mensagens
    url(r'^agente/add_instance_agente/$',InstanciasCreateView.as_view(), name='instance_create_view'),
    url(r'^agente/list_instance_agente/$',ListInstances.as_view(), name='instance_list_view'),
    url(r'^agente/update_instance_agente/(?P<pk>\w+)/$',InstanciasUpdateView.as_view(), name='instance_comportamento_update_view'),
    
    
    
    
)