'''
Created on 16/06/2014

@author: Roberto
'''

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from editor_objetos.models import CalcClass


class MyRESTView(APIView):

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



# REST: Classe que implementa as chamadas para listar e criar enquetes
#class AventuraViewSet(APIView):
   # "Lista as enquetes cadastradas"
    #def get(self, request):
        # Pega todas as enquetes
       # aventuras = Aventura.objects.all()
     #   print aventuras
        # Retorna uma lista de enquetes (dicionario contendo id, pergunta e url da API para ver mais dados sobre a enquete)
      #  return [{'id': p.id, 'nome': (p.nome), 'url': reverse('aventuras-resource', args=(p.id,))} for p in aventuras]