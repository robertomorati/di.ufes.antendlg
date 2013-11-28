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
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from editor_objetos.models import Objeto, TipoObjeto, Icone, Aventura, InstanciaObjeto, PosicaoGeografica, Sugestao, TipoImagem
from django.core import serializers
from forms import AventuraForm, AventuraWithoutFieldsForm, InstanciaObjetoCreateForm, PosicaoGeograficaCreateForm, InstanciaObjetoUpdateForm
from django.core.context_processors import request
from django.http import HttpResponse
import json
from core.ajax import AjaxableResponseMixin
import os

SESSION_AVENTURA = '_user_aventura_id'

#assumindo que a criação de aventuras não seja colaborativa
SESSION_INSTANCIA = '_instancia_aventura'

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
        #self.object = form.save()    
        self.object.save()
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


#Retorna uma lista contento o id e nome do objeto,  e id do seu icone
class ObjetoGetJsonView(ListView):
    model = Objeto

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(serializers.serialize('json', Objeto.objects.all().filter(tipo_objeto=self.kwargs['pk']), fields=('pk','nome', 'icone_objeto','dialogo',)))
    

'''
================================================================================
                          Views para Instância do Objeto
                    
Instância do Objeto é criada no momento em que o objeto é arrastado para o mapa.
=================================================================================
'''

#cria a instancia do objeto por meio de um POST com json
class InstanciaObjetoCreateView(AjaxableResponseMixin, CreateView):  
    #template_name = 'editor_objetos/instancia_objeto/create.html'
    model = InstanciaObjeto
    form_class = InstanciaObjetoCreateForm
    
    def get_success_url(self):
        return reverse('gmaps_view') 
    
    def form_valid(self, form,*args, **kwargs):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).,
        # json print self.request.body
        pos = json.loads(self.request.body)#get json post
        #recupera quantidade do objeto
        object_list = Objeto.objects.all().filter(pk=pos[0]['id_objeto'])
        
        qntde = 0
        id_tipo = 0
        #recupera quantidade
        for obj in object_list:#always return one object, because the id/pk is unique
            qntde = obj.quantidade
            id_tipo = obj.tipo_objeto_id
        #utilizado no if de comparacao a seguir
        #usa id_objeto e id_aventura para recuperar instâncias do objeto
        #em seguida verifica a instancia com maior instancia_cont e verifica se é possível criar uma nova instância.
        #recupero instancias do objeto de uma dada aventura
        object_list = InstanciaObjeto.objects.all().filter(aventura_id=self.request.session[SESSION_AVENTURA].id, objeto_id=pos[0]['id_objeto'])
        flag = False #permissão para criar outra instancia
        
        #permissao para criar mais instancias
        #qntde_new_inst_obj = 0
        #if not  object_list:
        #    qntde_new_inst_obj = 1
        #else:
        #    for obj in object_list:
        #        if obj.instancia_cont == int(qntde):
        #            flag = True
        #        if obj.instancia_cont >= qntde_new_inst_obj:
        #            qntde_new_inst_obj = obj.instancia_cont + 1;
        
        #calcula a quantidade de instancias
        qnt_total_instancias = 0;
        for obj in object_list:
            qnt_total_instancias += 1;
            
        if qnt_total_instancias >= int(qntde):
            flag = True
            
        
        #salva objeto
        data_return = {'pk': 0,}
        if flag == False:
            form.instance.nome = pos[0]['nome']
            form.instance.objeto_id = pos[0]['id_objeto']
            form.instance.aventura_id =  self.request.session[SESSION_AVENTURA].id
            #form.instance.instancia_cont = qntde_new_inst_obj
            self.object = form.save()
            response = super(AjaxableResponseMixin, self).form_valid(form)
            
            object_list = TipoObjeto.objects.all().filter(pk=id_tipo)
           
            qntde_pos = 1
            for obj in object_list:
                qntde_pos = obj.posicoes_geograficas
               
            data_return = {'pk': self.object.id,'qntde_pos':qntde_pos,}
            
            
        #retorna data com id do objeto
        if self.request.is_ajax():
            return self.render_to_json_response(data_return)
        else:
            return response  
    
class InstanciaObjetoGetJsonView(ListView):
    model = InstanciaObjeto

    #funcao que retorna todas instâncias de objetos de uma dada aventura, com um campo adiciona com a url do icone (json)
    def render_to_response(self, context, **response_kwargs):
        
        #recupero instancias de uma dada aventura
        flag = 0;
        flagTwo = 0;
        inst_object_list = InstanciaObjeto.objects.all().filter(aventura_id=self.kwargs['pk'])#id e nome
        json_inst_objetos = '[';
        #qntde_pos = 0;
        json_inst_pos = '';
        for inst_obj in inst_object_list:     
            #inst_object_list = InstanciaObjeto.objects.all().filter(aventura_id=self.kwargs['pk'])
            #objeto_list = Objeto.objects.all().filter(pk=inst_obj.objeto_id)#icone_objeto_id
            if flag == 0:
                flag = 1;
                json_inst_objetos += '{"id":"' + str(inst_obj.pk) + '"' + ',"nome":"' + inst_obj.nome + '"';#id e nome da instancia
            else:
                json_inst_objetos += ',{"id":"' + str(inst_obj.pk) + '"' + ',"nome":"' + inst_obj.nome + '"';#id e nome da instancia
            objeto_list = Objeto.objects.all().filter(pk=inst_obj.objeto_id)#icone_objeto_id
            pos_list = PosicaoGeografica.objects.all().filter(instancia_objeto_id=inst_obj.pk)
            for obj in objeto_list:
                icone_list = Icone.objects.all().filter(pk=obj.icone_objeto_id)
                for icone in  icone_list:
                    json_inst_objetos += ',"url_icone":"/media/' + str(icone.icone) + '"';
                tipo_list = TipoObjeto.objects.all().filter(pk=obj.tipo_objeto_id)
                for tipo in tipo_list:
                    json_inst_pos += ',"posicoes_geograficas":"' + str(tipo.posicoes_geograficas) + '"';
            #for pos in pos_list:
            #    qntde_pos = qntde_pos+1;
            json_inst_pos += ',"pos":[';
            for pos in pos_list:
                if flagTwo == 0:
                    flagTwo = 1;
                    #json_inst_pos += "{'lat':'" + str(pos.latitude) + "'" + ",'lng':'" +str(pos.longitude) + "'"+  ",'altd':'" + str(pos.altitude) + "'}"; 
                    json_inst_pos += '{"id_pos":"' + str(pos.pk) + '"' +  ',"lat":"'  + str(pos.latitude) + '"' + ',"lng":"' +str(pos.longitude) + '"'+  ',"altd":"' + str(pos.altitude) + '"}';    
                else:
                    json_inst_pos += ',{"id_pos":"' + str(pos.pk) + '"' +  ',"lat":"'  +  str(pos.latitude) + '"' + ',"lng":"' +str(pos.longitude) + '"'+  ',"altd":"' + str(pos.altitude) + '"}';      
            json_inst_pos += ']}';
            json_inst_objetos += str(json_inst_pos); #"}"
            json_inst_pos = "";
            flagTwo = 0;
             
        
        json_inst_objetos += ']';
        
        return HttpResponse(json_inst_objetos)

class InstanciaObjetoUpdateView(UpdateView):
    template_name = 'editor_objetos/instancia_objeto/update.html'
    model = InstanciaObjeto
    form_class = InstanciaObjetoUpdateForm
    #success_url = "success-url"
    
    #def get_object(self):
    #    return Objeto.objects.get(pk=self.request.GET.get('pk'))
    #def get_success_url(self):
    #    return reverse('gmaps_view')
    
    def form_valid(self, form):
        
        self.object = form.save()  
        #return HttpResponseRedirect(self.get_success_url())
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")
    
class InstanciaObjetoDeleteView(DeleteView):
    #template_name = 'editor_objetos/instancia_objeto/update.html'
    model = InstanciaObjeto;
    
    #Override no delete para retornar uma resposta json caso o objeto seja deletado com sucesso
    def delete(self, request, *args, **kwargs):
 
        
        self.object = self.get_object()

        #if not object_list:   
        self.object.delete()
        #else:
        #    ValidationError
        #    messages.error(request, "".join("Não é possível deletar o objeto " + self.object.nome) + ", pois existem instâncias deste objeto!")
        #    return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
    
        return HttpResponse(json.dumps({'response': 'delete'}), content_type="application/json")
    
        #def get_success_url(self):
        #    return reverse('gmaps_view') 
    
'''
================================================================================
                          Views para Posicao Geografica
=================================================================================
'''

#Cria a posição geográfica para o objeto
class PosicaoGeograficaCreateView(AjaxableResponseMixin, CreateView):  
    #template_name = 'editor_objetos/instancia_objeto/create.html'
    model = PosicaoGeografica
    form_class = PosicaoGeograficaCreateForm
    
    def get_success_url(self):
        return reverse('gmaps_view') 

    
    def form_valid(self, form,*args, **kwargs):
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

#Atualiza a posicao geográfica do objeto
class PosicaoGeograficaUpdateView(AjaxableResponseMixin, UpdateView):  
    #template_name = 'editor_objetos/instancia_objeto/create.html'
    model = PosicaoGeografica
    form_class = PosicaoGeograficaCreateForm
    
    def get_success_url(self):
        return reverse('gmaps_view') 

    
    def form_valid(self, form,*args, **kwargs):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).,
        # json print self.request.body
        pos = json.loads(self.request.body)

        form.instance.latitude = pos[0]['latitude']
        form.instance.longitude = pos[0]['longitude']
        #form.instance.instancia_objeto_id = pos[0]['instancia_objeto_id']
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
        
#Retorna json contendo dados da posicao de uma instância, ou conjunto de posicoes
class PosicaoGeograficaGetJsonView(ListView):
    model = PosicaoGeografica
    
    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(serializers.serialize('json', PosicaoGeografica.objects.all().filter(instancia_objeto_id=self.kwargs['pk'])))#utiliza o id da instância

#delete posicao geográfica de um marcador
class PosicaoGeograficaDeleteView(DeleteView):
    model = PosicaoGeografica;
    
    def delete(self, request, *args, **kwargs):
 
        self.object = self.get_object()
        #verifica a quantidade de marcadores da instância.
        #caso a quantidade seja <= 1 a instância também é deletada.
        
       
        
        objetct_markers_list = PosicaoGeografica.objects.all().filter(instancia_objeto_id = self.object.instancia_objeto_id)
        
        qnde_markers = 0;
        for obj in objetct_markers_list:
            qnde_markers = qnde_markers + 1;
            
        data = 0;
        if qnde_markers <= 1:
            data = 1;
        #objetct_instance_list = InstanciaObjeto.objects.all().filter(pk=)
        
       
        self.object.delete()
   
        return HttpResponse(json.dumps({'response': data}), content_type="application/json")
    
'''
====================================================================
                        Views para GMapView
====================================================================                   

'''
class GMapView(TemplateView):
    template_name = 'editor_objetos/gmap/gmap.html'
 
#abre modal para informar ao usuário que a posição da aventura foi salva com sucesso   
class MsgShowView(TemplateView):
    template_name = 'editor_objetos/gmap/pos_aventura.html'
    
    #def get_success_url(self):
        #return HttpResponseRedirect(self.get_success_url())
        #return HttpResponse(json.dumps({'response' : 'ok'}), content_type="application/json")
    
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
        #atualiza sessao
        self.request.session[SESSION_AVENTURA] = self.object
        
        nome = self.request.session[SESSION_AVENTURA].nome
        id_av = self.request.session[SESSION_AVENTURA].id
       
        return HttpResponse(json.dumps({'response': nome ,'id' : id_av }), content_type="application/json")

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
        id_av = self.request.session[SESSION_AVENTURA].id
        if self.request.session[SESSION_AVENTURA] == '-1':
            ValidationError
            messages.error(request, "".join("Ocorreu um problema ao ativar a aventura! Tente novamente!"))
            return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        return HttpResponse(json.dumps({'response': nome ,'id' : id_av }), content_type="application/json")



#Atualizar posição aventura
class AventuraUpdatePositionView(AjaxableResponseMixin, UpdateView):
    #template_name = 'editor_objetos/aventura/message.html'
    model = Aventura
    form_class = AventuraWithoutFieldsForm
    
    def get_success_url(self):
        return reverse('gmaps_view')

    
    def form_valid(self, form,*args, **kwargs):
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
    



#Deleção da aventura
class AventuraDeleteView(DeleteView):
    template_name = 'editor_objetos/aventura/delete.html'
    model = Aventura
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        #verifica se a aventura está em autoria
        id_av = ''
        if self.request.session[SESSION_AVENTURA] == '-1':#sem aventura
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

    
    
#Retorna json contendo dados da aventura
class AventuraGetJsonView(ListView):
    model = Aventura
    
    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(serializers.serialize('json', Aventura.objects.all().filter(pk=self.kwargs['pk'])))
    
    
''''
====================================================================
                        Views para Sugestao
====================================================================
'''
#Lista todas sugestões
class SugestaoListView(ListView):
    template_name = 'editor_objetos/sugestao/listar.html'
    model = Sugestao

#criação de sugestão
class SugestaoCreateView(CreateView):
    template_name = 'editor_objetos/sugestao/create.html'
    model = Sugestao
   
    #redireciona a requisição
    def get_success_url(self):
        return reverse('sugestao_list_view')
    
    #Override no form
    def form_valid(self, form):
        #arquivos devem ser txt, jpeg, png ou fbx (extensões de objetos 3D para Wikitude SDK Android para AR)
        tipo = form.cleaned_data['tipo']#recupera tipo de sugestao
        arquivo = form.cleaned_data['sugestao']#recupera file
        if arquivo:
            if tipo == 'STX':
                #valida arquivo de texto para salvar sugestao
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
                #valida arquivo de audio para salvar sugestao
                #if not file.content-type in ["audio/mpeg","audio/..."]:
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
                #valida imagem para salvar
                if not os.path.splitext(arquivo.name)[1] in [".png",".jpeg",".jpg"]:
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

        #file = self.cleaned_data.get('audio_file',False)
        #print file 
        self.object = form.save()   
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

#update sugestao
class SugestaoUpdateView(UpdateView):
    template_name = 'editor_objetos/sugestao/update.html'
    model = Sugestao
    
    #redireciona a requisição
    def get_success_url(self):
        return reverse('sugestao_list_view')
    
    #Override no form
    def form_valid(self, form):
        #arquivos devem ser txt, jpeg, png ou fbx (extensões de objetos 3D para Wikitude SDK Android para AR)
        tipo = form.cleaned_data['tipo']#recupera tipo de sugestao
        arquivo = form.cleaned_data['sugestao']#recupera file
        
        if hasattr(arquivo,"content_type"):
            if tipo == 'STX':
                #valida arquivo de texto para salvar sugestao
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
                #valida arquivo de audio para salvar sugestao
                #if not file.content-type in ["audio/mpeg","audio/..."]:
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
                #valida imagem para salvar
                if not os.path.splitext(arquivo.name)[1] in [".png",".jpeg",".jpg"]:
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

        #self.object = form.save() 
        self.object.save()  
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")

#delete sugestao
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
        #return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('sugestao_list_view') 
    
    
''''
====================================================================
                        Views para TipoImagem
====================================================================
'''
#listagem das imagens
class TipoImagemListView(ListView):
    template_name = 'editor_objetos/tipo_imagem/listar.html'
    model = TipoImagem

    
#create TipoImagem
class TipoImagemCreateView(CreateView):
    template_name = 'editor_objetos/tipo_imagem/create.html'
    model = TipoImagem
    
    #Override no form
    def form_valid(self, form):
        #arquivos devem ser txt, jpeg, png ou fbx (extensões de objetos 3D para Wikitude SDK Android para AR)
        tipo = form.cleaned_data['tipo']#recupera tipo de imagem
        arquivo = form.cleaned_data['img_play']#recupera file
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
                if not os.path.splitext(arquivo.name)[1] in [".png",".jpeg",".jpg"]:
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

#atualiza imagem  
class TipoImagemUpdateView(UpdateView):
    template_name = 'editor_objetos/tipo_imagem/update.html'
    model = TipoImagem
    
    def get_success_url(self):
        return reverse('tipo_imagem_list_view')
    
    def form_valid(self, form):
        #arquivos devem ser txt, jpeg, png ou fbx (extensões de objetos 3D para Wikitude SDK Android para AR)
        tipo = form.cleaned_data['tipo']#recupera tipo de imagem
        arquivo = form.cleaned_data['img_play']#recupera file
        if hasattr(arquivo,"content_type"):
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
                if not os.path.splitext(arquivo.name)[1] in [".png",".jpeg",".jpg"]:
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

#delete imagem
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
        return reverse('sugestao_list_view') 