# -*- coding: utf-8 -*-
'''
Created on 23/10/2013

@author: Roberto Gumarães  Morati Junior
'''
from django import forms 
from editor_objetos.models import Aventura, Autor, PosicaoGeografica, InstanciaObjeto, Objeto, TipoImagem, Icone, Missao, Avatar,CondicaoObjeto,CondicaoDialogo,CondicaoJogador
    
from django.forms.extras.widgets import SelectDateWidget 
from django.forms.models import ModelChoiceField
from datetime import date
from django.utils.translation import ugettext_lazy as _



'''
Forms para Listagem de Condições 
'''
class CondicoesObjetosFielForm(ModelChoiceField):
    def label_from_instance(self,obj):
        return obj.get_nome_instancia()
    
class CondicoesObjetosListagemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CondicoesObjetosListagemForm, self).__init__(*args, **kwargs)
        
        self.fields['ligacao']  = CondicoesObjetosFielForm()
        
        
'''
Forms para Ajustar Templates/Forms para Criação de Condinções
'''
class CondicaoObjetoModelChoiceField(ModelChoiceField):
    def label_from_instance(self,obj):
        return obj.get_nome_instancia()

#Condições Objetos 
class CondicaoObjetoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CondicaoObjetoForm, self).__init__(*args, **kwargs)
           
        #recupera id da aventura
        self.aventura_id = kwargs['initial']['aventura_id']
        object_list = Objeto.objects.filter(coletavel= True)

        #Recuperando Instâncias
        self.fields['prefixo'].label = 'Instâncias'
        flag = 0;
        buffer_inst = '';
        for obj in object_list:
            if flag == 0:
                buffer_inst = InstanciaObjeto.objects.filter(objeto_id=obj.id,aventura_id=self.aventura_id)
                flag = 1;
            elif flag == 1:
                buffer_inst = buffer_inst | InstanciaObjeto.objects.filter(objeto_id=obj.id);# | concatena apenas QuerySet
        
        #Carregando Instâncias
        self.fields['prefixo']  = InstanciaObjetoRoleModelChoiceField(queryset=buffer_inst,)
        self.fields['prefixo'].required = True
        
        #Carregando Instâncias
        self.fields['sufixo'].label = 'Instâncias'
        self.fields['sufixo']  = InstanciaObjetoRoleModelChoiceField(queryset=buffer_inst,)
        self.fields['sufixo'].required = True
    
    class Meta: 
        model = CondicaoObjeto


class CondicaoJogadorModelChoiceField(ModelChoiceField):
    def label_from_instance(self,obj):
        return obj.get_nome_avatar()
    
#Ajusta forms para condições entre jogadores e instâncias de objetos coletáveis.        
class CondicaoJogadorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CondicaoJogadorForm, self).__init__(*args, **kwargs)

        #recupera id da aventura para recuperar instãncias daquela aventura
        self.aventura_id = kwargs['initial']['aventura_id']
        object_list = Objeto.objects.filter(coletavel= True)
        
        self.fields['sufixo'].label = 'Instâncias'
        
        #recueprando instâncias
        flag = 0;
        buffer_inst = '';
        for obj in object_list:
            if flag == 0:
                buffer_inst = InstanciaObjeto.objects.filter(objeto_id=obj.id,aventura_id=self.aventura_id)
                flag = 1;
            elif flag == 1:
                buffer_inst = buffer_inst | InstanciaObjeto.objects.filter(objeto_id=obj.id);# | concatena apenas QuerySet
        
        #carregando instâncias
        self.fields['sufixo']  = InstanciaObjetoRoleModelChoiceField(queryset=buffer_inst,)
        self.fields['sufixo'].required = True
        
        #recupernado e carregando avatares da aventura
        self.fields['prefixo'].label = 'Avatar'
        self.fields['prefixo']  = CondicaoJogadorModelChoiceField(queryset=Avatar.objects.filter(aventura_avatar_id=self.aventura_id))
        self.fields['prefixo'].required = True
        
    class Meta: 
        model = CondicaoJogador


class CondicaoDialogoModelChoiceField(ModelChoiceField):
    def label_from_instance(self,obj):
        return obj.get_nome_avatar()

#Condições de avatares com diálogos de personagens        
class CondicaoDialogoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CondicaoDialogoForm, self).__init__(*args, **kwargs)
        
        
        #recupera id da aventura
        self.aventura_id = kwargs['initial']['aventura_id']
        object_list = Objeto.objects.filter(coletavel= False, dialogo = True, )
        
        #recuperar instâncias que possuem diálogo como ativado.
        self.fields['referencia_sufixo'].label = 'Instância Referência'
        flag = 0;
        buffer_inst = '';
        for obj in object_list:
            if flag == 0:
                buffer_inst = InstanciaObjeto.objects.filter(objeto_id=obj.id,aventura_id=self.aventura_id,)
                flag = 1;
            elif flag == 1:
                buffer_inst = buffer_inst | InstanciaObjeto.objects.filter(objeto_id=obj.id,aventura_id=self.aventura_id, )# | concatena apenas QuerySet
        
        self.fields['referencia_sufixo']  = InstanciaObjetoRoleModelChoiceField(queryset=buffer_inst,)
        self.fields['referencia_sufixo'].required = True
        
        self.fields['prefixo'].label = 'Avatar'
        self.fields['prefixo']  = CondicaoDialogoModelChoiceField(queryset=Avatar.objects.filter(aventura_avatar_id=self.aventura_id))
        self.fields['prefixo'].required = True
        
    class Meta: 
        model = CondicaoDialogo

        
'''
Form para Criar Papeis
'''

class InstanciaObjetoRoleModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_nome_instancia()


class AvatarRoleListForm(forms.ModelForm):  
    def __init__(self,  *args, **kwargs):
        super(AvatarRoleListForm, self).__init__(*args, **kwargs)
        #get_nome_tipo_imagem
        self.fields['inst_objeto'].label = 'Instância Objeto'
        self.fields['inst_objeto']  = InstanciaObjetoRoleModelChoiceField(queryset=InstanciaObjeto.objects.filter(encenacao='AV'),)
        self.fields['inst_objeto'].required = False
        
    class Meta: 
        model = Avatar
        exclude = ['publico','longitude','latitude','aventureiro','aventura_avatar','avatar']  
    
'''
Form para CreateAvatar
'''
class CreateAvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        exclude = ['longitude','latitude','aventureiro','aventura_avatar','inst_objeto',]
        
        
'''
Form para CreateMissao
'''
class CreateMissaoForm(forms.ModelForm):
    class Meta:
        model = Missao
        exclude = ['aventuras',]

'''
Form para Update Objeto - Customizando selec icone
'''
class IconeModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_nome_icone()
     
class UpdateObjetoForm(forms.ModelForm):
    class Meta:
        model = Objeto
        
    def __init__(self,  *args, **kwargs):
        super(UpdateObjetoForm, self).__init__(*args, **kwargs)
        self.fields['icone_objeto'] = IconeModelChoiceField(queryset=Icone.objects.filter(),)
        #forms.ModelChoiceField(queryset=TipoImagem.objects.filter(tipo='IM'))
       
            

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
class  PosicaoGeograficaCreateForm(forms.ModelForm):
    class Meta:
        model = PosicaoGeografica
        exclude = ['latitude','longitude','altitude','instancia_objeto',] 
        
        
'''
Form para Update Instancia de Objeto
'''
class InstanciaObjetoModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_nome_tipo_imagem()

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
        
        #get_nome_tipo_imagem
        self.fields['imagem_mapa'] = InstanciaObjetoModelChoiceField(queryset=TipoImagem.objects.filter(tipo='IC'),)
        self.fields['imagem_camera'] = InstanciaObjetoModelChoiceField(queryset=TipoImagem.objects.filter(tipo='IM'),)
        self.fields['imagem_mapa'].required = False
        self.fields['imagem_camera'].required = False
        self.fields['sugestao_objeto'].required = False
        object_list = Objeto.objects.all().filter(pk=instance.objeto.id)
        dialog_tam = int(len(instance.dialogo))
        for obj in object_list:
            if obj.dialogo == False:
                #self.fields['dialogo'].widget = forms.HiddenInput()
                self.fields.pop('dialogo')
            else:
                if dialog_tam > 80:#xml editado tem tamanho superior a 80
                    dialogo = "<dialogo id_instancia='" + str(instance.id) + "' nome='"+ instance.nome +"'>\n"
                    #dialogo +="<npc tipo='dialogoInicial'>\n Digite a fala inicial do personagem aqui.\n </npc>"
                    #dialogo +="<avatar tipo='confirmacao'>\nDigite a fala do jogador aqui.\n"
                    #dialogo +='<npc tipo="dialogoFinal">\nApós uma fala do jogador, o dialogo entre o mesmo e o npc pode acabar. Assim, tem-se dialogoFinal\n</npc>'
                    #'\n</avatar>'
                    #dialogo +="\n<avatar tipo='negacao'>\nDigite a fala do jogador aqui.\n</avatar>"       
                    dialogo +="\n</dialogo>" 
                    self.initial ={'nome':instance.nome, 'dialogo': dialogo,'proximidade': instance.proximidade,
                                   'encenacao':instance.encenacao,'sugestao':instance.sugestao_objeto,'visivel':instance.visivel}