'''
Created on 17/06/2014

@author: Roberto Guimaraes Morati Junior
'''

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.core import serializers
import json

from editor_objetos.models import CalcClass, Aventura

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
        response = Response(result, status=status.HTTP_200_OK)
        return response
    
#Teste para retornar lista de aventuras
class AventuraViewSet(APIView):
    
    "Lista as enquetes cadastradas"
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kw):
        #recupera todas as aventuras
        aventuras = Aventura.objects.all()

        #retornar as aventuras
        data = serializers.serialize('json', aventuras,)
        response = Response(data, status=status.HTTP_200_OK)
        return response