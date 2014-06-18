# -*- coding: utf-8 -*-
'''
Created --/--/2013

Autor: Roberto Guimarães Morati Junior
'''
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import FormView, CreateView, ListView
from editor_objetos.models import Autor
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.urlresolvers import reverse
from core.forms import LoginForm, AutorForm
from django.core import serializers
from  django.contrib.auth import *
import json
SESSION_AVENTURA = '_user_aventura_id'

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
    return HttpResponseRedirect('/autendlg/login/')

'''
LoginView - autenticação do usuário
'''
class LoginView(FormView):
  
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = "/autendlg/"
    
    def get(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        return self.render_to_response(self.get_context_data(form=form, **kwargs))       
   
    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if not form.is_valid():
            return self.get(request, *args, **kwargs)
        user = authenticate(username=form.cleaned_data["username"],
                            password=form.cleaned_data["password"])
        if not user or not user.is_active:
        #return self.get(request, *args, **kwargs)
        #return HttpResponse(json.dumps({'response': 'erro login'}), content_type="text")
            ValidationError
            messages.error(request, "".join("Usuário ou senha incorretos!"))
            return self.get(request, *args, **kwargs)
        #else: 
            #request.session['user'] = form.cleaned_data["username"]
            #print request.session['user']
            #print request.session['user']
            
        
        # Persist user
        #
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
        #return render_to_response('index.html', data, context_instance=RequestContext(request)) 
        
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
          
        #json.dumps() transforma objeto em string JSON e, json.loads() transforma string JSON em objeto    
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
