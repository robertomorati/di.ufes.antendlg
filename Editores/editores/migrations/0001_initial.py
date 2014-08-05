# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TipoObjeto'
        db.create_table(u'editores_tipoobjeto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('posicoes_geograficas', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3)),
            ('publico', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'editores', ['TipoObjeto'])

        # Adding model 'Icone'
        db.create_table(u'editores_icone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('icone', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'editores', ['Icone'])

        # Adding model 'Sugestao'
        db.create_table(u'editores_sugestao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('tipo', self.gf('django.db.models.fields.CharField')(default=u'STX', max_length=10)),
            ('sugestao', self.gf('django.db.models.fields.files.FileField')(default='', max_length=100)),
            ('proximidade', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3)),
            ('publico', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'editores', ['Sugestao'])

        # Adding model 'Objeto'
        db.create_table(u'editores_objeto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('quantidade', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=100)),
            ('coletavel', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tipo_objeto', self.gf('django.db.models.fields.related.ForeignKey')(related_name='objetos', to=orm['editores.TipoObjeto'])),
            ('icone_objeto', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='icones', to=orm['editores.Icone'])),
            ('dialogo', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'editores', ['Objeto'])

        # Adding model 'Autor'
        db.create_table(u'editores_autor', (
            (u'user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('dica_senha', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('icone_autor', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True)),
        ))
        db.send_create_signal(u'editores', ['Autor'])

        # Adding model 'Aventura'
        db.create_table(u'editores_aventura', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('inicio', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('fim', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(default=0.0, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(default=0.0, blank=True)),
            ('autor', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='Autor', blank=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'editores', ['Aventura'])

        # Adding model 'TipoImagem'
        db.create_table(u'editores_tipoimagem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome_img', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('tipo', self.gf('django.db.models.fields.CharField')(default='IM', max_length=10)),
            ('img_play', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('descricao', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
        ))
        db.send_create_signal(u'editores', ['TipoImagem'])

        # Adding model 'InstanciaObjeto'
        db.create_table(u'editores_instanciaobjeto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('proximidade', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3)),
            ('visivel', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('encenacao', self.gf('django.db.models.fields.CharField')(default='DS', max_length=14, blank=True)),
            ('objeto', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='instancias_objeto', blank=True, to=orm['editores.Objeto'])),
            ('sugestao_objeto', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='sugestoes', null=True, blank=True, to=orm['editores.Sugestao'])),
            ('aventura', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='aventura_inst_obj', null=True, blank=True, to=orm['editores.Aventura'])),
            ('dialogo', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('imagem_mapa', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='tipo_imagem_mapa', null=True, blank=True, to=orm['editores.TipoImagem'])),
            ('imagem_camera', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='tipo_imagem_camera', null=True, blank=True, to=orm['editores.TipoImagem'])),
        ))
        db.send_create_signal(u'editores', ['InstanciaObjeto'])

        # Adding model 'PosicaoGeografica'
        db.create_table(u'editores_posicaogeografica', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('altitude', self.gf('django.db.models.fields.FloatField')()),
            ('instancia_objeto', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='pos_inst_objeto', blank=True, to=orm['editores.InstanciaObjeto'])),
        ))
        db.send_create_signal(u'editores', ['PosicaoGeografica'])

        # Adding model 'Jogador'
        db.create_table(u'editores_jogador', (
            (u'user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('dica_senha', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
        ))
        db.send_create_signal(u'editores', ['Jogador'])

        # Adding model 'AventuraAtiva'
        db.create_table(u'editores_aventuraativa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instancia', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=2)),
            ('aventura', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='aventura', null=True, blank=True, to=orm['editores.Aventura'])),
            ('publica', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('chave_acesso', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True)),
        ))
        db.send_create_signal(u'editores', ['AventuraAtiva'])

        # Adding M2M table for field joadores_aventura_ativa on 'AventuraAtiva'
        m2m_table_name = db.shorten_name(u'editores_aventuraativa_joadores_aventura_ativa')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aventuraativa', models.ForeignKey(orm[u'editores.aventuraativa'], null=False)),
            ('jogador', models.ForeignKey(orm[u'editores.jogador'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aventuraativa_id', 'jogador_id'])

        # Adding model 'PosInstanciaAtiva'
        db.create_table(u'editores_posinstanciaativa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('altitude', self.gf('django.db.models.fields.FloatField')()),
            ('instancia_objeto_ativa', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='instancia_objeto_ativa', blank=True, to=orm['editores.InstanciaObjeto'])),
            ('aventura_ativa_instancia', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='aventura_ativa_instancia', blank=True, to=orm['editores.AventuraAtiva'])),
        ))
        db.send_create_signal(u'editores', ['PosInstanciaAtiva'])

        # Adding model 'Avatar'
        db.create_table(u'editores_avatar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('publico', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('aventureiro', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='aventureiro', null=True, blank=True, to=orm['editores.Jogador'])),
            ('aventura_avatar', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='aventura_avatar', null=True, blank=True, to=orm['editores.Aventura'])),
            ('inst_objeto', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='inst_objeto', null=True, blank=True, to=orm['editores.InstanciaObjeto'])),
        ))
        db.send_create_signal(u'editores', ['Avatar'])

        # Adding model 'AvatarAtivo'
        db.create_table(u'editores_avatarativo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('aventura_ativa_avatar', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='aventura_ativa_avatar', null=True, blank=True, to=orm['editores.AventuraAtiva'])),
            ('latitude', self.gf('django.db.models.fields.FloatField')(default='0')),
            ('longitude', self.gf('django.db.models.fields.FloatField')(default='0')),
            ('avatar', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='avatar_ativo', null=True, blank=True, to=orm['editores.Avatar'])),
        ))
        db.send_create_signal(u'editores', ['AvatarAtivo'])

        # Adding model 'Enredo'
        db.create_table(u'editores_enredo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('descricao', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('aventura', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='aventura_enredo', null=True, blank=True, to=orm['editores.Aventura'])),
        ))
        db.send_create_signal(u'editores', ['Enredo'])

        # Adding model 'EnredoFile'
        db.create_table(u'editores_enredofile', (
            (u'enredo_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['editores.Enredo'], unique=True, primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(default='SAU', max_length=10)),
            ('enredo_file', self.gf('django.db.models.fields.files.FileField')(default='', max_length=100)),
        ))
        db.send_create_signal(u'editores', ['EnredoFile'])

        # Adding model 'EnredoInstancia'
        db.create_table(u'editores_enredoinstancia', (
            (u'enredo_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['editores.Enredo'], unique=True, primary_key=True)),
            ('enredo_instancia', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='enredo_instancia', blank=True, to=orm['editores.InstanciaObjeto'])),
        ))
        db.send_create_signal(u'editores', ['EnredoInstancia'])

        # Adding model 'EnredoMensagem'
        db.create_table(u'editores_enredomensagem', (
            (u'enredo_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['editores.Enredo'], unique=True, primary_key=True)),
            ('enredo_mensagem', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
        ))
        db.send_create_signal(u'editores', ['EnredoMensagem'])

        # Adding model 'Missao'
        db.create_table(u'editores_missao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('descricao', self.gf('django.db.models.fields.CharField')(default='descreva o objetivo da miss\xc3\xa3o', max_length=200)),
            ('tempo', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('enredo', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='enredo_missao', null=True, blank=True, to=orm['editores.Enredo'])),
            ('aventuras', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='aventuras', null=True, blank=True, to=orm['editores.Aventura'])),
        ))
        db.send_create_signal(u'editores', ['Missao'])

        # Adding model 'MissaoAtiva'
        db.create_table(u'editores_missaoativa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('missao', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='missao', null=True, blank=True, to=orm['editores.Missao'])),
            ('aventura_ativa_missao', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='aventura_ativa_missao', null=True, blank=True, to=orm['editores.AventuraAtiva'])),
            ('estado_missao', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'editores', ['MissaoAtiva'])

        # Adding model 'Condicao'
        db.create_table(u'editores_condicao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('operador', self.gf('django.db.models.fields.CharField')(default='AND', max_length=10)),
            ('ligacao', self.gf('django.db.models.fields.CharField')(default='GET_OBJ', max_length=20)),
            ('enredo', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='enredos', null=True, blank=True, to=orm['editores.Enredo'])),
            ('missao', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='condicoes_missao', null=True, blank=True, to=orm['editores.Missao'])),
        ))
        db.send_create_signal(u'editores', ['Condicao'])

        # Adding model 'CondicaoAtiva'
        db.create_table(u'editores_condicaoativa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('condicao', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='condicao', null=True, blank=True, to=orm['editores.Condicao'])),
            ('missao_ativa', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='missao_ativa', null=True, blank=True, to=orm['editores.MissaoAtiva'])),
            ('aventura_ativa_condicao', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='aventura_ativa_condicao', null=True, blank=True, to=orm['editores.AventuraAtiva'])),
            ('estado_condicao', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'editores', ['CondicaoAtiva'])

        # Adding model 'CondicaoInstanciaObjeto'
        db.create_table(u'editores_condicaoinstanciaobjeto', (
            (u'condicao_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['editores.Condicao'], unique=True, primary_key=True)),
            ('prefixo', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='prefixo_co_inst_obj', null=True, blank=True, to=orm['editores.InstanciaObjeto'])),
            ('sufixo', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='sufixo_co_inst_obj', null=True, blank=True, to=orm['editores.InstanciaObjeto'])),
        ))
        db.send_create_signal(u'editores', ['CondicaoInstanciaObjeto'])

        # Adding model 'CondicaoJogadorInstancia'
        db.create_table(u'editores_condicaojogadorinstancia', (
            (u'condicao_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['editores.Condicao'], unique=True, primary_key=True)),
            ('prefixo', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='prefixo_cji_avateres', null=True, blank=True, to=orm['editores.Avatar'])),
            ('sufixo', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='sufixo_cji_inst_obj', null=True, blank=True, to=orm['editores.InstanciaObjeto'])),
        ))
        db.send_create_signal(u'editores', ['CondicaoJogadorInstancia'])

        # Adding model 'CondicaoJogadorObjeto'
        db.create_table(u'editores_condicaojogadorobjeto', (
            (u'condicao_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['editores.Condicao'], unique=True, primary_key=True)),
            ('prefixo', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='prefixo_cjo_avateres', null=True, blank=True, to=orm['editores.Avatar'])),
            ('sufixo', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='sufixo_cjo__obj', null=True, blank=True, to=orm['editores.Objeto'])),
            ('quantidade', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3)),
        ))
        db.send_create_signal(u'editores', ['CondicaoJogadorObjeto'])

        # Adding model 'CondicaoDialogoInstancia'
        db.create_table(u'editores_condicaodialogoinstancia', (
            (u'condicao_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['editores.Condicao'], unique=True, primary_key=True)),
            ('prefixo', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='prefixo_cd_avateres', null=True, blank=True, to=orm['editores.Avatar'])),
            ('sufixo', self.gf('django.db.models.fields.CharField')(default='DIALOGO_INICIAL', max_length=20)),
            ('referencia_sufixo', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='ref_sufixo_cd_inst_obj', null=True, blank=True, to=orm['editores.InstanciaObjeto'])),
        ))
        db.send_create_signal(u'editores', ['CondicaoDialogoInstancia'])

        # Adding model 'Agente'
        db.create_table(u'editores_agente', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('instancia', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='instancia', null=True, blank=True, to=orm['editores.InstanciaObjeto'])),
            ('proximidade', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3)),
            ('comportamento', self.gf('django.db.models.fields.CharField')(default='Agressivo', max_length=15)),
            ('aventura_agente', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='aventura_agente', null=True, blank=True, to=orm['editores.Aventura'])),
        ))
        db.send_create_signal(u'editores', ['Agente'])

        # Adding model 'Comportamento'
        db.create_table(u'editores_comportamento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos_inicial', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='pos_inicial', null=True, blank=True, to=orm['editores.PosicaoGeografica'])),
            ('agente', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='agente', null=True, blank=True, to=orm['editores.Agente'])),
        ))
        db.send_create_signal(u'editores', ['Comportamento'])

        # Adding model 'Agressivo'
        db.create_table(u'editores_agressivo', (
            (u'comportamento_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['editores.Comportamento'], unique=True, primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='instancia_agressivo', null=True, blank=True, to=orm['editores.InstanciaObjeto'])),
            ('avatar_vit', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='avatar_vit', null=True, blank=True, to=orm['editores.Avatar'])),
        ))
        db.send_create_signal(u'editores', ['Agressivo'])

        # Adding model 'Passivo'
        db.create_table(u'editores_passivo', (
            (u'comportamento_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['editores.Comportamento'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'editores', ['Passivo'])

        # Adding model 'Colaborativo'
        db.create_table(u'editores_colaborativo', (
            (u'comportamento_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['editores.Comportamento'], unique=True, primary_key=True)),
            ('avatar_col', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='avatar_col', null=True, blank=True, to=orm['editores.Avatar'])),
        ))
        db.send_create_signal(u'editores', ['Colaborativo'])

        # Adding model 'Competitivo'
        db.create_table(u'editores_competitivo', (
            (u'comportamento_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['editores.Comportamento'], unique=True, primary_key=True)),
            ('avatar_comp', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='avatar_comp', null=True, blank=True, to=orm['editores.Avatar'])),
        ))
        db.send_create_signal(u'editores', ['Competitivo'])

        # Adding model 'Mensagem'
        db.create_table(u'editores_mensagem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mensagem', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('instancia_objeto', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='instancia_objeto', null=True, blank=True, to=orm['editores.InstanciaObjeto'])),
            ('colaborativo', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='colaborativo', null=True, blank=True, to=orm['editores.Colaborativo'])),
            ('competitivo', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='competitivo', null=True, blank=True, to=orm['editores.Competitivo'])),
        ))
        db.send_create_signal(u'editores', ['Mensagem'])

        # Adding model 'Mochila'
        db.create_table(u'editores_mochila', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('avatar_mochila', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='avatar_mochila', null=True, blank=True, to=orm['editores.AvatarAtivo'])),
        ))
        db.send_create_signal(u'editores', ['Mochila'])

        # Adding M2M table for field instancia_mochila on 'Mochila'
        m2m_table_name = db.shorten_name(u'editores_mochila_instancia_mochila')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mochila', models.ForeignKey(orm[u'editores.mochila'], null=False)),
            ('instanciaobjeto', models.ForeignKey(orm[u'editores.instanciaobjeto'], null=False))
        ))
        db.create_unique(m2m_table_name, ['mochila_id', 'instanciaobjeto_id'])


    def backwards(self, orm):
        # Deleting model 'TipoObjeto'
        db.delete_table(u'editores_tipoobjeto')

        # Deleting model 'Icone'
        db.delete_table(u'editores_icone')

        # Deleting model 'Sugestao'
        db.delete_table(u'editores_sugestao')

        # Deleting model 'Objeto'
        db.delete_table(u'editores_objeto')

        # Deleting model 'Autor'
        db.delete_table(u'editores_autor')

        # Deleting model 'Aventura'
        db.delete_table(u'editores_aventura')

        # Deleting model 'TipoImagem'
        db.delete_table(u'editores_tipoimagem')

        # Deleting model 'InstanciaObjeto'
        db.delete_table(u'editores_instanciaobjeto')

        # Deleting model 'PosicaoGeografica'
        db.delete_table(u'editores_posicaogeografica')

        # Deleting model 'Jogador'
        db.delete_table(u'editores_jogador')

        # Deleting model 'AventuraAtiva'
        db.delete_table(u'editores_aventuraativa')

        # Removing M2M table for field joadores_aventura_ativa on 'AventuraAtiva'
        db.delete_table(db.shorten_name(u'editores_aventuraativa_joadores_aventura_ativa'))

        # Deleting model 'PosInstanciaAtiva'
        db.delete_table(u'editores_posinstanciaativa')

        # Deleting model 'Avatar'
        db.delete_table(u'editores_avatar')

        # Deleting model 'AvatarAtivo'
        db.delete_table(u'editores_avatarativo')

        # Deleting model 'Enredo'
        db.delete_table(u'editores_enredo')

        # Deleting model 'EnredoFile'
        db.delete_table(u'editores_enredofile')

        # Deleting model 'EnredoInstancia'
        db.delete_table(u'editores_enredoinstancia')

        # Deleting model 'EnredoMensagem'
        db.delete_table(u'editores_enredomensagem')

        # Deleting model 'Missao'
        db.delete_table(u'editores_missao')

        # Deleting model 'MissaoAtiva'
        db.delete_table(u'editores_missaoativa')

        # Deleting model 'Condicao'
        db.delete_table(u'editores_condicao')

        # Deleting model 'CondicaoAtiva'
        db.delete_table(u'editores_condicaoativa')

        # Deleting model 'CondicaoInstanciaObjeto'
        db.delete_table(u'editores_condicaoinstanciaobjeto')

        # Deleting model 'CondicaoJogadorInstancia'
        db.delete_table(u'editores_condicaojogadorinstancia')

        # Deleting model 'CondicaoJogadorObjeto'
        db.delete_table(u'editores_condicaojogadorobjeto')

        # Deleting model 'CondicaoDialogoInstancia'
        db.delete_table(u'editores_condicaodialogoinstancia')

        # Deleting model 'Agente'
        db.delete_table(u'editores_agente')

        # Deleting model 'Comportamento'
        db.delete_table(u'editores_comportamento')

        # Deleting model 'Agressivo'
        db.delete_table(u'editores_agressivo')

        # Deleting model 'Passivo'
        db.delete_table(u'editores_passivo')

        # Deleting model 'Colaborativo'
        db.delete_table(u'editores_colaborativo')

        # Deleting model 'Competitivo'
        db.delete_table(u'editores_competitivo')

        # Deleting model 'Mensagem'
        db.delete_table(u'editores_mensagem')

        # Deleting model 'Mochila'
        db.delete_table(u'editores_mochila')

        # Removing M2M table for field instancia_mochila on 'Mochila'
        db.delete_table(db.shorten_name(u'editores_mochila_instancia_mochila'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'editores.agente': {
            'Meta': {'object_name': 'Agente'},
            'aventura_agente': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventura_agente'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Aventura']"}),
            'comportamento': ('django.db.models.fields.CharField', [], {'default': "'Agressivo'", 'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instancia': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'instancia'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.InstanciaObjeto']"}),
            'nome': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'proximidade': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'})
        },
        u'editores.agressivo': {
            'Meta': {'object_name': 'Agressivo', '_ormbases': [u'editores.Comportamento']},
            'avatar_vit': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'avatar_vit'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Avatar']"}),
            u'comportamento_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['editores.Comportamento']", 'unique': 'True', 'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'instancia_agressivo'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.InstanciaObjeto']"})
        },
        u'editores.autor': {
            'Meta': {'object_name': 'Autor', '_ormbases': [u'auth.User']},
            'dica_senha': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'icone_autor': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'editores.avatar': {
            'Meta': {'object_name': 'Avatar'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'aventura_avatar': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventura_avatar'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Aventura']"}),
            'aventureiro': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventureiro'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Jogador']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inst_objeto': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'inst_objeto'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.InstanciaObjeto']"}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'publico': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'editores.avatarativo': {
            'Meta': {'object_name': 'AvatarAtivo'},
            'avatar': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'avatar_ativo'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Avatar']"}),
            'aventura_ativa_avatar': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'aventura_ativa_avatar'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.AventuraAtiva']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': "'0'"}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': "'0'"})
        },
        u'editores.aventura': {
            'Meta': {'object_name': 'Aventura'},
            'autor': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'Autor'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'fim': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'editores.aventuraativa': {
            'Meta': {'object_name': 'AventuraAtiva'},
            'aventura': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventura'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Aventura']"}),
            'chave_acesso': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instancia': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            'joadores_aventura_ativa': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'joadores_aventura_ativa'", 'default': "''", 'to': u"orm['editores.Jogador']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'publica': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'editores.colaborativo': {
            'Meta': {'object_name': 'Colaborativo', '_ormbases': [u'editores.Comportamento']},
            'avatar_col': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'avatar_col'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Avatar']"}),
            u'comportamento_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['editores.Comportamento']", 'unique': 'True', 'primary_key': 'True'}),
            'obstaculoscl': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'obstaculoscl'", 'default': "''", 'to': u"orm['editores.InstanciaObjeto']", 'through': u"orm['editores.Mensagem']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
        },
        u'editores.competitivo': {
            'Meta': {'object_name': 'Competitivo', '_ormbases': [u'editores.Comportamento']},
            'avatar_comp': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'avatar_comp'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Avatar']"}),
            u'comportamento_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['editores.Comportamento']", 'unique': 'True', 'primary_key': 'True'}),
            'obstaculoscp': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'obstaculoscp'", 'default': "''", 'to': u"orm['editores.InstanciaObjeto']", 'through': u"orm['editores.Mensagem']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
        },
        u'editores.comportamento': {
            'Meta': {'object_name': 'Comportamento'},
            'agente': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'agente'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Agente']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos_inicial': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'pos_inicial'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.PosicaoGeografica']"})
        },
        u'editores.condicao': {
            'Meta': {'object_name': 'Condicao'},
            'enredo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'enredos'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Enredo']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ligacao': ('django.db.models.fields.CharField', [], {'default': "'GET_OBJ'", 'max_length': '20'}),
            'missao': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'condicoes_missao'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Missao']"}),
            'nome': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'operador': ('django.db.models.fields.CharField', [], {'default': "'AND'", 'max_length': '10'})
        },
        u'editores.condicaoativa': {
            'Meta': {'object_name': 'CondicaoAtiva'},
            'aventura_ativa_condicao': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventura_ativa_condicao'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.AventuraAtiva']"}),
            'condicao': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'condicao'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Condicao']"}),
            'estado_condicao': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'missao_ativa': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'missao_ativa'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.MissaoAtiva']"})
        },
        u'editores.condicaodialogoinstancia': {
            'Meta': {'object_name': 'CondicaoDialogoInstancia', '_ormbases': [u'editores.Condicao']},
            u'condicao_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['editores.Condicao']", 'unique': 'True', 'primary_key': 'True'}),
            'prefixo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'prefixo_cd_avateres'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Avatar']"}),
            'referencia_sufixo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'ref_sufixo_cd_inst_obj'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.InstanciaObjeto']"}),
            'sufixo': ('django.db.models.fields.CharField', [], {'default': "'DIALOGO_INICIAL'", 'max_length': '20'})
        },
        u'editores.condicaoinstanciaobjeto': {
            'Meta': {'object_name': 'CondicaoInstanciaObjeto', '_ormbases': [u'editores.Condicao']},
            u'condicao_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['editores.Condicao']", 'unique': 'True', 'primary_key': 'True'}),
            'prefixo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'prefixo_co_inst_obj'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.InstanciaObjeto']"}),
            'sufixo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'sufixo_co_inst_obj'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.InstanciaObjeto']"})
        },
        u'editores.condicaojogadorinstancia': {
            'Meta': {'object_name': 'CondicaoJogadorInstancia', '_ormbases': [u'editores.Condicao']},
            u'condicao_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['editores.Condicao']", 'unique': 'True', 'primary_key': 'True'}),
            'prefixo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'prefixo_cji_avateres'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Avatar']"}),
            'sufixo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'sufixo_cji_inst_obj'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.InstanciaObjeto']"})
        },
        u'editores.condicaojogadorobjeto': {
            'Meta': {'object_name': 'CondicaoJogadorObjeto', '_ormbases': [u'editores.Condicao']},
            u'condicao_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['editores.Condicao']", 'unique': 'True', 'primary_key': 'True'}),
            'prefixo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'prefixo_cjo_avateres'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Avatar']"}),
            'quantidade': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'sufixo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'sufixo_cjo__obj'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Objeto']"})
        },
        u'editores.enredo': {
            'Meta': {'object_name': 'Enredo'},
            'aventura': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventura_enredo'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Aventura']"}),
            'descricao': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'})
        },
        u'editores.enredofile': {
            'Meta': {'object_name': 'EnredoFile', '_ormbases': [u'editores.Enredo']},
            'enredo_file': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100'}),
            u'enredo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['editores.Enredo']", 'unique': 'True', 'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'SAU'", 'max_length': '10'})
        },
        u'editores.enredoinstancia': {
            'Meta': {'object_name': 'EnredoInstancia', '_ormbases': [u'editores.Enredo']},
            'enredo_instancia': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'enredo_instancia'", 'blank': 'True', 'to': u"orm['editores.InstanciaObjeto']"}),
            u'enredo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['editores.Enredo']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'editores.enredomensagem': {
            'Meta': {'object_name': 'EnredoMensagem', '_ormbases': [u'editores.Enredo']},
            'enredo_mensagem': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            u'enredo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['editores.Enredo']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'editores.icone': {
            'Meta': {'object_name': 'Icone'},
            'icone': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'editores.instanciaobjeto': {
            'Meta': {'object_name': 'InstanciaObjeto'},
            'aventura': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventura_inst_obj'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Aventura']"}),
            'dialogo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'encenacao': ('django.db.models.fields.CharField', [], {'default': "'DS'", 'max_length': '14', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagem_camera': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'tipo_imagem_camera'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.TipoImagem']"}),
            'imagem_mapa': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'tipo_imagem_mapa'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.TipoImagem']"}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'objeto': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'instancias_objeto'", 'blank': 'True', 'to': u"orm['editores.Objeto']"}),
            'proximidade': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'sugestao_objeto': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'sugestoes'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Sugestao']"}),
            'visivel': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'editores.jogador': {
            'Meta': {'object_name': 'Jogador', '_ormbases': [u'auth.User']},
            'dica_senha': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'editores.mensagem': {
            'Meta': {'object_name': 'Mensagem'},
            'colaborativo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'colaborativo'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Colaborativo']"}),
            'competitivo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'competitivo'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Competitivo']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instancia_objeto': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'instancia_objeto'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.InstanciaObjeto']"}),
            'mensagem': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'})
        },
        u'editores.missao': {
            'Meta': {'object_name': 'Missao'},
            'aventuras': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventuras'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Aventura']"}),
            'descricao': ('django.db.models.fields.CharField', [], {'default': "'descreva o objetivo da miss\\xc3\\xa3o'", 'max_length': '200'}),
            'enredo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'enredo_missao'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Enredo']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'tempo': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'editores.missaoativa': {
            'Meta': {'object_name': 'MissaoAtiva'},
            'aventura_ativa_missao': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventura_ativa_missao'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.AventuraAtiva']"}),
            'estado_missao': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'missao': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'missao'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.Missao']"})
        },
        u'editores.mochila': {
            'Meta': {'object_name': 'Mochila'},
            'avatar_mochila': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'avatar_mochila'", 'null': 'True', 'blank': 'True', 'to': u"orm['editores.AvatarAtivo']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instancia_mochila': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'instancia_mochila'", 'default': "''", 'to': u"orm['editores.InstanciaObjeto']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
        },
        u'editores.objeto': {
            'Meta': {'object_name': 'Objeto'},
            'coletavel': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'dialogo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'icone_objeto': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'icones'", 'to': u"orm['editores.Icone']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'quantidade': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '100'}),
            'tipo_objeto': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'objetos'", 'to': u"orm['editores.TipoObjeto']"})
        },
        u'editores.passivo': {
            'Meta': {'object_name': 'Passivo', '_ormbases': [u'editores.Comportamento']},
            u'comportamento_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['editores.Comportamento']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'editores.posicaogeografica': {
            'Meta': {'object_name': 'PosicaoGeografica'},
            'altitude': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instancia_objeto': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'pos_inst_objeto'", 'blank': 'True', 'to': u"orm['editores.InstanciaObjeto']"}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {})
        },
        u'editores.posinstanciaativa': {
            'Meta': {'object_name': 'PosInstanciaAtiva'},
            'altitude': ('django.db.models.fields.FloatField', [], {}),
            'aventura_ativa_instancia': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventura_ativa_instancia'", 'blank': 'True', 'to': u"orm['editores.AventuraAtiva']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instancia_objeto_ativa': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'instancia_objeto_ativa'", 'blank': 'True', 'to': u"orm['editores.InstanciaObjeto']"}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {})
        },
        u'editores.sugestao': {
            'Meta': {'object_name': 'Sugestao'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'proximidade': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'publico': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sugestao': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "u'STX'", 'max_length': '10'})
        },
        u'editores.tipoimagem': {
            'Meta': {'object_name': 'TipoImagem'},
            'descricao': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_play': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nome_img': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'IM'", 'max_length': '10'})
        },
        u'editores.tipoobjeto': {
            'Meta': {'object_name': 'TipoObjeto'},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'posicoes_geograficas': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'publico': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['editores']