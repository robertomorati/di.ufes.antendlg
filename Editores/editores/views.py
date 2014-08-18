# -*- coding: utf-8 -*-
'''
Created --/--/2013

Autor: Roberto Guimarães Morati Junior
'''
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import FormView, CreateView, ListView
from editores.models import Autor
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.urlresolvers import reverse
from core.forms import LoginForm, AutorForm
from django.core import serializers
from  django.contrib.auth import *
import json
SESSION_AVENTURA = '_user_aventura_id'

#from django.core.context_processors import csrf
#from django.shortcuts import render_to_response

from rest_framework.response import Response
from rest_framework.routers import SimpleRouter
from rest_framework.compat import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import views

#override DefaultRouter
class DefaultRouter(SimpleRouter):
    """
    The default router extends the SimpleRouter, but also adds in a default
    API root view, and adds format suffix patterns to the URLs.
    """
    include_root_view = True
    include_format_suffixes = True
    root_view_name = 'api-root'

    def get_api_root_view(self):
        """
        Return a view to use as the API root.
        """
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        class APIRoot(views.APIView):
            _ignore_model_permissions = True

            def get(self, request, format=None):
                ret = {}
                for key, url_name in api_root_dict.items():
                    ret[key] = reverse(url_name, request=request, format=format)
                return Response(ret)

        return APIRoot.as_view()

    def get_urls(self):
        """
        Generate the list of URL patterns, including a default root view
        for the API, and appending `.json` style format suffixes.
        """
        urls = []

        if self.include_root_view:
            root_url = url(r'^autenvldg_services/$', self.get_api_root_view(), name=self.root_view_name)
            urls.append(root_url)

        default_urls = super(DefaultRouter, self).get_urls()
        urls.extend(default_urls)

        if self.include_format_suffixes:
            urls = format_suffix_patterns(urls)

        return urls
'''
Página inicial
'''
class IndexView(TemplateView):
    template_name = 'index.html'

    
  
'''
======================================================================
                            Autenticação
======================================================================
'''
'''
Logout do usuário

Pendencias: mudar para Class
'''
def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/autenvldg/login/')

'''
LoginView - autenticação do usuário
'''
class LoginView(FormView):
  
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = "/autenvldg/"
    
    def get(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        return self.render_to_response(self.get_context_data(form=form, **kwargs))       
   
    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if not form.is_valid():
            return self.get(request, *args, **kwargs)
        user = authenticate(username=form.cleaned_data["username"],
                            password=form.cleaned_data["password"])
        #melhorar
        
         
        if not user or not user.is_active:
            ValidationError
            messages.error(request, "".join("Invalid username or incorrect password !"))
            return self.get(request, *args, **kwargs)
      
        else:
            if not Autor.objects.all().filter(user_ptr_id = user.pk):
                ValidationError
                messages.error(request, "".join("It's a player account!"))
                return self.get(request, *args, **kwargs)
            
        # Persist user
        #login(request, user)
        #override login auth
        def login(request, user):
            """
            Persist a user id and a backend in the request. This way a user doesn't
            have to reauthenticate on every request. Note that data set during
            the anonymous session is retained when the user logs in.
            """
            if user is None:
                user = request.user
        # TODO: It would be nice to support different login methods, like signed cookies.
        #Autenticando usuário na seção
        if SESSION_KEY in request.session:
            if request.session[SESSION_KEY] != user.id:
                # To avoid reusing another user's session, create a new, empty
                # session if the existing session corresponds to a different
                # authenticated user.
                request.session.flush()
                request.session.set_expiry(600)
        else:
            request.session.cycle_key()
        request.session[SESSION_KEY] = user.id
        #SESSION_AVENTURA com -1 significa que não existe aventuras sendo editadas
        request.session[SESSION_AVENTURA] = '-1'
        request.session[BACKEND_SESSION_KEY] = user.backend
        if hasattr(request, 'user'):
            request.user = user
            user_logged_in.send(sender=user.__class__, request=request, user=user)
            
        #request.session[SESSION_KEY] = id_aventura
        #return HttpResponseRedirect(self.get_success_url())
        #data = {}
        return HttpResponseRedirect(self.get_success_url())
        #args = {}
        #args.update(csrf(request))
        #return render_to_response("/autendlg/", args) 
        
'''
LoginCreateView - criação de usuário
'''
class LoginCreateView(CreateView):
    success_url =  'login'
    template_name = 'registration/registration.html'
    form_class = AutorForm
  
    
    def get_success_url(self):
        return reverse('login')
    #Override no form. 
    def form_valid(self, form):
       
        self.object = form.save()
          

        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")



'''
=======================================================
                        Autor
=======================================================
'''
'''
AutorGerJsonView - retorna o avatar de um autor
'''
class AutorGetJsonView(ListView):
    #template_name = 'editor_objetos/icones/buffer.html'
    model = Autor

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(serializers.serialize('json', Autor.objects.all().filter(pk=self.kwargs['pk']), fields=('icone_autor')))
