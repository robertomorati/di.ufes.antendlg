# -*- coding: utf-8 -*-
'''
Created on 23/10/2013

@author: Roberto Gumarães  Morati Junior
'''
from django import forms
from editor_objetos.models import Aventura, Autor, PosicaoGeografica, InstanciaObjeto, Objeto
from django.forms.extras.widgets import SelectDateWidget
from datetime import date
from django.utils.translation import ugettext_lazy as _


'''
Form para Objeto
'''
class ObjetoForm(forms.ModelForm):
    class Meta:
        model = Objeto


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
Form utilizado para salvar aventura na session
'''
class AventuraWithoutFieldsForm(forms.ModelForm):
    class Meta:
        model = Aventura
        exclude = ['nome','descricao','inicio','fim','longitude','autor','latitude',]

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
        exclude = ['is_staff','is_active','is_superuser','last_login','date_joined','groups','user_permissions','id_password1','id_password2',]
        
'''
Form utilizado para criar instancia do objeto
'''
class InstanciaObjetoCreateForm(forms.ModelForm):
    class Meta:
        model = InstanciaObjeto
        exclude = ['nome','proximidade','encenacao','objeto','visivel','sugestao','num_instancia','aventura','instancia_cont',]

'''
Form utilizado para criar POS
'''
class   PosicaoGeograficaCreateForm(forms.ModelForm):
    class Meta:
        model = PosicaoGeografica
        exclude = ['latitude','longitude','altitude','instancia_objeto',] 
        
        
'''
Form para Update Instancia de Objeto
'''
class InstanciaObjetoUpdateForm(forms.ModelForm):  
    class Meta: 
        model = InstanciaObjeto
        #model.dialogo = forms.CharField(label=_("Diálogo"), widget=forms.Textarea(attrs={'cols': 40, 'rows': 5,'style':"width: 500px; height: 100px;"}))
        exclude = ['objeto','aventura','instancia_cont',]  

    nome = forms.CharField(label=_("Nome"), max_length=30, widget=forms.TextInput(attrs={'style' : 'width: 90px'}))
    proximidade = forms.IntegerField(label=_("Proximidade"), widget=forms.TextInput(attrs={'style' : 'width: 20px'}))
    dialogo = forms.CharField(label=_("Diálogo"), widget=forms.Textarea(attrs={'cols': 40, 'rows': 5,'style':"width: 500px; height: 100px;"}))
    
    #torna o campo field oculto
    def __init__(self,  *args, **kwargs):
        super(InstanciaObjetoUpdateForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)  
        object_list = Objeto.objects.all().filter(pk=instance.objeto.id) 
        for obj in object_list:
            if obj.dialogo == False:
                self.fields['dialogo'].widget = forms.HiddenInput()
            else:
                dialogo = "<dialogo id_instancia='" + str(instance.id) + "' nome='"+ instance.nome +"'>\n"
                #dialogo +="<npc tipo='dialogoInicial'>\n Digite a fala inicial do personagem aqui.\n </npc>"
                #dialogo +="<avatar tipo='confirmacao'>\nDigite a fala do jogador aqui.\n"
                #dialogo +='<npc tipo="dialogoFinal">\nApós uma fala do jogador, o dialogo entre o mesmo e o npc pode acabar. Assim, tem-se dialogoFinal\n</npc>'
                #'\n</avatar>'
                #dialogo +="\n<avatar tipo='negacao'>\nDigite a fala do jogador aqui.\n</avatar>"       
                dialogo +="\n</dialogo>" 
                self.initial ={'nome':instance.nome, 'dialogo': dialogo,'proximidade': instance.proximidade,
                               'encenacao':instance.encenacao,'sugestao':instance.sugestao,'visivel':instance.visivel}