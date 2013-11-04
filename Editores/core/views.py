# -*- coding: utf-8 -*-
'''
Created on 17/09/2013

@author: Roberto

Convenção: NomeDaClasseAçao - TipoObjetoCreateView
'''

#from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from editor_objetos.models import Objeto, TipoObjeto, Icone, Aventura
from django.core import serializers
from forms import AventuraForm, AventuraWithoutFieldsForm
import json
from django.core.context_processors import request
from django.contrib.auth import login
SESSION_AVENTURA = '_user_aventura_id'

'''
===================================================================
                    Views para Tipo de Objeto
===================================================================
'''
#Listagem dos tipos de objetos
class TipoObjetoListView(ListView):
    model = TipoObjeto
    template_name = 'editor_objetos/tipo_objeto/listar.html'

#Criação do tipo de objeto
class TipoObjetoCreateView(CreateView):
    template_name = 'editor_objetos/tipo_objeto/create.html'
    model = TipoObjeto
   
    #redireciona a requisição
    def get_success_url(self):
        return reverse('tipo_objeto_list_view')
    
    #Override no form
    def form_valid(self, form):
        self.object = form.save()    
        #json.dumps() transforma objeto em string JSON e, json.loads() transforma string JSON em objeto    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
   
#Atualização de um tipo de objeto
class TipoObjetoUpdateView(UpdateView):
    template_name = 'editor_objetos/tipo_objeto/update.html'
    model = TipoObjeto
    
    def get_success_url(self):
        return reverse('tipo_objeto_list_view')
    
    #Override no form. 
    def form_valid(self, form):
        self.object = form.save()      
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

#Deleção do tipo de objeto
class TipoObjetoDeleteView(DeleteView):
    template_name = 'editor_objetos/tipo_objeto/delete.html'
    model = TipoObjeto
     
    #Override no método delete para evitar o delete em cascata
    #Anteriormente quando um Tipo de Objeto era deletado, todos os... 
    #...ojetos desse tipo também eram deletados, pois o django por padrão configura o DB em cascate.
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ValidationError as e:
            messages.error(request, "".join(e.messages))
            return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
        #return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('tipo_objeto_list_view')  


#Retorna uma lista de tipos de objetos contendo o id do tipo e o tipo, em json
class TipoObjetoGetJsonView(ListView):
    model = TipoObjeto

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(serializers.serialize('json', TipoObjeto.objects.all(), fields=('pk','tipo')))


'''
===================================================================
                    Views para o Icone 
                    
Icone- é a imagem do objeto no momento da autoria.
===================================================================
'''
#Listagem dos icones
class IconeListView(ListView): 
    model = Icone
    template_name = 'editor_objetos/icones/listar.html'

# Criação do icone
class IconeCreateView(CreateView):
    template_name = 'editor_objetos/icones/create.html'
    model = Icone
    
    def get_success_url(self):
        return reverse('icone_list_view')  
    
    #Override no form. 
    def form_valid(self, form):
        self.object = form.save()    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
    #def upload_pic
    #form_valid(self, request):
    #    icone = request.
    #    if icone:
    #        if  icone._size > 4*1024*1024:
    #            raise ValidationError("O ícone não deve ultrapassar o tamanho de  4mb!")
    #        return icone
    #    else:
    #        raise ValidationError("Não foi possível ler o ícone carregado")

#Atualização de um icone
class IconeUpdateView(UpdateView): #não entendi pq havia usado herança multipla aqui. Não é necessário
    template_name = 'editor_objetos/icones/update.html'
    model = Icone
         
    def get_success_url(self):
        return reverse('icone_list_view')
    
    #Override no form. 
    def form_valid(self, form):
        self.object = form.save()    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

#Deleção do icone
class IconeDeleteView(DeleteView):
    template_name = 'editor_objetos/icones/delete.html'
    model = Icone
     
    #Override no método delete para evitar o deletar em cascata
    #Se algum objeto estiver referênciando o icone, não será possivel deletar o mesmo.
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ValidationError as e:
            messages.error(request, "".join(e.messages))
            return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

#Retorna a url do icone 
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
#Listagem dos objetos
class ObjetoListView(ListView):
    model = Objeto
    template_name = 'editor_objetos/objeto/listar.html'

#Criação de objetos
class ObjetoCreateView(CreateView):
    template_name = 'editor_objetos/objeto/create.html'
    model = Objeto
    
    def get_success_url(self):
        return reverse('objeto_list_view')
    
    #Override no form. 
    def form_valid(self, form):
        self.object = form.save()    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
   
#atualização de um objeto especifico  
class ObjetoUpdateView(UpdateView): 
    template_name = 'editor_objetos/objeto/update.html'
    model = Objeto

    #def get_object(self):
    #    return Objeto.objects.get(pk=self.request.GET.get('pk'))
    
    def form_valid(self, form):
        self.object = form.save()    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
    def get_success_url(self):
        return reverse('objeto_list_view')
    
#Deleção de objeto
class ObjetoDeleteView(DeleteView):
    template_name = 'editor_objetos/objeto/delete.html'
    model = Objeto

    #Override no delete para retornar uma resposta json caso o objeto seja deletado com sucesso
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
    def get_success_url(self):
        return reverse('objeto_list_view')  


#Retorna uma lista contento o id e nome do objeto,  e id do seu icone
class ObjetoGetJsonView(ListView):
    model = Objeto

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(serializers.serialize('json', Objeto.objects.all().filter(tipo_objeto=self.kwargs['pk']), fields=('pk','nome', 'icone_objeto')))
    
    
    
'''
====================================================================
                        Views para GMapView
====================================================================                   

'''
class GMapView(TemplateView):
    template_name = 'editor_objetos/gmap/gmap.html'

    
''''
====================================================================
                        Views para Aventura
====================================================================
'''
#Listagem da aventura
class AventuraListView(ListView):
    model = Aventura
    template_name = 'editor_objetos/aventura/listar.html' 
        
    def get_queryset(self):
        #print self.request.session[SESSION_AVENTURA]
        object_list = Aventura.objects.all().filter(autor=self.kwargs['pk'])
        #self.model.objects.filter(pk = self.kwargs['pk'])
        return object_list
    
#Criação das aventuras
class AventuraCreateView(CreateView):
    template_name = 'editor_objetos/aventura/create.html'
    model = Aventura
    form_class = AventuraForm
    
    def get_success_url(self):
        return reverse('aventura_list_view')
    
    #Override no form. 
    def form_valid(self, form):
        form.instance.autor_id = self.kwargs['pk']
        self.object = form.save()    
        return HttpResponse(json.dumps({'response' : 'ok'}), content_type="application/json")

#Atualização de uma aventura
class AventuraUpdateView(UpdateView):
    template_name = 'editor_objetos/aventura/update.html'
    model = Aventura
    form_class = AventuraForm
    
    def get_success_url(self):
        return reverse('aventura_list_view')
    
    #Override no form. 
    def form_valid(self, form):
        self.object = form.save()    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

#Adiciona objeto da aventura na SESSION
#class AventuraEditarView(DeleteView):
class AventuraAtivarView(UpdateView):
    template_name = 'editor_objetos/aventura/message.html'
    model = Aventura
    form_class = AventuraWithoutFieldsForm
    
    def get_success_url(self):
        return reverse('aventura_list_view')   

    def form_valid(self, form):
        
        self.request.session[SESSION_AVENTURA] = self.object
        nome = self.request.session[SESSION_AVENTURA].nome
        if self.request.session[SESSION_AVENTURA] == '-1':
            ValidationError
            messages.error(request, "".join("Ocorreu um problema ao ativar a aventura! Tente novamente!"))
            return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        return HttpResponse(json.dumps({'response': nome }), content_type="application/json")

    #def render_to_response(self, context, **response_kwargs):
        
    #    self.request.session[SESSION_AVENTURA] = self.kwargs['pk']
        
    #    return HttpResponse(serializers.serialize('json', Aventura.objects.all().filter(id=self.kwargs['pk'])))
         
    #def get_queryset(self):
    #    
    #    object_list = Aventura.objects.all().filter(id=self.kwargs['pk'])
    #    self.request.session[SESSION_AVENTURA] = self.kwargs['pk']
    #    print self.request.session[SESSION_AVENTURA]
    #    
    #    return object_list
        #return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

    
#Deleção da aventura
class AventuraDeleteView(DeleteView):
    template_name = 'editor_objetos/aventura/delete.html'
    model = Aventura
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        #verifica se a aventura está em autoria
        if self.request.session[SESSION_AVENTURA].id == self.object.id:
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

    
    
#Retorna json contendo dados da aventura
class AventuraGetJsonView(ListView):
    model = Aventura
    
    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(serializers.serialize('json', Aventura.objects.all().filter(pk=self.kwargs['pk'])))
