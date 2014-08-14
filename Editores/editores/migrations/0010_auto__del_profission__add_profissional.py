# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Profission'
        db.delete_table(u'editores_profission')

        # Adding model 'Profissional'
        db.create_table(u'editores_profissional', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'editores', ['Profissional'])


    def backwards(self, orm):
        # Adding model 'Profission'
        db.create_table(u'editores_profission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'editores', ['Profission'])

        # Deleting model 'Profissional'
        db.delete_table(u'editores_profissional')


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
            'autoria_estado': ('django.db.models.fields.CharField', [], {'default': "u'AI'", 'max_length': '10'}),
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
            'joadores_aventura_ativa': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'jogadores_aventura_ativa'", 'default': "''", 'to': u"orm['editores.Jogador']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
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
            'distancia': ('django.db.models.fields.IntegerField', [], {'default': '500', 'max_length': '10'}),
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
        u'editores.profissional': {
            'Meta': {'object_name': 'Profissional'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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