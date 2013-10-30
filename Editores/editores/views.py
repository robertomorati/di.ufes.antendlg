# -*- coding: utf-8 -*-
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
#from django.contrib.auth.models import User
#from django.contrib.auth.hashers import PBKDF2PasswordHasher
#from django.contrib.auth.models import User
import json

'''
Página inicial
'''
class IndexView(TemplateView):
    template_name = 'index.html'

    
  
'''
Autenticação

Pendencias: mudar para Class
'''
def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
   
    logout(request)
    #request.session['user'].flush()
    return HttpResponseRedirect('/autendlg/login/')



#class Login(DetailView):
#    template_name = 'login.html'
#    model = Autor
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
        login(request, user)
        #return HttpResponseRedirect(self.get_success_url())
        #data = {}
        return HttpResponseRedirect(self.get_success_url())
        #return render_to_response('index.html', data, context_instance=RequestContext(request)) 

class LoginCreateView(CreateView):
    success_url =  'login'
    template_name = 'registration/registration.html'
    form_class = AutorForm
  
    
    def get_success_url(self):
        return reverse('login')
    #Override no form. 
    def form_valid(self, form):
        #User.set_password(self.kwargs['password'])
        #Autor.set_unusable_password(self)
        
        #user = super(Autor, self).save(commit=False)
        #user.set_password(self.cleaned_data["password"])
        #user.save()
        self.object = form.save()
          
        #json.dumps() transforma objeto em string JSON e, json.loads() transforma string JSON em objeto    
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")



'''
Autor
'''
class AutorGetJsonView(ListView):
    #template_name = 'editor_objetos/icones/buffer.html'
    model = Autor

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(serializers.serialize('json', Autor.objects.all().filter(pk=self.kwargs['pk']), fields=('icone_autor')))
