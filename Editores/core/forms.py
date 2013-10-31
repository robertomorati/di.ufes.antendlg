# -*- coding: utf-8 -*-
'''
Created on 23/10/2013

@author: Roberto Gumarães  Morati Junior
'''
from django import forms
from editor_objetos.models import Aventura, Autor
from django.forms.extras.widgets import SelectDateWidget
from datetime import date
from django.utils.translation import ugettext_lazy as _


'''
Form para Aventura
'''
class AventuraForm(forms.ModelForm):
    class Meta:
        model = Aventura
        exclude = ['latitude','longitude','autor',]
        fim =  forms.DateField(widget=SelectDateWidget(years=range(date.today().year, 2099)),)
        #autor = forms.IntegerField(widget=forms.IntegerField())
        #def __init__(self, *args, **kwargs):
        #    super(AventuraForm, self).__init__(*args, **kwargs)
        #    self.fields['fim'].widget = forms.DateField(widget=SelectDateWidget(years=range(date.today().year, 2099)),)

'''
Form para Login
'''
class LoginForm(forms.Form):
    username = forms.CharField(label=_("Username"),
                               max_length=30, widget=forms.TextInput())
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(render_value=False))
 
'''
Form  para criação de Autor
''' 
class AutorForm(forms.ModelForm):
    password = forms.CharField(label=_("Senha"), widget=forms.PasswordInput(render_value=False))
    
    #criptografia senha autor
    def save(self, commit=True):
        user = super(AutorForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            return user
    class Meta: 
        model = Autor
        #remove parametros desnecessarios
        exclude = ['is_staff','is_active','is_superuser','last_login','date_joined','groups','user_permissions','id_password1','id_password2']