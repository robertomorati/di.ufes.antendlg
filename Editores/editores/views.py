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
from django.contrib.auth.views  import *
import json, re
SESSION_AVENTURA = '_user_aventura_id'

#from django.core.context_processors import csrf
#from django.shortcuts import render_to_response
from django.conf.urls import url
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter
#from rest_framework.compat import urls
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import views
from rest_framework import status
from rest_framework.authentication import *
from rest_framework import *


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
    
@sensitive_post_parameters()
@csrf_protect
@never_cache
def login_player(request, template_name='registration/login_player.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        print form
        if form.is_valid():
            
            # Ensure the user-originating redirection url is safe.
            #if not is_safe_url(url=redirect_to, host=request.get_host()):
            #    redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            
            user = form.get_user()       
            if not user or not user.is_active:
                '''
                ValidationError
                messages.error(request, "".join("Invalid username or incorrect password!"))
                return HttpResponseRedirect('/autenvldg_services/login_player/')
                msg = "Invalid username or incorrect password!"
                raise exceptions.AuthenticationFailed(msg)
                data = serializers.serialize('json', '"error_login":"Invalid username or incorrect password!"',)
                return Response(data, status=status.HTTP_200_OK)
                '''
                data = '[{"type_status":"error_login"},{"value": "Invalid username or incorrect password!"}]'
                return HttpResponse(data, content_type="application/json")
            else:
                if Autor.objects.all().filter(user_ptr_id = user.pk).exists():
                    '''
                    ValidationError
                    messages.error(request, "".join("Please, it's necessary use a player account to login."))
                    return HttpResponseRedirect('/autenvldg_services/login_player/')
                    return Response(serializers.serialize('json', '"error_login":"Please, it is necessary use a player account to login."',), status=status.HTTP_200_OK)
                    '''
                    data = '[{"type_status":"error_login"},{"value": "Please, it is necessary use a player account to login."}]'
                    return HttpResponse(data, content_type="application/json")
                auth_login(request, form.get_user())#log player to user services
            data = '[{"type_status":"success_login"},{"value":"' + request.COOKIES.get('csrftoken') + '"}]'
            return HttpResponse(data, content_type="application/json")
            #return HttpResponseRedirect('/autenvldg_services/')
        else:
            '''
            ValidationError
            messages.error(request, "".join("Please, verify if the username and password are correct. If the problem persists, contact the administrator: robertomorati@gmail.com."))
            return HttpResponseRedirect('/autenvldg_services/login_player/')
            response = Response(data, status=status.HTTP_200_OK)
            return response
            '''
            data = '[{"type_status":"error_login"},{"value": "Please, verify if the username and password are correct. If the problem persists, contact the administrator: robertomorati@gmail.com."}]'
            return HttpResponse(data, content_type="application/json")
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

    
    
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
        

        #TODO: melhorar         
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
