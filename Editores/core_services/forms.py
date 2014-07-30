'''
Created on Jul 22, 2014

@author: robertomorati
'''

from django import forms 
from editor_objetos.models import Jogador
from rest_framework import serializers


class JogadorSerializer(serializers.ModelSerializer):
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    
    # criptografia senha autor
    def save(self, commit=True):
        user = super(JogadorSerializer, self).save()
        user.set_password(self.object.password)
        if commit:
            user.save()
            return user
    class Meta: 
        model = Jogador
        # remove parametros desnecessarios
        exclude = ['is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions', 'id_password1', 'id_password2', ]