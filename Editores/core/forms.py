# -*- coding: utf-8 -*-
'''
Created on 23/10/2013

@author: Roberto Gumarães  Morati Junior
'''
from django import forms 
from editor_objetos.models import Aventura, Autor, PosicaoGeografica, InstanciaObjeto, Objeto, TipoImagem, Icone, Missao, Avatar,\
    PosInstanciaAtiva, AvatarAtivo, MissaoAtiva, CondicaoAtiva
from editor_objetos.models import CondicaoInstanciaObjeto, CondicaoDialogoInstancia, CondicaoJogadorInstancia, CondicaoJogadorObjeto, Agente
from editor_objetos.models import Agressivo, Passivo, Colaborativo, Mensagem, Competitivo, AventuraAtiva
from editor_objetos.models import Enredo, EnredoFile, EnredoInstancia, EnredoMensagem
from django.forms.extras.widgets import SelectDateWidget 
from django.forms.models import ModelChoiceField
from datetime import date
from django.utils.translation import ugettext_lazy as _



'''
Forms para tratar listagem de condições
'''
# retorna o nome da instância do objeto
class CondicoesObjetosFielForm(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_nome_instancia()

# <NOTHING>
class CondicoesObjetosListagemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CondicoesObjetosListagemForm, self).__init__(*args, **kwargs)
        
        self.fields['ligacao'] = CondicoesObjetosFielForm()
        

'''
Forms para templates para criação de Condições
'''
# retorna o nome da instancia do objeto       
class CondicaoObjetoModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_nome_instancia()

# retorna nome da missao
class MissaoModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_nome_missao()
    
# retorna nome do enredo
class EnredoModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_nome_enredo()    

# Template para condições do objeto
class CondicaoInstanciaObjetoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CondicaoInstanciaObjetoForm, self).__init__(*args, **kwargs)
           
        # recupera id da aventura
        self.aventura_id = kwargs['initial']['aventura_id']
        
        object_list = Objeto.objects.filter(coletavel=True)

        # Recuperando Instâncias
        flag = 0;
        buffer_inst = '';
        for obj in object_list:
            if flag == 0:
                buffer_inst = InstanciaObjeto.objects.filter(objeto_id=obj.id, aventura_id=self.aventura_id)
                flag = 1;
            elif flag == 1:
                buffer_inst = buffer_inst | InstanciaObjeto.objects.filter(objeto_id=obj.id, aventura_id=self.aventura_id);  # | concatena apenas QuerySet
        
        self.fields['nome'].label = 'Name'
        self.fields['operador'].label = 'Logical Operator'
        self.fields['ligacao'].label = 'Link'
        
        # Carregando Instâncias
        self.fields['prefixo'] = InstanciaObjetoRoleModelChoiceField(queryset=buffer_inst,)
        self.fields['prefixo'].required = True
        self.fields['prefixo'].label = 'Instances'
        
        # Carregando missoes da aventura
        self.fields['missao'] = MissaoModelChoiceField(Missao.objects.filter(aventuras_id=self.aventura_id),)
        self.fields['missao'].required = True
        self.fields['missao'].label = 'Mission'

        # Carregando enredos da aventura
        self.fields['enredo'] = EnredoModelChoiceField(Enredo.objects.filter(aventura_id=self.aventura_id),)
        self.fields['enredo'].required = True
        self.fields['enredo'].label = 'Story'
        
        
        # Carregando Instâncias
        self.fields['sufixo'] = InstanciaObjetoRoleModelChoiceField(queryset=buffer_inst,)
        self.fields['sufixo'].required = True
        self.fields['sufixo'].label = 'Instances'
    
    class Meta: 
        model = CondicaoInstanciaObjeto


# retorna o nome do avatar
class CondicaoJogadorModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_nome_avatar()
    
# Ajusta templates para condições entre jogadores e instâncias de objetos coletáveis.        
class CondicaoJogadorInstanciaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CondicaoJogadorInstanciaForm, self).__init__(*args, **kwargs)

        # recupera id da aventura para recuperar instãncias da aventura
        self.aventura_id = kwargs['initial']['aventura_id']
        object_list = Objeto.objects.filter(coletavel=True)
             
        # recueprando instâncias
        flag = 0;
        buffer_inst = '';
        for obj in object_list:
            if flag == 0:
                buffer_inst = InstanciaObjeto.objects.filter(objeto_id=obj.id, aventura_id=self.aventura_id)
                flag = 1;
            elif flag == 1:
                buffer_inst = buffer_inst | InstanciaObjeto.objects.filter(objeto_id=obj.id,aventura_id=self.aventura_id);  # | concatena apenas QuerySet
        
        self.fields['nome'].label = 'Name'
        self.fields['operador'].label = 'Logical Operator'
        self.fields['ligacao'].label = 'Link'
        
        # carregando instâncias
        self.fields['sufixo'] = InstanciaObjetoRoleModelChoiceField(queryset=buffer_inst,)
        self.fields['sufixo'].required = True
        self.fields['sufixo'].label = 'Instances'
        
        # recupernado e carregando avatares da aventura
        self.fields['prefixo'] = CondicaoJogadorModelChoiceField(queryset=Avatar.objects.filter(aventura_avatar_id=self.aventura_id))
        self.fields['prefixo'].required = True
        self.fields['prefixo'].label = 'Avatar'
        
                # Carregando missoes da aventura
        self.fields['missao'] = MissaoModelChoiceField(Missao.objects.filter(aventuras_id=self.aventura_id),)
        self.fields['missao'].required = True
        self.fields['missao'].label = 'Mission'

        # Carregando enredos da aventura
        self.fields['enredo'] = EnredoModelChoiceField(Enredo.objects.filter(aventura_id=self.aventura_id),)
        self.fields['enredo'].required = True
        self.fields['enredo'].label = 'Story'
        
    class Meta: 
        model = CondicaoJogadorInstancia

class CondicaoDialogoModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_nome_avatar()

# Condições de avatares com diálogos de personagens        
class CondicaoDialogoInstanciaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CondicaoDialogoInstanciaForm, self).__init__(*args, **kwargs)
        
        
        # recupera id da aventura
        self.aventura_id = kwargs['initial']['aventura_id']
        object_list = Objeto.objects.filter(coletavel=False, dialogo=True,)
        
        
        self.fields['nome'].label = 'Name'
        self.fields['operador'].label = 'Logical Operator'
        self.fields['ligacao'].label = 'Link'
        
        # recuperar instâncias que possuem diálogo como ativado.
        flag = 0;
        buffer_inst = '';
        for obj in object_list:
            if flag == 0:
                buffer_inst = InstanciaObjeto.objects.filter(objeto_id=obj.id, aventura_id=self.aventura_id,)
                flag = 1;
            elif flag == 1:
                buffer_inst = buffer_inst | InstanciaObjeto.objects.filter(objeto_id=obj.id, aventura_id=self.aventura_id,)  # | concatena apenas QuerySet
        
        self.fields['referencia_sufixo'] = InstanciaObjetoRoleModelChoiceField(queryset=buffer_inst,)
        self.fields['referencia_sufixo'].required = True
        self.fields['referencia_sufixo'].label = 'Instance Reference'
        
        
        self.fields['prefixo'] = CondicaoDialogoModelChoiceField(queryset=Avatar.objects.filter(aventura_avatar_id=self.aventura_id))
        self.fields['prefixo'].required = True
        self.fields['prefixo'].label = 'Avatar'
        
                        # Carregando missoes da aventura
        self.fields['missao'] = MissaoModelChoiceField(Missao.objects.filter(aventuras_id=self.aventura_id),)
        self.fields['missao'].required = True
        self.fields['missao'].label = 'Mission'

        # Carregando enredos da aventura
        self.fields['enredo'] = EnredoModelChoiceField(Enredo.objects.filter(aventura_id=self.aventura_id),)
        self.fields['enredo'].required = True
        self.fields['enredo'].label = 'Story'
        
    class Meta: 
        model = CondicaoDialogoInstancia

        
'''
Form para criação de roles/papeis para avatares
'''
# retorna o nome da instancia       
class InstanciaObjetoRoleModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_nome_instancia()

# Formada o template para criação de papéis
class AvatarRoleListForm(forms.ModelForm):  
    def __init__(self, *args, **kwargs):
        super(AvatarRoleListForm, self).__init__(*args, **kwargs)
        # get_nome_tipo_imagem
        self.fields['inst_objeto'].label = 'Object Instance'
        self.fields['inst_objeto'] = InstanciaObjetoRoleModelChoiceField(queryset=InstanciaObjeto.objects.filter(encenacao='AV'),)
        self.fields['inst_objeto'].required = False
        
    class Meta: 
        model = Avatar
        exclude = ['publico', 'longitude', 'latitude', 'aventureiro', 'aventura_avatar', 'avatar']  
    
'''
Form para tratar  a criação de avatar
'''
class CreateAvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        exclude = ['longitude', 'latitude', 'aventureiro', 'aventura_avatar', 'inst_objeto', ]
        
        
'''
Form para CreateMissao
'''
class CreateMissaoForm(forms.ModelForm):
    class Meta:
        model = Missao
        exclude = ['aventuras', ]

'''
Form para Update Objeto - Customizando selec icone
'''
class IconeModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_nome_icone()
     
class UpdateObjetoForm(forms.ModelForm):
    class Meta:
        model = Objeto
        
    def __init__(self, *args, **kwargs):
        super(UpdateObjetoForm, self).__init__(*args, **kwargs)
        self.fields['icone_objeto'] = IconeModelChoiceField(queryset=Icone.objects.filter(),)
        # forms.ModelChoiceField(queryset=TipoImagem.objects.filter(tipo='IM'))
       

'''
Form para Agente
'''            
class AgenteCreateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(AgenteCreateForm, self).__init__(*args, **kwargs)
        
        id_aven = kwargs['initial']['aventura_id']
      

        # get_nome_tipo_imagem
        
        self.fields['instancia'] = InstanciaObjetoRoleModelChoiceField(queryset=InstanciaObjeto.objects.filter(encenacao='AG',aventura_id =id_aven ))
        self.fields['instancia'].required = True
        self.fields['instancia'].label = 'Instance'
        self.fields['nome'].label = 'Name'
        self.fields['proximidade'].label = 'Proximity' 
        self.fields['comportamento'].label = 'Behavior'
        
        
    class Meta:
        model = Agente
        exclude = ['aventura_agente', ]        

        

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
        exclude = ['latitude', 'longitude', 'autor', ]
        fim = forms.DateField(widget=SelectDateWidget(years=range(date.today().year, 2099)),)
        # autor = forms.IntegerField(widget=forms.IntegerField())
        # def __init__(self, *args, **kwargs):
        #    super(AventuraForm, self).__init__(*args, **kwargs)
        #    self.fields['fim'].widget = forms.DateField(widget=SelectDateWidget(years=range(date.today().year, 2099)),)
        
'''
Form utilizado para salvar aventura na session
'''
class AventuraWithoutFieldsForm(forms.ModelForm):
    class Meta:
        model = Aventura
        exclude = ['nome', 'descricao', 'inicio', 'fim', 'longitude', 'autor', 'latitude', ]
        
'''
Form utilizado para salvar aventura na session
'''
class AgenteWithoutFieldsForm(forms.ModelForm):
    class Meta:
        model = Agente
        exclude = ['nome', 'proximidade', 'aventura_agente', 'comportamento', 'instancia_id', 'instancia']

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
    
    # criptografia senha autor
    def save(self, commit=True):
        user = super(AutorForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            return user
    class Meta: 
        model = Autor
        # remove parametros desnecessarios
        exclude = ['is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions', 'id_password1', 'id_password2', ]
        
'''
Form utilizado para criar instancia do objeto
'''
class InstanciaObjetoCreateForm(forms.ModelForm):
    class Meta:
        model = InstanciaObjeto
        exclude = ['nome', 'proximidade', 'encenacao', 'objeto', 'visivel', 'sugestao', 'num_instancia', 'aventura', 'instancia_cont', ]

'''
Form utilizado para criar POS
'''
class  PosicaoGeograficaCreateForm(forms.ModelForm):
    class Meta:
        model = PosicaoGeografica
        exclude = ['latitude', 'longitude', 'altitude', 'instancia_objeto', ] 
        
        
'''
Form para Update Instancia de Objeto
'''
class InstanciaObjetoModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_nome_tipo_imagem()

class InstanciaObjetoUpdateForm(forms.ModelForm):  
    class Meta: 
        model = InstanciaObjeto
        # model.dialogo = forms.CharField(label=_("Diálogo"), widget=forms.Textarea(attrs={'cols': 40, 'rows': 5,'style':"width: 500px; height: 100px;"}))
        exclude = ['objeto', 'aventura', 'instancia_cont', ]  

    nome = forms.CharField(label=_("Nome"), max_length=30, widget=forms.TextInput(attrs={'style' : 'width: 90px'}))
    proximidade = forms.IntegerField(label=_("Proximidade"), widget=forms.TextInput(attrs={'style' : 'width: 20px'}))
    dialogo = forms.CharField(label=_("Diálogo"), widget=forms.Textarea(attrs={'cols': 40, 'rows': 5, 'style':"width: 500px; height: 100px;"}))
    
    # torna o campo field oculto
    def __init__(self, *args, **kwargs):
        super(InstanciaObjetoUpdateForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        
        # get_nome_tipo_imagem
        self.fields['imagem_mapa'] = InstanciaObjetoModelChoiceField(queryset=TipoImagem.objects.filter(tipo='IM'),)
        self.fields['imagem_camera'] = InstanciaObjetoModelChoiceField(queryset=TipoImagem.objects.filter(tipo='IC'),)
        self.fields['imagem_mapa'].required = False
        self.fields['imagem_camera'].required = False
        self.fields['sugestao_objeto'].required = False
        object_list = Objeto.objects.all().filter(pk=instance.objeto.id)
        dialog_tam = int(len(instance.dialogo))
        for obj in object_list:
            if obj.dialogo == False:
                # self.fields['dialogo'].widget = forms.HiddenInput()
                self.fields.pop('dialogo')
            else:
                if dialog_tam < 60:  # xml editado tem tamanho superior a 80
                    dialogo = "<dialogo id_instancia='" + str(instance.id) + "' nome='" + instance.nome + "'>\n"
                    # dialogo +="<npc tipo='dialogoInicial'>\n Digite a fala inicial do personagem aqui.\n </npc>"
                    # dialogo +="<avatar tipo='confirmacao'>\nDigite a fala do jogador aqui.\n"
                    # dialogo +='<npc tipo="dialogoFinal">\nApós uma fala do jogador, o dialogo entre o mesmo e o npc pode acabar. Assim, tem-se dialogoFinal\n</npc>'
                    # '\n</avatar>'
                    # dialogo +="\n<avatar tipo='negacao'>\nDigite a fala do jogador aqui.\n</avatar>"       
                    dialogo += "\n</dialogo>" 
                    self.initial = {'nome':instance.nome, 'dialogo': dialogo, 'proximidade': instance.proximidade,
                                   'encenacao':instance.encenacao, 'sugestao':instance.sugestao_objeto, 'visivel':instance.visivel}
                    
'''
Forms para criação para Comportamentos
'''

class PosGeoRoleModelChoiceField(ModelChoiceField):
    
    def __init__(self, *args, **kwargs):
        self.pos = 0     
        super(PosGeoRoleModelChoiceField, self).__init__(*args, **kwargs)
    
    def label_from_instance(self, obj):
        self.pos += 1
        return "POS #%i" % self.pos

     
class AgressivoCreateForm(forms.ModelForm):
        
        def __init__(self, *args, **kwargs):
            super(AgressivoCreateForm, self).__init__(*args, **kwargs)
            
            # recupera id da instância do agente
            instancia_id = kwargs['initial']['instancia_id']
            # recupera id da aventura
            id_aventura = kwargs['initial']['aventura_id']
            
            # configura select com as posições da instância.
            queryset = PosicaoGeografica.objects.filter(instancia_objeto_id=instancia_id)
            aux = 0
            for obj in queryset:
                print obj.get_nome_instancia(aux)
                aux = aux + 1
            
            self.fields['pos_inicial'] = PosGeoRoleModelChoiceField(queryset=PosicaoGeografica.objects.filter(instancia_objeto_id=instancia_id),)
            self.fields['pos_inicial'].required = True
            self.fields['pos_inicial'].label = 'Initial Position'
            # recuperando instancias que sejam coletaveis
            
            
            objetos = Objeto.objects.filter(coletavel=1)
            print objetos
            
            flag = 0
            for obj in objetos:
                if flag == 0:
                    instancias = InstanciaObjeto.objects.filter(objeto_id=obj.id, aventura_id=id_aventura,)
                    flag = 1;
                elif flag == 1:
                    instancias = instancias | InstanciaObjeto.objects.filter(objeto_id=obj.id, aventura_id=id_aventura,)  # | concatena apenas QuerySet

            
            self.fields['item'] = InstanciaObjetoRoleModelChoiceField(queryset=instancias,)
            self.fields['item'].required = True
            self.fields['item'].label = 'Item'
            
            # carregando avatares 
            
            self.fields['avatar_vit'] = CondicaoJogadorModelChoiceField(queryset=Avatar.objects.filter(aventura_avatar_id=id_aventura))
            self.fields['avatar_vit'].required = True
            self.fields['avatar_vit'].label = 'Avatar'
            
        class Meta:
            model = Agressivo
            exclude = ['agente', ] 
            
class PassivoCreateForm(forms.ModelForm):
        
        def __init__(self, *args, **kwargs):
            super(PassivoCreateForm, self).__init__(*args, **kwargs)
            
            # recupera id da instância do agente
            instancia_id = kwargs['initial']['instancia_id']
            # recupera id da aventura
            # id_aventura = kwargs['initial']['aventura_id']
            
            # configura select com as posições da instância.
           
            
            queryset = PosicaoGeografica.objects.filter(instancia_objeto_id=instancia_id)
            aux = 0
            for obj in queryset:
                print obj.get_nome_instancia(aux)
                aux = aux + 1
            
            self.fields['pos_inicial'] = PosGeoRoleModelChoiceField(queryset=PosicaoGeografica.objects.filter(instancia_objeto_id=instancia_id),)
            self.fields['pos_inicial'].required = True
            self.fields['pos_inicial'].label = "Initial Position"

        class Meta:
            model = Passivo
            exclude = ['agente', ] 
            
class ColaborativoCreateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ColaborativoCreateForm, self).__init__(*args, **kwargs)
        
        # recupera id da instância do agente
        instancia_id = kwargs['initial']['instancia_id']
        # recupera id da aventura
        id_aventura = kwargs['initial']['aventura_id']
        
        queryset = PosicaoGeografica.objects.filter(instancia_objeto_id=instancia_id)
        aux = 0
        for obj in queryset:
            print obj.get_nome_instancia(aux)
            aux = aux + 1
            
        self.fields['pos_inicial'] = PosGeoRoleModelChoiceField(queryset=PosicaoGeografica.objects.filter(instancia_objeto_id=instancia_id),)
        self.fields['pos_inicial'].required = True
        self.fields['pos_inicial'].label = "Initial Position"
        
        self.fields['avatar_col'] = CondicaoJogadorModelChoiceField(queryset=Avatar.objects.filter(aventura_avatar_id=id_aventura))
        self.fields['avatar_col'].required = True
        self.fields['avatar_col'].label = 'Avatar'
        
    class Meta:
        model = Colaborativo
        exclude = ['obstaculoscl', 'agente', ] 
        
        
class CompetitivoCreateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CompetitivoCreateForm, self).__init__(*args, **kwargs)
        
        # recupera id da instância do agente
        instancia_id = kwargs['initial']['instancia_id']
        # recupera id da aventura
        id_aventura = kwargs['initial']['aventura_id']
        
        queryset = PosicaoGeografica.objects.filter(instancia_objeto_id=instancia_id)
        aux = 0
        for obj in queryset:
            print obj.get_nome_instancia(aux)
            aux = aux + 1
            
        self.fields['pos_inicial'] = PosGeoRoleModelChoiceField(queryset=PosicaoGeografica.objects.filter(instancia_objeto_id=instancia_id),)
        self.fields['pos_inicial'].required = True
        self.fields['pos_inicial'].label = "Initial Position"
        
        self.fields['avatar_comp'] = CondicaoJogadorModelChoiceField(queryset=Avatar.objects.filter(aventura_avatar_id=id_aventura))
        self.fields['avatar_comp'].required = True
        self.fields['avatar_comp'].label = 'Avatar'
        
    class Meta:
        model = Competitivo
        exclude = ['obstaculoscp', 'agente', ]         
        
        
class InstancesComportamentoAddForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(InstancesComportamentoAddForm, self).__init__(*args, **kwargs)
        
        # recupera id da instância do agente
        # instancia_id = kwargs['initial']['instancia_id']
        # recupera id da aventura
        id_aventura = kwargs['initial']['aventura_id']
        
        
        # encenacao="DS"   irá recuperar todos os tipos de instâncias
        self.fields['instancia_objeto'] = InstanciaObjetoRoleModelChoiceField(queryset=InstanciaObjeto.objects.filter(aventura_id=id_aventura,),)
        self.fields['instancia_objeto'].required = True
        self.fields['instancia_objeto'].label = 'Instances'
        
    class Meta:
        model = Mensagem
        exclude = ['colaborativo', 'competitivo', ] 
        
        
'''
Form para ocultar select aventura
'''
class  EnredoFileForm(forms.ModelForm):
    class Meta:
        model = EnredoFile
        exclude = ['aventura', ] 
        
class  EnredoInstanciaForm(forms.ModelForm):

      
        def __init__(self, *args, **kwargs):
            super(EnredoInstanciaForm, self).__init__(*args, **kwargs)
            
            # recupera id da instância do agente
            # instancia_id = kwargs['initial']['instancia_id']
            # recupera id da aventura
            id_aventura = kwargs['initial']['aventura_id']
            
            object_list = Objeto.objects.filter(coletavel=True)

            # Recuperando Instâncias
            flag = 0;
            buffer_inst = '';
            for obj in object_list:
                if flag == 0:
                    print id_aventura
                    buffer_inst = InstanciaObjeto.objects.filter(objeto_id=obj.id, aventura_id=id_aventura)
                    flag = 1;
                elif flag == 1:
                    buffer_inst = buffer_inst | InstanciaObjeto.objects.filter(objeto_id=obj.id, aventura_id=id_aventura);  # | concatena apenas QuerySet
            
            # Carregando Instâncias
            self.fields['enredo_instancia'] = InstanciaObjetoRoleModelChoiceField(queryset=buffer_inst,)
            self.fields['enredo_instancia'].required = True
            self.fields['enredo_instancia'].label = 'Instances'
            
            self.fields['nome'].label = 'Name'
            self.fields['descricao'].label = 'Description'
            # encenacao="DS"   irá recuperar todos os tipos de instâncias
            #self.fields['instancia_objeto'] = queryset=InstanciaObjeto.objects.filter(aventura_id=id_aventura,),)
            #self.fields['instancia_objeto'].required = True
            #self.fields['instancia_objeto'].label = 'Instances'
            
        class Meta:
            model = EnredoInstancia
            exclude = ['aventura', ]
'''
Form para ocultar select aventura
'''
class  EnredoMensagemForm(forms.ModelForm):
    class Meta:
        model = EnredoMensagem
        exclude = ['aventura', ] 
        
        
'''
Form para ajustar template para criação de condições com avatar e objeto
'''
class ObjetoRoleModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_nome_objeto()
    
class CondicaoJogadorObjetoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CondicaoJogadorObjetoForm, self).__init__(*args, **kwargs)

        # recupera id da aventura para recuperar instâncias da aventura
        self.aventura_id = kwargs['initial']['aventura_id']
        object_list = Objeto.objects.filter(coletavel=True)
             
        # recueprando instâncias
        flag = 0
        buffer_inst = ''
        for obj in object_list:
            if flag == 0:
                buffer_inst = InstanciaObjeto.objects.filter(objeto_id=obj.id, aventura_id=self.aventura_id)
                flag = 1;
            elif flag == 1:
                buffer_inst = buffer_inst | InstanciaObjeto.objects.filter(objeto_id=obj.id,aventura_id=self.aventura_id)  # | concatena apenas QuerySet
        
        
        #recuperando objetos coletaveis que possuem instâncias
        buffer_objetos = ''
        flag = 0
        for obj in buffer_inst:
            if flag == 0:
                buffer_objetos = Objeto.objects.filter(coletavel=True, pk = obj.objeto_id, )
                flag = 1
            elif flag == 1:
                buffer_objetos = buffer_objetos | Objeto.objects.filter(coletavel=True, pk = obj.objeto_id, )
    
        
        self.fields['nome'].label = 'Name'
        self.fields['operador'].label = 'Logical Operator'
        self.fields['ligacao'].label = 'Link'
        
        # carregando instâncias
        self.fields['sufixo'] = ObjetoRoleModelChoiceField(queryset=buffer_objetos,)
        self.fields['sufixo'].required = True
        self.fields['sufixo'].label = 'Instances'
        
        # recupernado e carregando avatares da aventura
        self.fields['prefixo'] = CondicaoJogadorModelChoiceField(queryset=Avatar.objects.filter(aventura_avatar_id=self.aventura_id))
        self.fields['prefixo'].required = True
        self.fields['prefixo'].label = 'Avatar'
        
                # Carregando missoes da aventura
        self.fields['missao'] = MissaoModelChoiceField(Missao.objects.filter(aventuras_id=self.aventura_id),)
        self.fields['missao'].required = True
        self.fields['missao'].label = 'Mission'

        # Carregando enredos da aventura
        self.fields['enredo'] = EnredoModelChoiceField(Enredo.objects.filter(aventura_id=self.aventura_id),)
        self.fields['enredo'].required = True
        self.fields['enredo'].label = 'Story'
        
    class Meta: 
        model = CondicaoJogadorObjeto


'''
Form utilizado para AventuraAtiva
'''
class AventuraAtivaWithoutFieldsForm(forms.ModelForm):
    class Meta:
        model = AventuraAtiva
        exclude = ['aventura','joadores_aventura_ativa', 'instancia', 'chave_acesso', ]    
        
        
'''
########################################################
Form utilizado para Create dos Estado da Aventura
########################################################
'''
class PosInstanciaAtivaCreateForm(forms.ModelForm):
    class Meta:
        model = PosInstanciaAtiva
        exclude = ['latitude', 'longitude', 'altitude', 'instancia_objeto_ativa', 'aventura_ativa_instancia', ]
   
class AvatarAtivoCreateForm(forms.ModelForm):
    class Meta:
        model = AvatarAtivo
        exclude = ['latitude', 'longitude', 'avatar', 'aventura_ativa_avatar', ]

class MissaoAtivaCreateForm(forms.ModelForm):
    class Meta:
        model = MissaoAtiva
        exclude = ['missao', 'aventura_ativa_missao', 'estado_missao', ]

class CondicaoAtivaCreateForm(forms.ModelForm):
    class Meta:
        model = CondicaoAtiva
        exclude = ['missao_ativa', 'aventura_ativa_condicao', 'estado_condicao','condicao', ]