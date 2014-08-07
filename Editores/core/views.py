# -*- coding: utf-8 -*-
# encoding: utf-8
'''
Created on 17/09/2013

@author: Roberto

Convenção: NomeDaClasseAçao - TipoObjetoCreateView
'''

# from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core import serializers
from django.core.context_processors import request
from django.http import HttpResponse
from core.ajax import AjaxableResponseMixin

# imports para objeto, tipos de objetos, icones utilizados no momento de autoria, instancias dos objetos.
# Also, imports para posições geográficas que as instâncias possuem, bem como a sugestão e o tipo de imagem
from editores.models import Objeto, TipoObjeto, Icone, Aventura, InstanciaObjeto, PosicaoGeografica, Sugestao, TipoImagem, \
    Jogador

# impost para Enredo, criação de missões e tipos de condições que compoõem missões
from editores.models import Missao, Condicao, CondicaoDialogoInstancia, CondicaoJogadorInstancia, CondicaoJogadorObjeto, CondicaoInstanciaObjeto

from editores.models import Enredo, EnredoFile, EnredoInstancia, EnredoMensagem

# imports para avatar e criação de agentes com seus tipos de comportamentps
from editores.models import Avatar, Agente, Agressivo, Comportamento, Passivo, Colaborativo, Mensagem, Competitivo

from editores.models import AventuraAtiva, CondicaoAtiva, MissaoAtiva, PosInstanciaAtiva, AvatarAtivo

from forms import PosInstanciaAtivaCreateForm, AvatarAtivoCreateForm, MissaoAtivaCreateForm, CondicaoAtivaCreateForm

from forms import AventuraForm, AventuraWithoutFieldsForm, AvatarRoleListForm, InstanciaObjetoCreateForm 
from forms import PosicaoGeograficaCreateForm, InstanciaObjetoUpdateForm, UpdateObjetoForm, CreateMissaoForm, CreateAvatarForm
from forms import CondicaoInstanciaObjetoForm, CondicaoDialogoInstanciaForm, CondicaoJogadorInstanciaForm, AgenteCreateForm
from forms import AgenteWithoutFieldsForm, AgressivoCreateForm, PassivoCreateForm, ColaborativoCreateForm, InstancesComportamentoAddForm, CompetitivoCreateForm
from forms import EnredoFileForm, EnredoInstanciaForm, EnredoMensagemForm, CondicaoJogadorObjetoForm, AventuraAtivaWithoutFieldsForm

from forms import AventuraAutoriaEstadoForm

from itertools import chain

import string, random

from django import template
from rest_framework.urls import template_name
 
register = template.Library()

import os
import json


SESSION_AVENTURA = '_user_aventura_id'

# assumindo que a criação de aventuras não seja colaborativa
SESSION_INSTANCIA = '_instancia_aventura'
SESSION_AGENTE = '_instancia_agente'
SESSION_TYPE_BEHAVIOR = '_type_behavior'
SESSION_AVENTURA_AUTORIA = '_aventura_autoria'


'''
===================================================================
                    Views para Tipo de Objeto
===================================================================
'''
# Listagem dos tipos de objetos
class TipoObjetoListView(ListView):
    model = TipoObjeto
    template_name = 'editor_objetos/tipo_objeto/listar.html'

# Criação do tipo de objeto
class TipoObjetoCreateView(CreateView):
    template_name = 'editor_objetos/tipo_objeto/create.html'
    model = TipoObjeto
   
    # redireciona a requisição
    def get_success_url(self):
        return reverse('tipo_objeto_list_view')
    
    # Override no form
    def form_valid(self, form):
        self.object = form.save()    
        # json.dumps() transforma objeto em string JSON e, json.loads() transforma string JSON em objeto    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
   
# Atualização de um tipo de objeto
class TipoObjetoUpdateView(UpdateView):
    template_name = 'editor_objetos/tipo_objeto/update.html'
    model = TipoObjeto
    
    def get_success_url(self):
        return reverse('tipo_objeto_list_view')
    
    # Override no form. 
    def form_valid(self, form):
        self.object = form.save()      
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

# Deleção do tipo de objeto
class TipoObjetoDeleteView(DeleteView):
    template_name = 'editor_objetos/tipo_objeto/delete.html'
    model = TipoObjeto
     
    # Override no método delete para evitar o delete em cascata
    # Anteriormente quando um Tipo de Objeto era deletado, todos os... 
    # ...ojetos desse tipo também eram deletados, pois o django por padrão configura o DB em cascate.
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ValidationError as e:
            messages.error(request, "".join(e.messages))
            return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
        # return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('tipo_objeto_list_view')  


# Retorna uma lista de tipos de objetos contendo o id do tipo e o tipo, em json
class TipoObjetoGetJsonView(ListView):
    model = TipoObjeto

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(serializers.serialize('json', TipoObjeto.objects.all(), fields=('pk', 'tipo')))


'''
===================================================================
                    Views para o Icone 
                    
Icone- é a imagem do objeto no momento da autoria.
===================================================================
'''
# Listagem dos icones
class IconeListView(ListView): 
    model = Icone
    template_name = 'editor_objetos/icones/listar.html'

# Criação do icone
class IconeCreateView(CreateView):
    template_name = 'editor_objetos/icones/create.html'
    model = Icone
    
    def get_success_url(self):
        return reverse('icone_list_view')  
    
    # Override no form. 
    def form_valid(self, form):
        self.object = form.save()    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
    # def upload_pic
    # form_valid(self, request):
    #    icone = request.
    #    if icone:
    #        if  icone._size > 4*1024*1024:
    #            raise ValidationError("O ícone não deve ultrapassar o tamanho de  4mb!")
    #        return icone
    #    else:
    #        raise ValidationError("Não foi possível ler o ícone carregado")

# Atualização de um icone
class IconeUpdateView(UpdateView):  # não entendi pq havia usado herança multipla aqui. Não é necessário
    template_name = 'editor_objetos/icones/update.html'
    model = Icone
         
    def get_success_url(self):
        return reverse('icone_list_view')
    
    # Override no form. 
    def form_valid(self, form):
        # self.object = form.save()    
        self.object.save()
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

# Deleção do icone
class IconeDeleteView(DeleteView):
    template_name = 'editor_objetos/icones/delete.html'
    model = Icone
     
    # Override no método delete para evitar o deletar em cascata
    # Se algum objeto estiver referênciando o icone, não será possivel deletar o mesmo.
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ValidationError as e:
            messages.error(request, "".join(e.messages))
            return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

# Retorna a url do icone 
class IconeGetJsonView(ListView):
    model = Icone

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(serializers.serialize('json', Icone.objects.all().filter(pk=self.kwargs['pk']), fields=('icone')))


'''
===================================================================
                    Views para Objeto
Objeto - objeto aqui não tem relação com OO. Objeto são "Things"
         para o jogo.
===================================================================
'''
# Listagem dos objetos
class ObjetoListView(ListView):
    model = Objeto
    template_name = 'editor_objetos/objeto/listar.html'

# Criação de objetos
class ObjetoCreateView(CreateView):
    template_name = 'editor_objetos/objeto/create.html'
    model = Objeto
    form_class = UpdateObjetoForm
    
    def get_success_url(self):
        return reverse('objeto_list_view')
    
    # Override no form. 
    def form_valid(self, form):
        self.object = form.save()    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
   
# atualização de um objeto especifico  
class ObjetoUpdateView(UpdateView): 
    template_name = 'editor_objetos/objeto/update.html'
    model = Objeto
    form_class = UpdateObjetoForm

    # def get_object(self):
    #    return Objeto.objects.get(pk=self.request.GET.get('pk'))
    
    def form_valid(self, form):
        self.object = form.save()    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
    def get_success_url(self):
        return reverse('objeto_list_view')
    
# Deleção de objeto
class ObjetoDeleteView(DeleteView):
    template_name = 'editor_objetos/objeto/delete.html'
    model = Objeto

    # Override no delete para retornar uma resposta json caso o objeto seja deletado com sucesso
    def delete(self, request, *args, **kwargs):
        
        object_list = InstanciaObjeto.objects.all().filter(objeto_id=self.kwargs['pk'])
        self.object = self.get_object()

        if not object_list:   
            self.object.delete()
        else:
            ValidationError
            messages.error(request, "".join("Não é possível deletar o objeto " + self.object.nome) + ", pois existem instâncias deste objeto!")
            return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
    def get_success_url(self):
        return reverse('objeto_list_view')  


# Retorna uma lista contento o id e nome do objeto,  e id do seu icone
class ObjetoGetJsonView(ListView):
    model = Objeto

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(serializers.serialize('json', Objeto.objects.all().filter(tipo_objeto=self.kwargs['pk']), fields=('pk', 'nome', 'icone_objeto', 'dialogo',)))
    

'''
================================================================================
                          Views para Instância do Objeto
                    
Instância do Objeto é criada no momento em que o objeto é arrastado para o mapa.
=================================================================================
'''

# cria a instancia do objeto por meio de um POST com json
class InstanciaObjetoCreateView(AjaxableResponseMixin, CreateView):  
    # template_name = 'editor_objetos/instancia_objeto/create.html'
    model = InstanciaObjeto
    form_class = InstanciaObjetoCreateForm
    
    def get_success_url(self):
        return reverse('gmaps_view') 
    
    def form_valid(self, form, *args, **kwargs):
       
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).,
        # json print self.request.body
        pos = json.loads(self.request.body)  # get json post
        # recupera quantidade do objeto
        object_list = Objeto.objects.all().filter(pk=pos[0]['id_objeto'])
        
        qntde = 0
        id_tipo = 0
        # recupera quantidade
        for obj in object_list:  # always return one object, because the id/pk is unique
            qntde = obj.quantidade
            id_tipo = obj.tipo_objeto_id
        # utilizado no if de comparacao a seguir
        # usa id_objeto e id_aventura para recuperar instâncias do objeto
        # em seguida verifica a instancia com maior instancia_cont e verifica se é possível criar uma nova instância.
        # recupero instancias do objeto de uma dada aventura
        object_list = InstanciaObjeto.objects.all().filter(aventura_id=self.request.session[SESSION_AVENTURA].id, objeto_id=pos[0]['id_objeto'])
        flag = False  # permissão para criar outra instancia
        
        # permissao para criar mais instancias
        # qntde_new_inst_obj = 0
        # if not  object_list:
        #    qntde_new_inst_obj = 1
        # else:
        #    for obj in object_list:
        #        if obj.instancia_cont == int(qntde):
        #            flag = True
        #        if obj.instancia_cont >= qntde_new_inst_obj:
        #            qntde_new_inst_obj = obj.instancia_cont + 1;
        
        # calcula a quantidade de instancias
        qnt_total_instancias = 0;
        for obj in object_list:
            qnt_total_instancias += 1;
            
        if qnt_total_instancias >= int(qntde):
            flag = True
            
        
        # salva objeto
        data_return = {'pk': 0, }
        if flag == False:
            form.instance.nome = pos[0]['nome']
            form.instance.objeto_id = pos[0]['id_objeto']
            form.instance.aventura_id = self.request.session[SESSION_AVENTURA].id
            # form.instance.instancia_cont = qntde_new_inst_obj
            self.object = form.save()
            response = super(AjaxableResponseMixin, self).form_valid(form)
            
            object_list = TipoObjeto.objects.all().filter(pk=id_tipo)
           
            qntde_pos = 1
            for obj in object_list:
                qntde_pos = obj.posicoes_geograficas
               
            data_return = {'pk': self.object.id, 'qntde_pos':qntde_pos, }
            
            
        # retorna data com id do objeto
        if self.request.is_ajax():
            return self.render_to_json_response(data_return)
        else:
            return response  
    
class InstanciaObjetoGetJsonView(ListView):
    model = InstanciaObjeto

    # funcao que retorna todas instâncias de objetos de uma dada aventura, com um campo adiciona com a url do icone (json)
    def render_to_response(self, context, **response_kwargs):
        
        # recupero instancias de uma dada aventura
        flag = 0;
        flagTwo = 0;
        inst_object_list = InstanciaObjeto.objects.all().filter(aventura_id=self.kwargs['pk'])  # id e nome
        json_inst_objetos = '[';
        # qntde_pos = 0;
        json_inst_pos = '';
        for inst_obj in inst_object_list:     
            # inst_object_list = InstanciaObjeto.objects.all().filter(aventura_id=self.kwargs['pk'])
            # objeto_list = Objeto.objects.all().filter(pk=inst_obj.objeto_id)#icone_objeto_id
            if flag == 0:
                flag = 1;
                json_inst_objetos += '{"id":"' + str(inst_obj.pk) + '"' + ',"nome":"' + inst_obj.nome + '"';  # id e nome da instancia
            else:
                json_inst_objetos += ',{"id":"' + str(inst_obj.pk) + '"' + ',"nome":"' + inst_obj.nome + '"';  # id e nome da instancia
            objeto_list = Objeto.objects.all().filter(pk=inst_obj.objeto_id)  # icone_objeto_id
            pos_list = PosicaoGeografica.objects.all().filter(instancia_objeto_id=inst_obj.pk)
            for obj in objeto_list:
                icone_list = Icone.objects.all().filter(pk=obj.icone_objeto_id)
                for icone in  icone_list:
                    json_inst_objetos += ',"url_icone":"/media/' + str(icone.icone) + '"';
                tipo_list = TipoObjeto.objects.all().filter(pk=obj.tipo_objeto_id)
                for tipo in tipo_list:
                    json_inst_pos += ',"posicoes_geograficas":"' + str(tipo.posicoes_geograficas) + '"';
            # for pos in pos_list:
            #    qntde_pos = qntde_pos+1;
            json_inst_pos += ',"pos":[';
            for pos in pos_list:
                if flagTwo == 0:
                    flagTwo = 1;
                    # json_inst_pos += "{'lat':'" + str(pos.latitude) + "'" + ",'lng':'" +str(pos.longitude) + "'"+  ",'altd':'" + str(pos.altitude) + "'}"; 
                    json_inst_pos += '{"id_pos":"' + str(pos.pk) + '"' + ',"lat":"' + str(pos.latitude) + '"' + ',"lng":"' + str(pos.longitude) + '"' + ',"altd":"' + str(pos.altitude) + '"}';    
                else:
                    json_inst_pos += ',{"id_pos":"' + str(pos.pk) + '"' + ',"lat":"' + str(pos.latitude) + '"' + ',"lng":"' + str(pos.longitude) + '"' + ',"altd":"' + str(pos.altitude) + '"}';      
            json_inst_pos += ']}';
            json_inst_objetos += str(json_inst_pos);  # "}"
            json_inst_pos = "";
            flagTwo = 0;
             
        
        json_inst_objetos += ']';
        
        print "Instâncias de Objetos em JSON"
        print json_inst_objetos
        
        return HttpResponse(json_inst_objetos)

# Pendencia: validacao manua do form.
class InstanciaObjetoUpdateView(UpdateView):
    template_name = 'editor_objetos/instancia_objeto/update.html'
    model = InstanciaObjeto
    form_class = InstanciaObjetoUpdateForm
    # success_url = "success-url"
    
    # def get_object(self):
    #    return Objeto.objects.get(pk=self.request.GET.get('pk'))
    # def get_success_url(self):
    #    return reverse('gmaps_view')
    
    def form_valid(self, form):
        print str(form)
        self.object = form.save()  
        # return HttpResponseRedirect(self.get_success_url())
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
class InstanciaObjetoDeleteView(DeleteView):
    # template_name = 'editor_objetos/instancia_objeto/update.html'
    model = InstanciaObjeto;
    
    # Override no delete para retornar uma resposta json caso o objeto seja deletado com sucesso
    def delete(self, request, *args, **kwargs):
 
        
        self.object = self.get_object()

        # if not object_list:   
        self.object.delete()
        # else:
        #    ValidationError
        #    messages.error(request, "".join("Não é possível deletar o objeto " + self.object.nome) + ", pois existem instâncias deste objeto!")
        #    return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
    
        return HttpResponse(json.dumps({'response': 'delete'}), content_type="application/json")
    
        # def get_success_url(self):
        #    return reverse('gmaps_view') 
    
'''
================================================================================
                          Views para Posicao Geografica
=================================================================================
'''

# Cria a posição geográfica para o objeto
class PosicaoGeograficaCreateView(AjaxableResponseMixin, CreateView):  
    # template_name = 'editor_objetos/instancia_objeto/create.html'
    model = PosicaoGeografica
    form_class = PosicaoGeograficaCreateForm
    
    def get_success_url(self):
        return reverse('gmaps_view') 

    
    def form_valid(self, form, *args, **kwargs):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).,
        # json print self.request.body
        pos = json.loads(self.request.body)
        form.instance.latitude = pos[0]['latitude']
        form.instance.longitude = pos[0]['longitude']
        form.instance.instancia_objeto_id = pos[0]['instancia_objeto_id']
        form.instance.altitude = pos[0]['altitude']
        self.object = form.save()
        response = super(AjaxableResponseMixin, self).form_valid(form)
            
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response 

# Atualiza a posicao geográfica do objeto
class PosicaoGeograficaUpdateView(AjaxableResponseMixin, UpdateView):  
    # template_name = 'editor_objetos/instancia_objeto/create.html'
    model = PosicaoGeografica
    form_class = PosicaoGeograficaCreateForm
    
    def get_success_url(self):
        return reverse('gmaps_view') 

    
    def form_valid(self, form, *args, **kwargs):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).,
        # json print self.request.body
        pos = json.loads(self.request.body)

        form.instance.latitude = pos[0]['latitude']
        form.instance.longitude = pos[0]['longitude']
        # form.instance.instancia_objeto_id = pos[0]['instancia_objeto_id']
        form.instance.altitude = pos[0]['altitude']
        self.object = form.save()
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response    
        
# Retorna json contendo dados da posicao de uma instância, ou conjunto de posicoes
class PosicaoGeograficaGetJsonView(ListView):
    model = PosicaoGeografica
    
    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(serializers.serialize('json', PosicaoGeografica.objects.all().filter(instancia_objeto_id=self.kwargs['pk'])))  # utiliza o id da instância

# delete posicao geográfica de um marcador
class PosicaoGeograficaDeleteView(DeleteView):
    model = PosicaoGeografica;
    
    def delete(self, request, *args, **kwargs):
 
        self.object = self.get_object()
        # verifica a quantidade de marcadores da instância.
        # caso a quantidade seja <= 1 a instância também é deletada.

        objetct_markers_list = PosicaoGeografica.objects.all().filter(instancia_objeto_id=self.object.instancia_objeto_id)
        
        qnde_markers = 0;
        for obj in objetct_markers_list:
            qnde_markers = qnde_markers + 1;
            
        data = 0;
        if qnde_markers <= 1:
            data = 1;
        # objetct_instance_list = InstanciaObjeto.objects.all().filter(pk=)
        
       
        self.object.delete()
   
        return HttpResponse(json.dumps({'response': data}), content_type="application/json")
    
'''
====================================================================
                        Views para GMapView
====================================================================                   

'''
class GMapView(TemplateView):
    template_name = 'editor_objetos/gmap/gmap.html'
 
# abre modal para informar ao usuário que a posição da aventura foi salva com sucesso   
class MsgShowView(TemplateView):
    template_name = 'editor_objetos/gmap/pos_aventura.html'
    
    # def get_success_url(self):
        # return HttpResponseRedirect(self.get_success_url())
        # return HttpResponse(json.dumps({'response' : 'ok'}), content_type="application/json")
    
''''
====================================================================
                        Views para Aventura
====================================================================
'''
    
# atualiza o estado de autoria de uma aventura - completo ou incompleto para que a mesma possa ser publicada
class AventuraAutoriaEstadoUpdateView(UpdateView):
    template_name = 'editor_aventuras/aventura/autoria_estado_update.html'
    model = Aventura
    form_class = AventuraAutoriaEstadoForm
    
    def get_success_url(self):
        return reverse('aventura_list_view')
    
    # Override no form. 
    def form_valid(self, form):
        # form.instance.autor_id = self.kwargs['pk']

        self.object = form.save()    
        
        #atualiza objeto na session
        self.request.session[SESSION_AVENTURA].autoria_estado =  self.object.autoria_estado
        #copia dados da aventura
        nome = self.request.session[SESSION_AVENTURA].nome
        id_av = self.request.session[SESSION_AVENTURA].id
       
        if self.request.session[SESSION_AVENTURA].autoria_estado == 'AC':
            autoria_estado = "Completa"
        else:
            autoria_estado = "Em construção"
        return HttpResponse(json.dumps({'nome': nome , 'id' : id_av, 'autoria_estado': autoria_estado }), content_type="application/json")
    
# Listagem da aventura
class AventuraListView(ListView):
    model = Aventura
    template_name = 'editor_aventuras/aventura/listar.html' 
        
    def get_context_data(self, **kwargs):
        context = super(AventuraListView, self).get_context_data(**kwargs)
        if self.request.session[SESSION_AVENTURA] != '-1':
            context['aventura_autoria'] = self.request.session[SESSION_AVENTURA].id
        else:
            context['aventura_autoria'] = '-1'
        
        context['object_list'] = Aventura.objects.all().filter(autor=self.kwargs['pk'])
       
        # print self.request.session[SESSION_AVENTURA]
        return context

# Criação das aventuras
class AventuraCreateView(CreateView):
    template_name = 'editor_aventuras/aventura/create.html'
    model = Aventura
    form_class = AventuraForm
    
    def get_success_url(self):
        return reverse('aventura_list_view')
    
    # Override no form. 
    def form_valid(self, form):
        form.instance.autor_id = self.kwargs['pk']
        self.object = form.save()    
        return HttpResponse(json.dumps({'response' : 'ok'}), content_type="application/json")

# Atualização de uma aventura
class AventuraUpdateView(UpdateView):
    template_name = 'editor_aventuras/aventura/update.html'
    model = Aventura
    form_class = AventuraForm
    
    def get_success_url(self):
        return reverse('aventura_list_view')
    
    # Override no form. 
    def form_valid(self, form):
        self.object = form.save()   
        # atualiza sessao
        self.request.session[SESSION_AVENTURA] = self.object
        
        nome = self.request.session[SESSION_AVENTURA].nome
        id_av = self.request.session[SESSION_AVENTURA].id
        if self.request.session[SESSION_AVENTURA].autoria_estado == 'AC':
            autoria_estado = "Autoria Completa"
        else:
            autoria_estado = "Autoria Incompleta"
        return HttpResponse(json.dumps({'response': nome , 'id' : id_av, 'autoria_estado':autoria_estado }), content_type="application/json")

# ativar aventura para autoria
class AventuraAtivarView(UpdateView):
    template_name = 'editor_aventuras/aventura/message.html'
    model = Aventura
    form_class = AventuraWithoutFieldsForm
    
    def get_success_url(self):
        return reverse('aventura_list_view')   

    def form_valid(self, form):
        
        self.request.session[SESSION_AVENTURA] = self.object
        nome = self.request.session[SESSION_AVENTURA].nome
        id_av = self.request.session[SESSION_AVENTURA].id
        if self.request.session[SESSION_AVENTURA].autoria_estado == 'AC':
            autoria_estado = "Autoria Completa"
        else:
            autoria_estado = "Autoria Incompleta"
        if self.request.session[SESSION_AVENTURA] == '-1':
            ValidationError
            messages.error(request, "".join("Ocorreu um problema ao ativar a aventura! Tente novamente!"))
            return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        return HttpResponse(json.dumps({'response': nome , 'id' : id_av, 'autoria_estado':autoria_estado }), content_type="application/json")


class AventuraDesativarView(UpdateView):
    template_name = 'editor_aventuras/aventura/messageDesativar.html'
    model = Aventura
    form_class = AventuraWithoutFieldsForm
    
    def get_success_url(self):
        return reverse('aventura_list_view')   

    def form_valid(self, form):
        
        if self.request.session[SESSION_AVENTURA].id == self.object.id:
            self.request.session[SESSION_AVENTURA] = '-1'  # desativa aventura
            return HttpResponse(json.dumps({'response':'ok'}), content_type="application/json")
        else:
            ValidationError
            messages.error(request, "".join("Está aventura não está ativa!"))
            return HttpResponse(json.dumps({'response': 'exception desativar'}), content_type="text")
        

# Atualizar posição aventura
class AventuraUpdatePositionView(AjaxableResponseMixin, UpdateView):
    # template_name = 'editor_aventuras/aventura/message.html'
    model = Aventura
    form_class = AventuraWithoutFieldsForm
    
    def get_success_url(self):
        return reverse('gmaps_view')

    
    def form_valid(self, form, *args, **kwargs):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).,
        # json print self.request.body
        pos = json.loads(self.request.body)
        form.instance.latitude = pos[0]['latitude']
        form.instance.longitude = pos[0]['longitude']
        self.object = form.save()
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response
    



# Deleção da aventura
class AventuraDeleteView(DeleteView):
    template_name = 'editor_aventuras/aventura/delete.html'
    model = Aventura
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # verifica se a aventura está em autoria
        id_av = ''
        if self.request.session[SESSION_AVENTURA] == '-1':  # sem aventura
            id_av = self.request.session[SESSION_AVENTURA]
        else:
            id_av = self.request.session[SESSION_AVENTURA].id

        if id_av == self.object.id:
            ValidationError
            msg = 'A aventura ' + self.object.nome + ' está em autoria. Para deleção é necessário que a aventura esteja com o modo de autoria desativado.'

            messages.error(request, "".join(msg))
            return HttpResponse(json.dumps({'response': 'ativa'}), content_type="text")
        else:
            try:
                self.object.delete()
            except ValidationError as e:
                messages.error(request, "".join(e.messages))
                return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

    
    
# Retorna json contendo dados da aventura
class AventuraGetJsonView(ListView):
    model = Aventura
    
    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(serializers.serialize('json', Aventura.objects.all().filter(pk=self.kwargs['pk'])))


#############################################################################
#       Views que tratam da instanciacao de uma aventura para ser jogada    #
#############################################################################

# view que lista as aventuras ativas
class AventuraAtivaListView(ListView):
    model = AventuraAtiva
    template_name = 'editor_aventuras/aventura/listar_aventuras_ativas.html'
    
    def get_queryset(self):
        if self.request.session[SESSION_AVENTURA] != '-1':
            object_list = AventuraAtiva.objects.all().filter(aventura_id=self.request.session[SESSION_AVENTURA].id)
        else:  
            object_list = AventuraAtiva.objects.all().filter(aventura_id='-1')  # sem aventuras ativas
            
        return object_list
    
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
# ativação da aventura para ser jogada
class AtivarAventuraView(CreateView):
    template_name = 'editor_aventuras/aventura/ativar_aventura.html' 
    model = AventuraAtiva
    form_class = AventuraAtivaWithoutFieldsForm
    
    def get_success_url(self):
        return reverse('aventuras_ativas_list_view')
    
    
    def get_initial(self):
        initial = super(AtivarAventuraView, self).get_initial()
        initial['request'] = self.request
        if self.request.session[SESSION_AVENTURA] != '-1':
            initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
            initial['autoria_estado'] = self.request.session[SESSION_AVENTURA].autoria_estado
        else:
            initial['aventura_id'] = self.request.session[SESSION_AVENTURA]
        return initial
    
    # Override no form. 
    def form_valid(self, form):
        
        
        # Aventura só pode ser ativada se estiver em modo de autoria
        if self.request.session[SESSION_AVENTURA] != '-1':
            if self.request.session[SESSION_AVENTURA].autoria_estado == 'AC':
            
                # verificando quantidade de aventuras ativas
                flag = 1
                object_list = AventuraAtiva.objects.all().filter(aventura_id=self.request.session[SESSION_AVENTURA].id)
                for obj in object_list:
                    flag = flag + 1
                    
                # gerando chave de acesso
                if form.instance.publica == False:
                    form.instance.chave_acesso = id_generator()
                    
                form.instance.aventura_id = self.request.session[SESSION_AVENTURA].id
                
                form.instance.instancia = flag
               
                # ativando aventura
                self.object = form.save()  
                # recuperando id da aventura ativada
                aventura_ativa_id = self.object.pk
               
               
                # recuperando dados da aventura que está sendo ativa
                instancias = InstanciaObjeto.objects.all().filter(aventura_id=self.request.session[SESSION_AVENTURA].id)
                
                posicoes_instancias = ''
                flag = 0
                for obj in instancias:
                    if flag == 0:
                        posicoes_instancias = PosicaoGeografica.objects.all().filter(instancia_objeto_id=obj.id)
                        flag = 1
                    elif flag == 1:
                        posicoes_instancias = posicoes_instancias | PosicaoGeografica.objects.all().filter(instancia_objeto_id=obj.id)
                        
                avatares = Avatar.objects.all().filter(aventura_avatar_id=self.request.session[SESSION_AVENTURA].id)
                
                missoes = Missao.objects.all().filter(aventuras_id=self.request.session[SESSION_AVENTURA].id)
                
                
                
                flag = 0
                condicoes = ''
                for obj in missoes:
                    if flag == 0:
                        condicoes = Condicao.objects.all().filter(missao_id=obj.id)
                        flag = 1
                    elif flag == 1:
                        condicoes = condicoes | Condicao.objects.all().filter(missao_id=obj.id)
              
    
                json_instancias = '{"aventura_ativa_id":"' + str(aventura_ativa_id) + '","PosInstanciaAtiva":['
                
                flag = 0
                for obj in posicoes_instancias:
                    if flag == 0:
                        json_instancias = json_instancias + ' {"instancia_id":' + '"' + str(obj.instancia_objeto_id) + '",'
                        json_instancias = json_instancias + ' "lat":' + '"' + str(obj.latitude) + '",'
                        json_instancias = json_instancias + ' "log":' + '"' + str(obj.longitude) + '",'
                        json_instancias = json_instancias + ' "alt":' + '"' + str(obj.altitude) + '"}'
                        flag = 1
                    elif flag == 1:
                        json_instancias = json_instancias + ',{"instancia_id":' + '"' + str(obj.instancia_objeto_id) + '",'
                        json_instancias = json_instancias + ' "lat":' + '"' + str(obj.latitude) + '",'
                        json_instancias = json_instancias + ' "log":' + '"' + str(obj.longitude) + '",'
                        json_instancias = json_instancias + ' "alt":' + '"' + str(obj.altitude) + '"}'
                        
                json_instancias = json_instancias + ']}'
                
                json_avatares = '{"aventura_ativa_id":"' + str(aventura_ativa_id) + '","AvatarAtivo":['
                flag = 0
                for obj in avatares:
                    if flag == 0:
                        json_avatares = json_avatares + ' {"avatar_id":' + '"' + str(obj.id) + '"}'
                        flag = 1
                    elif flag == 1:
                        json_avatares = json_avatares + ',{"avatar_id":' + '"' + str(obj.id) + '"}'
                
                json_avatares = json_avatares + ']}'
                
                
                json_missoes = '{"aventura_ativa_id":"' + str(aventura_ativa_id) + '","MissaoAtiva":['
                flag = 0
                for obj in missoes:
                    if flag == 0:
                        json_missoes = json_missoes + ' {"missao_id":' + '"' + str(obj.id) + '"}'
                        flag = 1
                    elif flag == 1:
                        json_missoes = json_missoes + ',{"missao_id":' + '"' + str(obj.id) + '"}'
                
                json_missoes = json_missoes + ']}'
                
                
                json_condicoes = '{"aventura_ativa_id":"' + str(aventura_ativa_id) + '","CondicaoAtiva":['
                flag = 0
                if condicoes:
                    for obj in condicoes:
                        if flag == 0:
                            json_condicoes = json_condicoes + ' {"condicao_id":' + '"' + str(obj.id) + '",'
                            json_condicoes = json_condicoes + ' "missao_id":' + '"' + str(obj.missao_id) + '"}'
                            flag = 1
                        elif flag == 1:
                            json_condicoes = json_condicoes + ',{"condicao_id":' + '"' + str(obj.id) + '",'
                            json_condicoes = json_condicoes + ' "missao_id":' + '"' + str(obj.missao_id) + '"}'
                
                json_condicoes = json_condicoes + ']}'           
            
            return HttpResponse(json.dumps({'PosInstanciaAtiva' : json_instancias, 'AvatarAtivo':json_avatares, 'MissaoAtiva' : json_missoes, 'CondicaoAtiva': json_condicoes}), content_type="application/json")            
        
# ativação da aventura para ser jogada
class AventuraAtivaUpdateView(UpdateView):
    template_name = 'editor_aventuras/aventura/update_aventura_ativa.html' 
    model = AventuraAtiva
    form_class = AventuraAtivaWithoutFieldsForm
    
    def get_success_url(self):
        return reverse('aventuras_ativas_list_view')
    
    def get_initial(self):
        initial = super(AventuraAtivaUpdateView, self).get_initial()
        initial['request'] = self.request
        if self.request.session[SESSION_AVENTURA] != '-1':
            initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        else:
            initial['aventura_id'] = self.request.session[SESSION_AVENTURA]
        return initial
    # Override no form. 
    def form_valid(self, form):
        
        if self.request.session[SESSION_AVENTURA] != '-1':
            
            # verifica se o atributo publico foi alterado    
            if form.instance.publica == True:
                form.instance.chave_acesso = ""
            elif  form.instance.publica == False and form.instance.chave_acesso == "": 
                form.instance.chave_acesso = id_generator() 
            form.instance.aventura_id = self.request.session[SESSION_AVENTURA].id
            
            # ativa aventura
            self.object = form.save()  
   
        return HttpResponse(json.dumps({'response' : 'ok'}), content_type="application/json")

class AventuraAtivaDeleteView(DeleteView):
    template_name = 'editor_aventuras/aventura/delete_aventura_ativa.html' 
    model = AventuraAtiva
    form_class = AventuraAtivaWithoutFieldsForm
    
    def get_success_url(self):
        return reverse('aventuras_ativas_list_view')
    
    def delete(self, request, *args, **kwargs):
        
        
        if self.request.session[SESSION_AVENTURA] != '-1':
            
            object_list = ''
            avatares_ativos = AvatarAtivo.objects.all().filter(aventura_ativa_avatar_id=self.kwargs['pk'],)
            
            flag = 0
            for obj in avatares_ativos:    
                if flag == 0:
                    object_list = Avatar.objects.all().filter(pk=obj.avatar_id,)
                    flag = 1
                elif flag == 1:
                    object_list = object_list | Avatar.objects.all().filter(pk=obj.avatar_id,)
            
            flag = 0
            if object_list:
                for obj in object_list:
                    if str(obj.aventureiro_id) == "None":
                        flag = flag + 1
            else:  # deleção de aventura ativada para testes
                self.object = self.get_object() 
                return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")  
                        
            self.object = self.get_object()

            if flag > 0:   
                self.object.delete()
            else:
                ValidationError
                messages.error(request, "".join("Não é possível deletar a Aventura Ativa, pois existem Jogadores vinculados a mesma!"))
                return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
            return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")


''''
====================================================================
                        Views para Sugestao
====================================================================
'''
# Lista todas sugestões
class SugestaoListView(ListView):
    template_name = 'editor_objetos/sugestao/listar.html'
    model = Sugestao

# criação de sugestão
class SugestaoCreateView(CreateView):
    template_name = 'editor_objetos/sugestao/create.html'
    model = Sugestao
   
    # redireciona a requisição
    def get_success_url(self):
        return reverse('sugestao_list_view')
    
    # Override no form
    def form_valid(self, form):
        # arquivos devem ser txt, jpeg, png ou fbx (extensões de objetos 3D para Wikitude SDK Android para AR)
        tipo = form.cleaned_data['tipo']  # recupera tipo de sugestao
        arquivo = form.cleaned_data['sugestao']  # recupera file
        if arquivo:
            if tipo == 'STX':
                # valida arquivo de texto para salvar sugestao
                if not os.path.splitext(arquivo.name)[1] in [".txt"]:
                    ValidationError
                    msg = "O arquivo deve ser *.txt...."
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                elif not arquivo.content_type == 'text/plain':
                    ValidationError
                    msg = "Não é um arquivo de texto válido!"
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
            elif tipo == 'SAU':
                # valida arquivo de audio para salvar sugestao
                # if not file.content-type in ["audio/mpeg","audio/..."]:
                if not os.path.splitext(arquivo.name)[1] in [".mp3"]:
                    ValidationError
                    msg = "O arquivo deve ser *.mp3...."
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                elif not arquivo.content_type == 'audio/mp3':
                    ValidationError
                    msg = "Não é um arquivo de áudio válido!"
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
            elif tipo == 'SIMG':
                # valida imagem para salvar
                if not os.path.splitext(arquivo.name)[1] in [".png", ".jpeg", ".jpg"]:
                    ValidationError
                    msg = "O arquivo deve ser *.png ou *.jpeg...."
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                elif not arquivo.content_type == 'image/png':
                    if not arquivo.content_type == 'image/jpeg':
                        ValidationError
                        msg = "Não é um arquivo de imagem válido!"
                        messages.error(self.request, "".join(msg))
                        return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")

        # file = self.cleaned_data.get('audio_file',False)
        # print file 
        self.object = form.save()   
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

# update sugestao
class SugestaoUpdateView(UpdateView):
    template_name = 'editor_objetos/sugestao/update.html'
    model = Sugestao
    
    # redireciona a requisição
    def get_success_url(self):
        return reverse('sugestao_list_view')
    
    # Override no form
    def form_valid(self, form):
        # arquivos devem ser txt, jpeg, png ou fbx (extensões de objetos 3D para Wikitude SDK Android para AR)
        tipo = form.cleaned_data['tipo']  # recupera tipo de sugestao
        arquivo = form.cleaned_data['sugestao']  # recupera file
        if hasattr(arquivo, "content_type"):
            if tipo == 'STX':
                # valida arquivo de texto para salvar sugestao
                if not os.path.splitext(arquivo.name)[1] in [".txt"]:
                    ValidationError
                    msg = "O arquivo deve ser *.txt...."
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                elif not arquivo.content_type == 'text/plain':
                    ValidationError
                    msg = "Não é um arquivo de texto válido!"
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
            elif tipo == 'SAU':
                # valida arquivo de audio para salvar sugestao
                # if not file.content-type in ["audio/mpeg","audio/..."]:
                if not os.path.splitext(arquivo.name)[1] in [".mp3"]:
                    ValidationError
                    msg = "O arquivo deve ser *.mp3...."
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                elif not arquivo.content_type == 'audio/mp3':
                    ValidationError
                    msg = "Não é um arquivo de áudio válido!"
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
            elif tipo == 'SIMG':
                # valida imagem para salvar
                if not os.path.splitext(arquivo.name)[1] in [".png", ".jpeg", ".jpg"]:
                    ValidationError
                    msg = "O arquivo deve ser *.png ou *.jpeg...."
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                elif not arquivo.content_type == 'image/png':
                    if not arquivo.content_type == 'image/jpeg':
                        ValidationError
                        msg = "Não é um arquivo de imagem válido!"
                        messages.error(self.request, "".join(msg))
                        return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")

        # self.object = form.save() 
        self.object.save()  
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

# delete sugestao
class SugestaoDeleteView(DeleteView):
    template_name = 'editor_objetos/sugestao/delete.html'
    model = Sugestao
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ValidationError as e:
            messages.error(request, "".join(e.messages))
            return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
        # return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('sugestao_list_view') 
    
    
''''
====================================================================
                        Views para TipoImagem
====================================================================
'''
# listagem das imagens
class TipoImagemListView(ListView):
    template_name = 'editor_objetos/tipo_imagem/listar.html'
    model = TipoImagem

    
# create TipoImagem
class TipoImagemCreateView(CreateView):
    template_name = 'editor_objetos/tipo_imagem/create.html'
    model = TipoImagem
    
    # Override no form
    def form_valid(self, form):
        # arquivos devem ser txt, jpeg, png ou fbx (extensões de objetos 3D para Wikitude SDK Android para AR)
        tipo = form.cleaned_data['tipo']  # recupera tipo de imagem
        arquivo = form.cleaned_data['img_play']  # recupera file
        if arquivo:
            if tipo == 'IC':
                if not os.path.splitext(arquivo.name)[1] in [".fbx"]:
                    ValidationError
                    msg = "O arquivo deve ser *.fbx...."
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                elif not arquivo.content_type == 'application/octet-stream':
                    ValidationError
                    msg = "Para imagens para serem visualizadas câmera, a mesma deve ser de extensão fbx!"
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
            elif tipo == 'IM':
                if not os.path.splitext(arquivo.name)[1] in [".png", ".jpeg", ".jpg"]:
                    ValidationError
                    msg = "O arquivo deve ser *.png ou *.jpeg...."
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                elif not arquivo.content_type == 'image/png':
                    if not arquivo.content_type == 'image/jpeg':
                        ValidationError
                        msg = "Não é um arquivo de imagem válido!"
                        messages.error(self.request, "".join(msg))
                        return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")

        self.object = form.save()   
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

# atualiza imagem  
class TipoImagemUpdateView(UpdateView):
    template_name = 'editor_objetos/tipo_imagem/update.html'
    model = TipoImagem
    
    def get_success_url(self):
        return reverse('tipo_imagem_list_view')
    
    def form_valid(self, form):
        # arquivos devem ser txt, jpeg, png ou fbx (extensões de objetos 3D para Wikitude SDK Android para AR)
        tipo = form.cleaned_data['tipo']  # recupera tipo de imagem
        arquivo = form.cleaned_data['img_play']  # recupera file
        if hasattr(arquivo, "content_type"):
            if tipo == 'IC':
                if not os.path.splitext(arquivo.name)[1] in [".fbx"]:
                    ValidationError
                    msg = "O arquivo deve ser *.fbx...."
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                elif not arquivo.content_type == 'application/octet-stream':
                    ValidationError
                    msg = "Para imagens para serem visualizadas câmera, a mesma deve ser de extensão fbx!"
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
            elif tipo == 'IM':
                if not os.path.splitext(arquivo.name)[1] in [".png", ".jpeg", ".jpg"]:
                    ValidationError
                    msg = "O arquivo deve ser *.png ou *.jpeg...."
                    messages.error(self.request, "".join(msg))
                    return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                elif not arquivo.content_type == 'image/png':
                    if not arquivo.content_type == 'image/jpeg':
                        ValidationError
                        msg = "Não é um arquivo de imagem válido!"
                        messages.error(self.request, "".join(msg))
                        return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")

        self.object = form.save()   
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

# delete imagem
class TipoImagemDeleteView(DeleteView):
    template_name = 'editor_objetos/tipo_imagem/delete.html'
    model = TipoImagem
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ValidationError as e:
            messages.error(request, "".join(e.messages))
            return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
    def get_success_url(self):
        return reverse('tipo_imagem_list_view') 

   
'''
====================================================================
                        Views para Enredo
====================================================================
'''
# listagem de enredos
class EnredoListView(ListView):
    template_name = 'editor_enredos/enredos/listar.html'
    model = Enredo
    
    def get_queryset(self):
        
        object_list = ''
        if self.request.session[SESSION_AVENTURA] != '-1':
            object_list = Enredo.objects.all().filter(aventura_id=self.request.session[SESSION_AVENTURA].id)
            # for obj in object_list:
                # print obj
        return object_list
    
# listagem de enredos
class EnredoFileListView(ListView):
    template_name = 'editor_enredos/enredos/listar_enredo_file.html'
    model = EnredoFile
    
    def get_queryset(self):
        
        object_list = ''
        if self.request.session[SESSION_AVENTURA] != '-1':
            object_list = EnredoFile.objects.all().filter(aventura_id=self.request.session[SESSION_AVENTURA].id)
            
            print object_list
            
            # object_list = Enredo.objects.all().filter(aventura_id=self.request.session[SESSION_AVENTURA].id)
            
            print object_list
            # for obj in object_list:
                # print obj
        return object_list

# listagem de enredos
class EnredoInstanciaListView(ListView):
    template_name = 'editor_enredos/enredos/listar_enredo_instancia.html'
    model = EnredoInstancia
    
    def get_queryset(self):
        
        object_list = ''
        if self.request.session[SESSION_AVENTURA] != '-1':
            object_list = EnredoInstancia.objects.all().filter(aventura_id=self.request.session[SESSION_AVENTURA].id)
            
            print object_list
            
            # object_list = Enredo.objects.all().filter(aventura_id=self.request.session[SESSION_AVENTURA].id)
            
            print object_list
            # for obj in object_list:
                # print obj
        return object_list

# listagem de enredos
class EnredoMessageListView(ListView):
    template_name = 'editor_enredos/enredos/listar_enredo_mensagem.html'
    model = EnredoMensagem
    
    def get_queryset(self):
        
        object_list = ''
        if self.request.session[SESSION_AVENTURA] != '-1':
            object_list = EnredoMensagem.objects.all().filter(aventura_id=self.request.session[SESSION_AVENTURA].id)
            
            print object_list
            
            # object_list = Enredo.objects.all().filter(aventura_id=self.request.session[SESSION_AVENTURA].id)
            
            print object_list
            # for obj in object_list:
                # print obj
        return object_list

# create EnredoFile
class EnredoFileCreateView(CreateView):
    template_name = 'editor_enredos/enredos/create_enredo_file.html'
    model = EnredoFile
    form_class = EnredoFileForm
    
    # Override no form
    def form_valid(self, form):
        
        if self.request.session[SESSION_AVENTURA] != '-1':
            
            # arquivos devem ser txt, jpeg, png ou fbx (extensões de objetos 3D para Wikitude SDK Android para AR)
            tipo = form.cleaned_data['tipo']  # recupera tipo de imagem
            arquivo = form.cleaned_data['enredo_file']  # recupera file
            if arquivo:
                if tipo == 'SAU':
                # valida arquivo de audio para salvar sugestao
                # if not file.content-type in ["audio/mpeg","audio/..."]:
                    if not os.path.splitext(arquivo.name)[1] in [".mp3"]:
                        ValidationError
                        msg = "O arquivo deve ser *.mp3...."
                        messages.error(self.request, "".join(msg))
                        return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                    elif not arquivo.content_type == 'audio/mp3':
                        ValidationError
                        msg = "Não é um arquivo de áudio válido!"
                        messages.error(self.request, "".join(msg))
                        return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                if tipo == 'IMGC':
                    if not os.path.splitext(arquivo.name)[1] in [".fbx"]:
                        ValidationError
                        msg = "O arquivo deve ser *.fbx...."
                        messages.error(self.request, "".join(msg))
                        return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                    elif not arquivo.content_type == 'application/octet-stream':
                        ValidationError
                        msg = "Imagens para serem visualizadas câmera, a mesma deve ser de extensão fbx!"
                        messages.error(self.request, "".join(msg))
                        return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                elif tipo == 'IMGM':
                    if not os.path.splitext(arquivo.name)[1] in [".png", ".jpeg", ".jpg"]:
                        ValidationError
                        msg = "O arquivo deve ser *.png ou *.jpeg...."
                        messages.error(self.request, "".join(msg))
                        return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                    elif not arquivo.content_type == 'image/png':
                        if not arquivo.content_type == 'image/jpeg':
                            ValidationError
                            msg = "Não é um arquivo de imagem válido!"
                            messages.error(self.request, "".join(msg))
                            return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                    
            # add id da aventura no enredo
            form.instance.aventura_id = self.request.session[SESSION_AVENTURA].id
            print form.instance
            self.object = form.save()   
            return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
        
        else:
            ValidationError
            msg = "Please. Activate an adventure for authoring!"
            messages.error(self.request, "".join(msg))
            return HttpResponse(json.dumps({'response': 'exception created'}), content_type="application/json")
            
            
class EnredoInstanciaCreateView(CreateView):
    template_name = 'editor_enredos/enredos/create_enredo_instancia.html'
    model = EnredoInstancia
    form_class = EnredoInstanciaForm
    
    
    def get_initial(self):
        initial = super(EnredoInstanciaCreateView, self).get_initial()
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial
    # Override no form
    def form_valid(self, form):
        
        if self.request.session[SESSION_AVENTURA] != '-1':
            
         
            # add id da aventura no enredo
            form.instance.aventura_id = self.request.session[SESSION_AVENTURA].id
            self.object = form.save()   
            return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
        
        else:
            ValidationError
            msg = "Please. Activate an adventure for authoring!"
            messages.error(self.request, "".join(msg))
            return HttpResponse(json.dumps({'response': 'exception created'}), content_type="application/json")

class EnredoMensagemCreateView(CreateView):
    template_name = 'editor_enredos/enredos/create_enredo_mensagem.html'
    model = EnredoMensagem
    form_class = EnredoMensagemForm
    
    # Override no form
    def form_valid(self, form):
        
        if self.request.session[SESSION_AVENTURA] != '-1':
            
            # add id da aventura no enredo
            form.instance.aventura_id = self.request.session[SESSION_AVENTURA].id
            self.object = form.save()   
            return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
        
        else:
            ValidationError
            msg = "Please. Activate an adventure for authoring!"
            messages.error(self.request, "".join(msg))
            return HttpResponse(json.dumps({'response': 'exception created'}), content_type="application/json")   
              
class  EnredoFileUpdateView(UpdateView):
    template_name = 'editor_enredos/enredos/update_enredo_file.html'
    model = EnredoFile  
    form_class = EnredoFileForm
    
    def get_success_url(self):
        return reverse('enredo_file_list_view')
    
    # Override no form
    def form_valid(self, form):
        
        if self.request.session[SESSION_AVENTURA] != '-1':
            
            # arquivos devem ser txt, jpeg, png ou fbx (extensões de objetos 3D para Wikitude SDK Android para AR)
            tipo = form.cleaned_data['tipo']  # recupera tipo de imagem
            arquivo = form.cleaned_data['enredo_file']  # recupera file

            if arquivo:
                if hasattr(arquivo, "content_type"):
                    if tipo == 'SAU':
                    # valida arquivo de audio para salvar sugestao
                    # if not file.content-type in ["audio/mpeg","audio/..."]:
                        if not os.path.splitext(arquivo.name)[1] in [".mp3"]:
                            ValidationError
                            msg = "O arquivo deve ser *.mp3...."
                            messages.error(self.request, "".join(msg))
                            return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                        elif not arquivo.content_type == 'audio/mp3':
                            ValidationError
                            msg = "Não é um arquivo de áudio válido!"
                            messages.error(self.request, "".join(msg))
                            return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                    if tipo == 'IMGC':
                        if not os.path.splitext(arquivo.name)[1] in [".fbx"]:
                            ValidationError
                            msg = "O arquivo deve ser *.fbx...."
                            messages.error(self.request, "".join(msg))
                            return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                        elif not arquivo.content_type == 'application/octet-stream':
                            ValidationError
                            msg = "Imagens para serem visualizadas câmera, a mesma deve ser de extensão fbx!"
                            messages.error(self.request, "".join(msg))
                            return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                    elif tipo == 'IMGM':
                        if not os.path.splitext(arquivo.name)[1] in [".png", ".jpeg", ".jpg"]:
                            ValidationError
                            msg = "O arquivo deve ser *.png ou *.jpeg...."
                            messages.error(self.request, "".join(msg))
                            return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                        elif not arquivo.content_type == 'image/png':
                            if not arquivo.content_type == 'image/jpeg':
                                ValidationError
                                msg = "Não é um arquivo de imagem válido!"
                                messages.error(self.request, "".join(msg))
                                return HttpResponse(json.dumps({'response': 'exception create'}), content_type="text")
                        
                    
            # add id da aventura no enredo
            form.instance.aventura_id = self.request.session[SESSION_AVENTURA].id
            print form.instance
            self.object = form.save()   
            return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
        
        else:
            ValidationError
            msg = "Please. Activate an adventure for authoring!"
            messages.error(self.request, "".join(msg))
            return HttpResponse(json.dumps({'response': 'exception created'}), content_type="application/json")


class EnredoInstanciaUpdateView(UpdateView):
    template_name = 'editor_enredos/enredos/update_enredo_instancia.html'
    model = EnredoInstancia
    form_class = EnredoInstanciaForm
    
    
    def get_initial(self):
        initial = super(EnredoInstanciaUpdateView, self).get_initial()
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial
    # Override no form
    def form_valid(self, form):
        
        if self.request.session[SESSION_AVENTURA] != '-1':
            
            # add id da aventura no enredo
            form.instance.aventura_id = self.request.session[SESSION_AVENTURA].id
            self.object = form.save()   
            return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
        
        else:
            ValidationError
            msg = "Please. Activate an adventure for authoring!"
            messages.error(self.request, "".join(msg))
            return HttpResponse(json.dumps({'response': 'exception created'}), content_type="application/json")


class EnredoMensagemUpdateView(UpdateView):
    template_name = 'editor_enredos/enredos/update_enredo_mensagem.html'
    model = EnredoMensagem
    form_class = EnredoMensagemForm
    
    # Override no form
    def form_valid(self, form):
        
        if self.request.session[SESSION_AVENTURA] != '-1':
            
            # add id da aventura no enredo
            form.instance.aventura_id = self.request.session[SESSION_AVENTURA].id
            self.object = form.save()   
            return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
        
        else:
            ValidationError
            msg = "Please. Activate an adventure for authoring!"
            messages.error(self.request, "".join(msg))
            return HttpResponse(json.dumps({'response': 'exception created'}), content_type="application/json") 
        
          
# delete enredo
class EnredoDeleteView(DeleteView):
    template_name = 'editor_enredos/enredos/delete.html'
    model = Enredo
    
    def delete(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        id_enredo = self.kwargs['pk']
        tipo_enredo = ''
        if EnredoFile.objects.all().filter(enredo_ptr_id=id_enredo).exists():
            tipo_enredo = "EnredoFile"
        elif EnredoInstancia.objects.all().filter(enredo_ptr_id=id_enredo).exists(): 
            tipo_enredo = "EnredoInstancia"
        elif EnredoMensagem.objects.all().filter(enredo_ptr_id=id_enredo).exists(): 
            tipo_enredo = "EnredoMensagem"
      
            
        try:
            self.object.delete()
        except ValidationError as e:
            messages.error(request, "".join(e.messages))
            return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        return HttpResponse(json.dumps({'response': tipo_enredo}), content_type="application/json")
    
    def get_success_url(self):
        return reverse('enredo_list_view') 
    
'''
====================================================================
                        Views para Missão/Condições
====================================================================
'''
# Lista as missões
class MissaoListView(ListView):
    template_name = 'editor_missao/missao/listar.html'
    model = Missao
    
    def get_queryset(self):
        
        object_list = ''
        if self.request.session[SESSION_AVENTURA] != '-1':
            object_list = Missao.objects.all().filter(aventuras_id=self.request.session[SESSION_AVENTURA].id)
            # for obj in object_list:
                # print obj
        return object_list
    
    
# cria uma missão
class MissaoCreateView(CreateView):
    template_name = 'editor_missao/missao/create.html'
    model = Missao
    form_class = CreateMissaoForm
    
    def get_success_url(self):
        return reverse('missao_list_view')
    
    def form_valid(self, form):
          
        # verifica se aventura está ativa
        if self.request.session[SESSION_AVENTURA] != '-1':
            form.instance.aventuras_id = self.request.session[SESSION_AVENTURA].id
            self.object = form.save() 
            return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
        else:
            ValidationError
            msg = "For the creating a mission it's necessary activate an adventure!"
            messages.error(self.request, "".join(msg))
            return HttpResponse(json.dumps({'response': 'exception created'}), content_type="pplication/json")

# atualiza um missão
class MissaoUpdateView(UpdateView):
    template_name = 'editor_missao/missao/update.html'
    model = Missao
    form_class = CreateMissaoForm
    
    def form_valid(self, form):
        self.object = form.save()   
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

# deleta uma missão
class MissaoDeleteView(DeleteView):
    template_name = 'editor_missao/missao/delete.html'
    model = Missao
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # try:
        self.object.delete()
        # except ValidationError as e:
            # messages.error(request, "".join(e.messages))
            # return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

class SetVarNode(template.Node):
 
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value
 
    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""
 
def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])
 
register.tag('set', set_var)

class CondicoesMissaoListView(ListView):
    template_name = 'editor_missao/condicoes/listar_condicoes_missao.html'
    model = Condicao
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CondicoesMissaoListView, self).get_context_data(**kwargs)
        
        object_list = ''
        if self.request.session[SESSION_AVENTURA] != '-1':
                      
            missao_list = Missao.objects.all().filter(id=self.kwargs['pk'], aventuras_id=self.request.session[SESSION_AVENTURA].id)


            flag = 0
            condicao_list = ''
            for obj in missao_list:
                if flag == 0:
                    condicao_list = Condicao.objects.all().filter(missao_id=obj.id,)
                    flag = 1
                elif flag == 1:
                    condicao_list = condicao_list | Condicao.objects.all().filter(missao_id=obj.id,)

            
            flag = 0
            condicao_jogador_instancia = ''
            for obj in  condicao_list:
                if flag == 0:
                    condicao_jogador_instancia = CondicaoJogadorInstancia.objects.all().filter(condicao_ptr_id=obj.id,)
                    flag = 1
                elif flag == 1:
                    condicao_jogador_instancia = condicao_jogador_instancia | CondicaoJogadorInstancia.objects.all().filter(condicao_ptr_id=obj.id,)
             
            
            flag = 0
            condicao_instancia = ''
            for obj in  condicao_list:
                if flag == 0:
                    condicao_instancia = CondicaoInstanciaObjeto.objects.all().filter(condicao_ptr_id=obj.id,)
                    flag = 1
                elif flag == 1:
                    condicao_instancia = condicao_instancia | CondicaoInstanciaObjeto.objects.all().filter(condicao_ptr_id=obj.id,)
             
            flag = 0
            condicao_avatar_objeto = ''
            for obj in  condicao_list:
                if flag == 0:
                    condicao_avatar_objeto = CondicaoJogadorObjeto.objects.all().filter(condicao_ptr_id=obj.id,)
                    flag = 1
                elif flag == 1:
                    condicao_avatar_objeto = condicao_avatar_objeto | CondicaoJogadorObjeto.objects.all().filter(condicao_ptr_id=obj.id,)
            
            flag = 0
            condicao_dialogo = ''
            for obj in  condicao_list:
                if flag == 0:
                    condicao_dialogo = CondicaoDialogoInstancia.objects.all().filter(condicao_ptr_id=obj.id,)
                    flag = 1
                elif flag == 1:
                    condicao_dialogo = condicao_dialogo | CondicaoDialogoInstancia.objects.all().filter(condicao_ptr_id=obj.id,)
  
           
            condicoes_tipos = ''
            condicoes_tipos = chain(condicao_jogador_instancia, condicao_instancia)
            condicoes_tipos = chain(condicoes_tipos, condicao_avatar_objeto)
            condicoes_tipos = chain(condicoes_tipos, condicao_dialogo)
            

            # atualizando field link
            '''
            for obj in condicoes_tipos:
                if obj.ligacao == "JOIN_OBJ":
                    obj.ligacao = "combinou"
                elif obj.ligacao == "GET_OBJ":
                    obj.ligacao = "possui"
                else:
                    obj.ligacao = "conversou"
             '''
        
            # Add in a QuerySet of all the books
            context['buffer'] = 0
            context['missao_list'] = missao_list
            context['object_list'] = condicoes_tipos
            context['condicao_jogador_instancia'] = condicao_jogador_instancia
            context['condicao_instancia'] = condicao_instancia
            context['condicao_avatar_objeto'] = condicao_avatar_objeto
            context['condicao_dialogo'] = condicao_dialogo
            
        
        return context 
    
    
# recupera a lista de condicoes 
class CondicoesListView(ListView, template.Node):
    template_name = 'editor_missao/condicoes/listar_condicoes.html'
    model = Condicao
  
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CondicoesListView, self).get_context_data(**kwargs)
        
        object_list = ''
        if self.request.session[SESSION_AVENTURA] != '-1':
                        
            missao_list = Missao.objects.all().filter(aventuras_id=self.request.session[SESSION_AVENTURA].id)


            flag = 0
            condicao_list = ''
            for obj in missao_list:
                if flag == 0:
                    condicao_list = Condicao.objects.all().filter(missao_id=obj.id,)
                    flag = 1
                elif flag == 1:
                    condicao_list = condicao_list | Condicao.objects.all().filter(missao_id=obj.id,)

            flag = 0
            condicao_jogador_instancia = ''
            for obj in  condicao_list:
                if flag == 0:
                    condicao_jogador_instancia = CondicaoJogadorInstancia.objects.all().filter(condicao_ptr_id=obj.id,)
                    flag = 1
                elif flag == 1:
                    condicao_jogador_instancia = condicao_jogador_instancia | CondicaoJogadorInstancia.objects.all().filter(condicao_ptr_id=obj.id,)
             
            
            flag = 0
            condicao_instancia = ''
            for obj in  condicao_list:
                if flag == 0:
                    condicao_instancia = CondicaoInstanciaObjeto.objects.all().filter(condicao_ptr_id=obj.id,)
                    flag = 1
                elif flag == 1:
                    condicao_instancia = condicao_instancia | CondicaoInstanciaObjeto.objects.all().filter(condicao_ptr_id=obj.id,)
             
            flag = 0
            condicao_avatar_objeto = ''
            for obj in  condicao_list:
                if flag == 0:
                    condicao_avatar_objeto = CondicaoJogadorObjeto.objects.all().filter(condicao_ptr_id=obj.id,)
                    flag = 1
                elif flag == 1:
                    condicao_avatar_objeto = condicao_avatar_objeto | CondicaoJogadorObjeto.objects.all().filter(condicao_ptr_id=obj.id,)
            
            flag = 0
            condicao_dialogo = ''
            for obj in  condicao_list:
                if flag == 0:
                    condicao_dialogo = CondicaoDialogoInstancia.objects.all().filter(condicao_ptr_id=obj.id,)
                    flag = 1
                elif flag == 1:
                    condicao_dialogo = condicao_dialogo | CondicaoDialogoInstancia.objects.all().filter(condicao_ptr_id=obj.id,)
  
           
            condicoes_tipos = ''
            condicoes_tipos = chain(condicao_jogador_instancia, condicao_instancia)
            condicoes_tipos = chain(condicoes_tipos, condicao_avatar_objeto)
            condicoes_tipos = chain(condicoes_tipos, condicao_dialogo)
            

            # atualizando field link
            '''
            for obj in condicoes_tipos:
                if obj.ligacao == "JOIN_OBJ":
                    obj.ligacao = "combinou"
                elif obj.ligacao == "GET_OBJ":
                    obj.ligacao = "possui"
                else:
                    obj.ligacao = "conversou"
             '''
        
            # Add in a QuerySet of all the books
            context['buffer'] = 0
            context['missao_list'] = missao_list
            context['object_list'] = condicoes_tipos
            context['condicao_jogador_instancia'] = condicao_jogador_instancia
            context['condicao_instancia'] = condicao_instancia
            context['condicao_avatar_objeto'] = condicao_avatar_objeto
            context['condicao_dialogo'] = condicao_dialogo
            
            
            print condicoes_tipos
            c1 = condicoes_tipos
            c2 = condicoes_tipos
            for m in missao_list:
                print m.nome
                for c in condicao_instancia:       
                    print c.nome
               
            
        return context 

# lista condição entre instâncias de objetos
class CondicaoObjetoListView(ListView):
    template_name = 'editor_missao/condicoes/listar_condicao_instancia_objeto.html'
    model = CondicaoInstanciaObjeto
    
    def get_queryset(self):

        object_list = ''
        if self.request.session[SESSION_AVENTURA] != '-1':
            missao_list = Missao.objects.all().filter(aventuras_id=self.request.session[SESSION_AVENTURA].id)
            
            flag = 0;
            for obj in missao_list:
                if flag == 0:
                    object_list = CondicaoInstanciaObjeto.objects.all().filter(missao_id=obj.id).order_by('missao')
                    flag = 1
                elif flag == 1:
                    object_list = object_list | CondicaoInstanciaObjeto.objects.all().filter(missao_id=obj.id).order_by('missao')
            # atualizando field link
            for obj in object_list:
                if obj.ligacao == "JOIN_OBJ":
                    obj.ligacao = "combinou"
                elif obj.ligacao == "GET_OBJ":
                    obj.ligacao = 'possui'
                else:
                    obj.ligacao = "conversou"

        return object_list
    

# cria condições entre instancias deobjetos
class CondicaoInstanciaObjetoCreateView(CreateView):
    template_name = 'editor_missao/condicoes/create_condicao_instancia_objeto.html'
    model = CondicaoInstanciaObjeto
    form_class = CondicaoInstanciaObjetoForm
    
    def get_initial(self):
        initial = super(CondicaoInstanciaObjetoCreateView, self).get_initial()
        if self.request.session[SESSION_AVENTURA] != '-1':
            initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        else:
            initial['aventura_id'] = '0'
        return initial
     
    def get_success_url(self):
        return reverse('condicao_objeto_list_view')
    
    def form_valid(self, form):
        
        # verifica se aventura está ativa
        if self.request.session[SESSION_AVENTURA] != '-1':
            form.instance.aventuras_id = self.request.session[SESSION_AVENTURA].id
            self.object = form.save() 
            return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
        else:
            ValidationError
            msg = "For the creating a condition it's necessary activate an adventure!"
            messages.error(self.request, "".join(msg))
            return HttpResponse(json.dumps({'response': 'exception created'}), content_type="pplication/json") 


# atualiza condições entre instâncias de objeto
class CondicaoInstanciaObjetoUpdateView(UpdateView):
    template_name = 'editor_missao/condicoes/update_condicao_instancia_objeto.html'
    model = CondicaoInstanciaObjeto
    form_class = CondicaoInstanciaObjetoForm
    
    def get_initial(self):
        initial = super(CondicaoInstanciaObjetoUpdateView, self).get_initial()
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial
    
    def form_valid(self, form):
        self.object = form.save()   
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")


# lista condicoes entre jogador e instâncias
class CondicaoJogadorInstanciaListView(ListView):
    template_name = 'editor_missao/condicoes/listar_condicao_jogador_instancias.html'
    model = CondicaoJogadorInstancia
    
    def get_queryset(self):

        object_list = ''
        if self.request.session[SESSION_AVENTURA] != '-1':
            missao_list = Missao.objects.all().filter(aventuras_id=self.request.session[SESSION_AVENTURA].id)

            flag = 0;
            for obj in missao_list:
                if flag == 0:
                    object_list = CondicaoJogadorInstancia.objects.all().filter(missao_id=obj.id).order_by('missao')
                    flag = 1
                elif flag == 1:
                    object_list = object_list | CondicaoJogadorInstancia.objects.all().filter(missao_id=obj.id).order_by('missao')
                
            # atualizando field link
            for obj in object_list:
                
                if obj.ligacao == "JOIN_OBJ":
                    obj.ligacao = "combinou"
                elif obj.ligacao == "GET_OBJ":
                    obj.ligacao = 'possui'
                else:
                    obj.ligacao = "conversou"
                
        return object_list
    
# Cria condição entre um determinado avatar da aventura e a instância de objeto
class CondicaoJogadorInstanciaCreateView(CreateView):
    template_name = 'editor_missao/condicoes/create_condicao_jogador_instancias.html'
    model = CondicaoJogadorInstancia
    form_class = CondicaoJogadorInstanciaForm
    
    def get_initial(self):
        initial = super(CondicaoJogadorInstanciaCreateView, self).get_initial()
        if self.request.session[SESSION_AVENTURA] != '-1':
            initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        else:
            initial['aventura_id'] = '0'
        return initial
    
    def get_success_url(self):
        return reverse('condicao_jogador_list_view')
    
    def form_valid(self, form):

        # verifica se aventura está ativa
        if self.request.session[SESSION_AVENTURA] != '-1':
            form.instance.aventuras_id = self.request.session[SESSION_AVENTURA].id
            self.object = form.save() 
            return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
        else:
            ValidationError
            msg = "For the creating a condition it's necessary activate an adventure!"
            messages.error(self.request, "".join(msg))
            return HttpResponse(json.dumps({'response': 'exception created'}), content_type="pplication/json") 
    


# update condicao entre instancias
class CondicaoJogadorInstanciaUpdateView(UpdateView):
    template_name = 'editor_missao/condicoes/update_condicao_jogador_instancia.html'
    model = CondicaoJogadorInstancia
    form_class = CondicaoJogadorInstanciaForm
    
    
    def get_initial(self):
        initial = super(CondicaoJogadorInstanciaUpdateView, self).get_initial()
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial
    
    # def get_form_kwargs(self, **kwargs):
    #    kwargs = super(CondicaoJogadorUpdateView, self).get_form_kwargs(**kwargs)
    #    kwargs['initial']['aventura_id'] = self.request.session[SESSION_AVENTURA].id
    #    return kwargs
    
    # def get_form_kwargs(self, **kwargs):
    #    kwargs = super(CondicaoJogadorUpdateView, self).get_form_kwargs(**kwargs)
    #    initial = kwargs.get('initial', {})
    #    initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
    #    kwargs['initial'] = initial
    #    return kwargs
    
    def form_valid(self, form):
        self.object = form.save()   
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
    # def form_invalid(self, form):
    #    return UpdateView.form_invalid(self, form)
    
# Lista condicoes entre jogador e objetos
class CondicaoJogadorObjetoListView(ListView):
    template_name = 'editor_missao/condicoes/listar_condicao_jogador_objeto.html'
    model = CondicaoJogadorObjeto
    
    def get_queryset(self):

        object_list = ''
        if self.request.session[SESSION_AVENTURA] != '-1':
            missao_list = Missao.objects.all().filter(aventuras_id=self.request.session[SESSION_AVENTURA].id)

            flag = 0;
            for obj in missao_list:
                if flag == 0:
                    object_list = CondicaoJogadorObjeto.objects.all().filter(missao_id=obj.id).order_by('missao')
                    flag = 1
                elif flag == 1:
                    object_list = object_list | CondicaoJogadorObjeto.objects.all().filter(missao_id=obj.id).order_by('missao')
                
            # atualizando field link
            for obj in object_list:
                
                if obj.ligacao == "JOIN_OBJ":
                    obj.ligacao = "combinou"
                elif obj.ligacao == "GET_OBJ":
                    obj.ligacao = 'possui'
                else:
                    obj.ligacao = "conversou"
                
        return object_list

# Cria condição entre um determinado avatar da aventura e um objeto
class CondicaoJogadorObjetoCreateView(CreateView):
    template_name = 'editor_missao/condicoes/create_condicao_jogador_objeto.html'
    model = CondicaoJogadorObjeto
    form_class = CondicaoJogadorObjetoForm
    
    def get_initial(self):
        initial = super(CondicaoJogadorObjetoCreateView, self).get_initial()
        if self.request.session[SESSION_AVENTURA] != '-1':
            initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        else:
            initial['aventura_id'] = '0'
        return initial
    
    def get_success_url(self):
        return reverse('condicao_jogador_objeto_list_view')
    
    def form_valid(self, form):

        # verifica se aventura está ativa
        if self.request.session[SESSION_AVENTURA] != '-1':
            form.instance.aventuras_id = self.request.session[SESSION_AVENTURA].id
            self.object = form.save() 
            return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
        else:
            ValidationError
            msg = "For the creating a condition it's necessary activate an adventure!"
            messages.error(self.request, "".join(msg))
            return HttpResponse(json.dumps({'response': 'exception created'}), content_type="pplication/json") 

# update condicao entre objetos
class CondicaoJogadorObjetoUpdateView(UpdateView):
    template_name = 'editor_missao/condicoes/update_condicao_jogador_objeto.html'
    model = CondicaoJogadorObjeto
    form_class = CondicaoJogadorObjetoForm
    
    
    def get_initial(self):
        initial = super(CondicaoJogadorObjetoUpdateView, self).get_initial()
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial

    def form_valid(self, form):
        self.object = form.save()   
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
    # def form_invalid(self, form):
    #    return UpdateView.form_invalid(self, form)  

# Lista condicoes de avatares e dialogos
class CondicaoDialogoInstanciaListView(ListView):
    template_name = 'editor_missao/condicoes/listar_condicoes_dialogo_instancia_objeto.html'
    model = CondicaoDialogoInstancia
    
    def get_queryset(self):

        object_list = ''
        if self.request.session[SESSION_AVENTURA] != '-1':
            missao_list = Missao.objects.all().filter(aventuras_id=self.request.session[SESSION_AVENTURA].id)
            
            flag = 0;
            for obj in missao_list:
                if flag == 0:
                    object_list = CondicaoDialogoInstancia.objects.all().filter(missao_id=obj.id).order_by('missao')
                    flag = 1
                elif flag == 1:
                    object_list = object_list | CondicaoDialogoInstancia.objects.all().filter(missao_id=obj.id).order_by('missao')
                
            # atualizando field link
            for obj in object_list:

                if obj.ligacao == "JOIN_OBJ":
                    obj.ligacao = u"combinou"
                elif obj.ligacao == "GET_OBJ":
                    obj.ligacao = u"possui"
                else:
                    obj.ligacao = u"conversou"
                
                if obj.sufixo == "DIALOGO_INICIAL":
                    obj.sufixo = u"Dialogo Inicial"
                elif obj.sufixo == "DIALOGO_FINAL":
                    obj.sufixo = u"Dialogo Final"
                elif obj.sufixo == "ACEITO":
                    obj.sufixo = u"confirmação"
                else:
                    obj.sufixo = u"negação"
                    
        return object_list
    
# Cria a dondição entre um Avatar e uma parte de diálogo de uma dada instância.
class CondicaoDialogoInstanciaCreateView(CreateView):
    template_name = 'editor_missao/condicoes/create_condicao_dialogo_instancia.html'
    model = CondicaoDialogoInstancia
    form_class = CondicaoDialogoInstanciaForm
    
    def get_initial(self):
        initial = super(CondicaoDialogoInstanciaCreateView, self).get_initial()
        if self.request.session[SESSION_AVENTURA] != '-1':
            initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        else:
            initial['aventura_id'] = '0'
        return initial
    
    def get_success_url(self):
        return reverse('condicoes_dialogo_list_view')
    
    def form_valid(self, form):
          
        self.object = form.save() 
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")  


# update condicao dialogos
class CondicaoDialogoInstanciaUpdateView(UpdateView):
    template_name = 'editor_missao/condicoes/update_condicao_dialogo_instancia.html'
    model = CondicaoDialogoInstancia
    form_class = CondicaoDialogoInstanciaForm
    def get_initial(self):
        initial = super(CondicaoDialogoInstanciaUpdateView, self).get_initial()
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial
    
    def form_valid(self, form):
        self.object = form.save()   
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")




# Deleção de todas os três tipos de condições
class CondicaoDeleteView(DeleteView):
    template_name = 'editor_missao/condicoes/delete_condicao.html'
    model = Condicao
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # try:
        
        # if self.object == CondicaoJogador:
        #    print "Condicao Jogador"
        
        id_condicao = self.kwargs['pk']
        tipo_condicao = ''
        if CondicaoJogadorInstancia.objects.all().filter(condicao_ptr_id=id_condicao).exists():
            tipo_condicao = "CondicaoJogadorInstancia"
        elif CondicaoInstanciaObjeto.objects.all().filter(condicao_ptr_id=id_condicao).exists(): 
            tipo_condicao = "CondicaoInstanciaObjeto"
        elif CondicaoDialogoInstancia.objects.all().filter(condicao_ptr_id=id_condicao).exists(): 
            tipo_condicao = "CondicaoDialogoInstancia"
        elif CondicaoJogadorObjeto.objects.all().filter(condicao_ptr_id=id_condicao).exists(): 
            tipo_condicao = "CondicaoJogadorObjeto"
            
        self.object.delete()
        return HttpResponse(json.dumps({'response': tipo_condicao}), content_type="application/json")
        # except ValidationError as e:
            # messages.error(request, "".join(e.messages))
            # return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        # return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
 
'''
====================================================================
                        Views para Avatares
====================================================================
'''
   
# Recupera lista de avatars para a avetura que está sendo editada. 
class AvataresListView(ListView):
    template_name = 'editor_jogadores/avatares/listar.html'
    model = Avatar
    
    def get_queryset(self):
        
        # id_av = self.request.session[SESSION_AVENTURA]
        
        object_list = ''
        if self.request.session[SESSION_AVENTURA] != '-1':
            object_list = Avatar.objects.all().filter(aventura_avatar_id=self.request.session[SESSION_AVENTURA].id)

        return object_list
    
# Cria avatares para a aventura que está sendo editada
class AvataresCreateView(CreateView):
    template_name = 'editor_jogadores/avatares/create.html'
    model = Avatar
    form_class = CreateAvatarForm
    
    def get_success_url(self):
        return reverse('missao_list_view')
    
    def form_valid(self, form):
        if self.request.session[SESSION_AVENTURA] != '-1':
            form.instance.aventura_avatar_id = self.request.session[SESSION_AVENTURA].id
            self.object = form.save()
            return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
        else:
            ValidationError
            msg = "Please. Activate an adventure for authoring!"
            messages.error(self.request, "".join(msg))
            return HttpResponse(json.dumps({'response': 'exception created'}), content_type="application/json")
              

# Atualiza avatar
class AvataresUpdateView(UpdateView):
    template_name = 'editor_jogadores/avatares/update.html'
    model = Avatar
    form_class = CreateAvatarForm
    def form_valid(self, form):
        self.object = form.save()   
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

# Deleção do avatar
class AvataresDeleteView(DeleteView):
    template_name = 'editor_jogadores/avatares/delete.html'
    model = Avatar
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ValidationError as e:
            messages.error(request, "".join(e.messages))
            return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
# Recupe a lista de instâncias que são controaldas por avatares
class AvataresListInstancesView(ListView):
    template_name = 'editor_jogadores/papeis/listar.html'
    model = Avatar
    form_class = AvatarRoleListForm
    
    def get_queryset(self):
        
        object_list = ''
        if self.request.session[SESSION_AVENTURA] != '-1':
            object_list = Avatar.objects.all().filter(aventura_avatar_id=self.request.session[SESSION_AVENTURA].id)

        return object_list
    # def get_queryset(self):
        
        # id_av = self.request.session[SESSION_AVENTURA].id
        
        # if id_av > 0:
        #    object_list = Missao.objects.all().filter(aventuras_id=id_av)

        # return object_list
# Atualiza roles
class AvataresUpdateRolesView(UpdateView):
    template_name = 'editor_jogadores/papeis/update.html'
    model = Avatar
    form_class = AvatarRoleListForm
    def form_valid(self, form):
        
        object_list = Avatar.objects.all().filter(inst_objeto_id=self.object.inst_objeto_id)
        object_list_end = "";
        
        for obj in object_list:
            if self.object.id != obj.id:
                object_list_end += obj;
        
        if object_list_end:
            ValidationError
            msg = "Está instância já está sendo controlada por outro Avatar!"
            messages.error(self.request, "".join(msg))
            return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        
        
        self.object = form.save()   
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

 
'''
====================================================================
                        Views para Agentes
====================================================================
''' 
   
# atualiza session do agente que está tendo o comportamento criado
class AgenteSessionView(UpdateView):
    # template_name = 'editor_objetos/aventura/message.html'
    model = Agente
    form_class = AgenteWithoutFieldsForm
    
    def get_success_url(self):
        return reverse('agente_list_view') 
    
    # Verifica se o agente possui o comportamento informado
    # Assim, retornar uma resposta se é atualização ou criação de comportamento
    def form_valid(self, form, *args, **kwargs):
        # form.instance.aventura_agente_id =  self.request.session[SESSION_AVENTURA].id

        dados = json.loads(self.request.body)  # get json post
        
        self.request.session[SESSION_AGENTE] = self.object
        self.request.session[SESSION_TYPE_BEHAVIOR] = dados[0]['comportamento']
        comportamento = Comportamento.objects.all().filter(agente_id=dados[0]['idAgente'])
         
        # nunca atualiza - POG ;)
        flag = 0
        if flag == 1:
            self.object = form.save()
        
        if comportamento:
            return HttpResponse(json.dumps({'response': 'update'}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'response': 'create'}), content_type="application/json")
   
# recupera a lista de agentes da aventura corrente
class AgentesListView(ListView):
    template_name = 'editor_movimentos/agentes/listar.html'
    model = Agente
    
    def get_queryset(self):
        object_list = ''
        if self.request.session[SESSION_AVENTURA] != '-1':
            object_list = Agente.objects.all().filter(aventura_agente_id=self.request.session[SESSION_AVENTURA].id)

        return object_list   

# Criaçãao do agente
class AgenteCreateView(CreateView):
    template_name = 'editor_movimentos/agentes/create.html'   
    model = Agente
    form_class = AgenteCreateForm
    
    def get_success_url(self):
        return reverse('agente_list_view')
    
    def get_initial(self):
        initial = super(AgenteCreateView, self).get_initial()
        if self.request.session[SESSION_AVENTURA] != '-1':
            initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        else:
            initial['aventura_id'] = self.request.session[SESSION_AVENTURA]
            ValidationError
            messages.error(self.request, "".join("Please. Activate an adventure for authoring!"))
        return initial
    
    
    def form_valid(self, form):
        
        if self.request.session[SESSION_AVENTURA] != '-1':
            form.instance.aventura_agente_id = self.request.session[SESSION_AVENTURA].id
            self.object = form.save()
        else:
            ValidationError
            messages.error(self.request, "".join("Please. Activate an adventure for authoring to create an agent!"))
            return HttpResponse(json.dumps({'response': 'no adventure activate'}), content_type="text")
        
        
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
 
# Atualização do agente
class AgenteUpdateView(UpdateView):
    template_name = 'editor_movimentos/agentes/update.html'   
    model = Agente
    form_class = AgenteCreateForm
    
    def get_initial(self):
        initial = super(AgenteUpdateView, self).get_initial()
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial
    
    def get_success_url(self):
        return reverse('agente_list_view')
    
    def form_valid(self, form):
        
        form.instance.aventura_agente_id = self.request.session[SESSION_AVENTURA].id
        
        if self.request.session[SESSION_AVENTURA] != '-1':
            
            # id agente
            id_agente = self.kwargs['pk']
            # recupera comportamento
            comportamento = Comportamento.objects.all().filter(agente_id=id_agente)
            # verifica tipo de comportamento
            tipo_comportamento_nome = ''
            tipo_comportamento_objeto = ''
            tipo_comportamento_id = ' '
            for obj in comportamento:
                # verificando o tipo de comportamento
                agressivo = Agressivo.objects.all().filter(comportamento_ptr_id=obj.pk)
                if agressivo:
                    tipo_comportamento_objeto = agressivo
                    tipo_comportamento_nome = "Agressivo"
                    tipo_comportamento_id = obj.pk
                passivo = Passivo.objects.all().filter(comportamento_ptr_id=obj.pk)
                if passivo:
                    tipo_comportamento_objeto = passivo
                    tipo_comportamento_nome = "Passivo"
                    tipo_comportamento_id = obj.pk
                colaborativo = Colaborativo.objects.all().filter(comportamento_ptr_id=obj.pk)
                if colaborativo:
                    tipo_comportamento_objeto = colaborativo
                    tipo_comportamento_nome = "Colaborativo"
                    tipo_comportamento_id = obj.pk 
                competidor = Competitivo.objects.all().filter(comportamento_ptr_id=obj.pk)
                if competidor:
                    tipo_comportamento_objeto = competidor
                    tipo_comportamento_nome = "Competidor"
                    tipo_comportamento_id = obj.pk     
                          
            # verifica se o novo comportamento é diferente ao antigo
            if str(tipo_comportamento_nome) != str(form.instance.comportamento):  # verificação ineficiente, feita com base em string
                    # deleta comportamento antigo
                    if tipo_comportamento_objeto: 
                        # mensagem apresentada ao autor, informando que o comprotamento antigo foi apagado.
                        msg = "The old beahavior, called " + tipo_comportamento_nome + ", was deleted!"
                        
                        self.object = form.save()
                        
                        return HttpResponse(json.dumps({'comportamento': str(tipo_comportamento_id), 'mensagem' : msg }), content_type="application/json")
                    
        self.object = form.save()
        return HttpResponse(json.dumps({'comportamento': 'nothing'}), content_type="application/json")

# Delecao do comportamento
class ComportamentoOldDeleteView(DeleteView):
    model = Comportamento
    
    def get_success_url(self):
        return reverse('agente_list_view')
    
    
    def delete(self, request, *args, **kwargs):
        
        comportamento = Comportamento.objects.all().filter(pk=self.kwargs['pk'])
        self.object = comportamento
        self.object.delete()
    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    

# Criação do comportamento agressivo para o agente   
class AgressivoCreateView(CreateView):
    template_name = 'editor_movimentos/agentes/create_agressivo.html'   
    model = Agressivo
    form_class = AgressivoCreateForm
    
    
    def get_initial(self):
        initial = super(AgressivoCreateView, self).get_initial()
        print self.request.session[SESSION_AGENTE]
        print self.request.session[SESSION_AGENTE].instancia_id
        initial['instancia_id'] = self.request.session[SESSION_AGENTE].instancia_id
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial
    
    def get_success_url(self):
        return reverse('agente_list_view')
    
    def form_valid(self, form):
        # form.instance.aventura_agente_id =  self.request.session[SESSION_AVENTURA].id
        form.instance.agente_id = self.request.session[SESSION_AGENTE].id
        self.object = form.save()
    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
# atualiza comportamento agressivo
class AgressivoUpdateView(UpdateView):
    template_name = 'editor_movimentos/agentes/update_agressivo.html'
    model = Agressivo
    form_class = AgressivoCreateForm
    
    def get_initial(self):
        initial = super(AgressivoUpdateView, self).get_initial()
        initial['instancia_id'] = self.request.session[SESSION_AGENTE].instancia_id
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial
    
    def get_success_url(self):
        return reverse('agente_list_view')
    
    def form_valid(self, form):
        # form.instance.aventura_agente_id =  self.request.session[SESSION_AVENTURA].id
        form.instance.agente_id = self.request.session[SESSION_AGENTE].id
        
        self.object = form.save()
    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
# Criação do comportamento passivo para o agente   
class PassivoCreateView(CreateView):
    template_name = 'editor_movimentos/agentes/create_passivo.html'   
    model = Passivo
    form_class = PassivoCreateForm
    
    
    def get_initial(self):
        initial = super(PassivoCreateView, self).get_initial()
        initial['instancia_id'] = self.request.session[SESSION_AGENTE].instancia_id
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial
    
    def get_success_url(self):
        return reverse('agente_list_view')
    
    def form_valid(self, form):
        # form.instance.aventura_agente_id =  self.request.session[SESSION_AVENTURA].id
        form.instance.agente_id = self.request.session[SESSION_AGENTE].id
        self.object = form.save()
    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
# Atualização do comportamento passivo para o agente   
class PassivoUpdateView(UpdateView):
    template_name = 'editor_movimentos/agentes/update_passivo.html'   
    model = Passivo
    form_class = PassivoCreateForm
    
    
    def get_initial(self):
        initial = super(PassivoUpdateView, self).get_initial()
        initial['instancia_id'] = self.request.session[SESSION_AGENTE].instancia_id
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial
    
    def get_success_url(self):
        return reverse('agente_list_view')
    
    def form_valid(self, form):
        # form.instance.aventura_agente_id =  self.request.session[SESSION_AVENTURA].id
        form.instance.agente_id = self.request.session[SESSION_AGENTE].id
        self.object = form.save()
    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
# Criação do comportamento Colaborativo para p agente
class ColaborativoCreateView(CreateView):
    template_name = 'editor_movimentos/agentes/create_colaborativo.html'
    model = Colaborativo
    form_class = ColaborativoCreateForm
    
    def get_initial(self):
        initial = super(ColaborativoCreateView, self).get_initial()
        initial['instancia_id'] = self.request.session[SESSION_AGENTE].instancia_id
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial
    
    def get_success_url(self):
        return reverse('agente_list_view')
    
    def form_valid(self, form):
        # form.instance.aventura_agente_id =  self.request.session[SESSION_AVENTURA].id
        print form 
        form.instance.agente_id = self.request.session[SESSION_AGENTE].id
        self.object = form.save()
    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

# Atualização do comportamento Colaborativo para p agente
class ColaborativoUpdateView(UpdateView):
    template_name = 'editor_movimentos/agentes/update_colaborativo.html'
    model = Colaborativo
    form_class = ColaborativoCreateForm
    
    def get_initial(self):
        initial = super(ColaborativoUpdateView, self).get_initial()
        initial['instancia_id'] = self.request.session[SESSION_AGENTE].instancia_id
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial
    
    def get_success_url(self):
        return reverse('agente_list_view')
    
    def form_valid(self, form):
        # form.instance.aventura_agente_id =  self.request.session[SESSION_AVENTURA].id
        print form 
        form.instance.agente_id = self.request.session[SESSION_AGENTE].id
        self.object = form.save()
    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    

# Criação do comportamento Competitivo para o agente
class CompetitivoCreateView(CreateView):
    template_name = 'editor_movimentos/agentes/create_competitivo.html'
    model = Competitivo
    form_class = CompetitivoCreateForm
    
    def get_initial(self):
        initial = super(CompetitivoCreateView, self).get_initial()
        initial['instancia_id'] = self.request.session[SESSION_AGENTE].instancia_id
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial
    
    def get_success_url(self):
        return reverse('agente_list_view')
    
    def form_valid(self, form):
        # form.instance.aventura_agente_id =  self.request.session[SESSION_AVENTURA].id
        print form 
        form.instance.agente_id = self.request.session[SESSION_AGENTE].id
        self.object = form.save()
    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
# Atualização do comportamento Colaborativo para p agente
class CompetitivoUpdateView(UpdateView):
    template_name = 'editor_movimentos/agentes/update_competitivo.html'
    model = Competitivo
    form_class = CompetitivoCreateForm
    
    def get_initial(self):
        initial = super(CompetitivoUpdateView, self).get_initial()
        initial['instancia_id'] = self.request.session[SESSION_AGENTE].instancia_id
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial
    
    def get_success_url(self):
        return reverse('agente_list_view')
    
    def form_valid(self, form):
        # form.instance.aventura_agente_id =  self.request.session[SESSION_AVENTURA].id
        print form 
        form.instance.agente_id = self.request.session[SESSION_AGENTE].id
        self.object = form.save()
    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

# retorna a lista de mensagegens do comportamento atual que está sendo editado
class ListInstances(ListView):
    template_name = 'editor_movimentos/agentes/list_instance.html'
    model = Mensagem
    
    def get_queryset(self):
        
        object_list = ''
        if self.request.session[SESSION_AVENTURA] != '-1':
            
            comportamento = Comportamento.objects.all().filter(agente_id=self.request.session[SESSION_AGENTE].id)
            
            id_comportamento = ''
            for obj in comportamento:
                id_comportamento = obj.pk
            
            object_list = Mensagem.objects.all().filter(colaborativo_id=id_comportamento)

        return object_list   


# Add Instâncias para comportamento Calaborativo ou Competidor
class InstanciasCreateView(CreateView):
    template_name = 'editor_movimentos/agentes/add_instance.html'
    model = Mensagem
    form_class = InstancesComportamentoAddForm
    
    def get_initial(self):
        initial = super(InstanciasCreateView, self).get_initial()
        initial['instancia_id'] = self.request.session[SESSION_AGENTE].instancia_id
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial
    
    def get_success_url(self):
        return reverse('agente_list_view')
    
    def form_valid(self, form):
        # form.instance.aventura_agente_id =  self.request.session[SESSION_AVENTURA].id
        
        comportamentos = Comportamento.objects.all().filter(agente_id=self.request.session[SESSION_AGENTE].id)
        
        id_comportamento = ''
        for obj in comportamentos:
            id_comportamento = obj.pk
        
        print id_comportamento
        print self.request.session[SESSION_TYPE_BEHAVIOR]
        
        if self.request.session[SESSION_TYPE_BEHAVIOR] == "Colaborativo":
            form.instance.colaborativo_id = id_comportamento
        else:
            form.instance.colaborativo_id = id_comportamento
            
        self.object = form.save()
    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")  

  
# Atualiza Instâncias para comportamento Calaborativo ou Competidor
class InstanciasUpdateView(UpdateView):
    template_name = 'editor_movimentos/agentes/update_instance.html'
    model = Mensagem
    form_class = InstancesComportamentoAddForm
    
    def get_initial(self):
        initial = super(InstanciasUpdateView, self).get_initial()
        initial['instancia_id'] = self.request.session[SESSION_AGENTE].instancia_id
        initial['aventura_id'] = self.request.session[SESSION_AVENTURA].id
        return initial 
    
    def form_valid(self, form):
        # form.instance.aventura_agente_id =  self.request.session[SESSION_AVENTURA].id
        
        comportamentos = Comportamento.objects.all().filter(agente_id=self.request.session[SESSION_AGENTE].id)
        
        id_comportamento = ''
        for obj in comportamentos:
            id_comportamento = obj.pk
        
        print id_comportamento
        print self.request.session[SESSION_TYPE_BEHAVIOR]
        
        if self.request.session[SESSION_TYPE_BEHAVIOR] == "Colaborativo":
            form.instance.colaborativo_id = id_comportamento
        else:
            form.instance.colaborativo_id = id_comportamento
            
        self.object = form.save()
    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json") 
    
    def get_success_url(self):
        return reverse('agente_list_view')
    
# Deleção do Agente
class AgenteDeleteView(DeleteView):
    template_name = 'editor_movimentos/agentes/delete.html'
    model = Agente

    # Override no delete para retornar uma resposta json caso o objeto seja deletado com sucesso
    def delete(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        self.object.delete()
        
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
    def get_success_url(self):
        return reverse('agente_list_view') 
    
    
 
'''
====================================================================
                        Views para Models de Estado do Jogo
====================================================================
''' 
   
class PosInstanciaAtivaCreateView(AjaxableResponseMixin, CreateView):  
    model = PosInstanciaAtiva
    form_class = PosInstanciaAtivaCreateForm
    
    def get_success_url(self):
        return reverse('avtentura_ativas_list_view') 
    
    def form_valid(self, form, *args, **kwargs):
       
        pos = json.loads(self.request.body)  # get json post
        # exemplo de acesso, pos[0]['id_objeto']
        

        for ins in pos['PosInstanciaAtiva']:
            posinstanciaativa = PosInstanciaAtiva()
            posinstanciaativa.latitude = ins['lat']
            posinstanciaativa.longitude = ins['log']
            posinstanciaativa.altitude = ins['alt']
            posinstanciaativa.instancia_objeto_ativa_id = ins['instancia_id']
            posinstanciaativa.aventura_ativa_instancia_id = pos['aventura_ativa_id'] 
            posinstanciaativa.save()
            # form.instance.latitude = ins['lat']
            # form.instance.longitude = ins['log']
            # form.instance.altitude = ins['alt']
            # form.instance.instancia_objeto_ativa_id = ins['instancia_id']
            # form.instance.aventura_ativa_instancia_id = pos['aventura_ativa_id'] 
            # self.object = form.save()
            

        # form.instance.nome = pos[0]['nome']
        # form.instance.objeto_id = pos[0]['id_objeto']
        # form.instance.aventura_id =  self.request.session[SESSION_AVENTURA].id
        # form.instance.instancia_cont = qntde_new_inst_obj
        # self.object = form.save()
        # response = super(AjaxableResponseMixin, self).form_valid(form)
                       
        # qntde_pos = 1

               
        data_return = {'response': 'ok', }         

        return self.render_to_json_response(data_return)

class AvatarAtivoCreateView(AjaxableResponseMixin, CreateView):  
    model = AvatarAtivo
    form_class = AvatarAtivoCreateForm
    
    def get_success_url(self):
        return reverse('avtentura_ativas_list_view') 
    
    def form_valid(self, form, *args, **kwargs):
       
        pos = json.loads(self.request.body)  # get json post
        # exemplo de acesso, pos[0]['id_objeto']
        
        for ins in pos['AvatarAtivo']:
            posavatarativo = AvatarAtivo()
            posavatarativo.latitude = 0.0
            posavatarativo.longitude = 0.0
            posavatarativo.avatar_id = ins['avatar_id']
            posavatarativo.aventura_ativa_avatar_id = pos['aventura_ativa_id'] 
            posavatarativo.save()

               
        data_return = {'response': 'ok', }         

        return self.render_to_json_response(data_return)
    
class MissaoAtivaCreateView(AjaxableResponseMixin, CreateView):  
    model = MissaoAtiva
    form_class = MissaoAtivaCreateForm
    
    def get_success_url(self):
        return reverse('avtentura_ativas_list_view') 
    
    def form_valid(self, form, *args, **kwargs):
       
        pos = json.loads(self.request.body)  # get json post
        # exemplo de acesso, pos[0]['id_objeto']
        

        for ins in pos['MissaoAtiva']:
            posmissaoativa = MissaoAtiva()
            posmissaoativa.estado_missao = False
            posmissaoativa.missao_id = ins['missao_id']
            posmissaoativa.aventura_ativa_missao_id = pos['aventura_ativa_id'] 
            posmissaoativa.save()

               
        data_return = {'response': 'ok', }         

        return self.render_to_json_response(data_return)

class CondicaoAtivaCreateView(AjaxableResponseMixin, CreateView):  
    model = CondicaoAtiva
    form_class = CondicaoAtivaCreateForm
    
    def get_success_url(self):
        return reverse('avtentura_ativas_list_view') 
    
    def form_valid(self, form, *args, **kwargs):
       
        pos = json.loads(self.request.body)  # get json post
        # exemplo de acesso, pos[0]['id_objeto']
        

        for ins in pos['CondicaoAtiva']:
            poscondicaoativa = CondicaoAtiva()
            poscondicaoativa.estado_condicao = False
            missaoativa = MissaoAtiva.objects.all().filter(missao_id=ins['missao_id'], aventura_ativa_missao_id=pos['aventura_ativa_id'])
            for m in missaoativa:
                poscondicaoativa.missao_ativa_id = m.pk
            poscondicaoativa.aventura_ativa_condicao_id = pos['aventura_ativa_id'] 
            poscondicaoativa.condicao_id = ins['condicao_id'] 
            poscondicaoativa.save()

               
        data_return = {'response': 'ok', }         

        return self.render_to_json_response(data_return)
