# -*- coding: utf-8 -*-
'''
Created on 17/06/2014

@author: Roberto Guimaraes Morati Junior
'''

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers


from editor_objetos.models import CalcClass, Aventura
from editor_objetos.models import Objeto, Icone, TipoObjeto, InstanciaObjeto, PosicaoGeografica

from rest_framework import permissions


class MyRESTView(APIView):
    
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        get_arg1 = request.GET.get('arg1', None)
        get_arg2 = request.GET.get('arg2', None)

        # Any URL parameters get passed in **kw
        myClass = CalcClass(get_arg1, get_arg2, *args, **kw)
        result = myClass.do_work()
        print result
        response = Response(result, status=status.HTTP_200_OK)
        return response
    
"""
Retorna lista de aventuras por autor
"""
class AventuraView(APIView):
    
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kw):
        #recupera todas as aventuras
        aventuras = Aventura.objects.all().filter(autor=self.kwargs['autor_id'])

        #retornar as aventuras
        data = serializers.serialize('json', aventuras,)
        response = Response(data, status=status.HTTP_200_OK)
        return response
        #return HttpResponse(data, content_type="application/json")
    
    def post(self,request, *args, **kw):
        pass
"""
Retorna a lista de inst�ncia para uma dada aventura
"""
class InstanciasObjetoView(APIView):
    
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kw):
        
        #recuperando inst�ncias de objetos de uma determinada aventura
        flag = 0;
        flagTwo = 0;
        inst_object_list = InstanciaObjeto.objects.all().filter(aventura_id=kw['aventura_id'])#id e nome
        json_inst_objetos = '[';
     
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
        
        response = Response(json_inst_objetos, status=status.HTTP_200_OK)
        return response