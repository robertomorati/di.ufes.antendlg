'''
Created on 23/10/2013

@author: Roberto
'''
from django import forms
from editor_objetos.models import Aventura, Autor
from django.forms.extras.widgets import SelectDateWidget
from datetime import date
from django.utils.translation import ugettext_lazy as _
#from django.contrib.auth.models import User

class AventuraForm(forms.ModelForm):
    class Meta:
        model = Aventura
        exclude = ['latitude','longitude','autor',]
        fim =  forms.DateField(widget=SelectDateWidget(years=range(date.today().year, 2099)),)
        #autor = forms.IntegerField(widget=forms.IntegerField())
        #def __init__(self, *args, **kwargs):
        #    super(AventuraForm, self).__init__(*args, **kwargs)
        #    self.fields['fim'].widget = forms.DateField(widget=SelectDateWidget(years=range(date.today().year, 2099)),)


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Username"),
                               max_length=30, widget=forms.TextInput())
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(render_value=False))
 
 
class AutorForm(forms.Form):
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(render_value=False))
    #class Meta:
    #    model = Autor
    #    exclude = ['is_staff','is_active','is_superuser','last_login','date_joined','groups','user_permissions']











'''
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ('dica_senha', 'nickname')
'''
'''
class LoginForm(forms.ModelForm):
    class Meta:
        model = Autor
        username = forms.CharField(label=_("Username"), max_length=30, widget=forms.TextInput(),required=True)
        password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(render_value=False),required=True)

     
class LoginForm(forms.ModelForm):
    class Meta:
        model = Autor
        exclude = ['username','first_name','last_name','email','password','dica_senha','nickname']
        username = forms.CharField(label=_("Username"), max_length=30, widget=forms.TextInput(),required=True)
        password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(render_value=False),required=True)
'''