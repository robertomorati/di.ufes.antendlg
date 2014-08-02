# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Comportamento'
        db.create_table('editor_objetos_comportamento', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos_inicial', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='pos_inicial', null=True, blank=True, to=orm['editor_objetos.PosicaoGeografica'])),
            ('agente', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='agente', null=True, blank=True, to=orm['editor_objetos.Agente'])),
        ))
        db.send_create_signal('editor_objetos', ['Comportamento'])

        # Adding model 'Mensagem'
        db.create_table('editor_objetos_mensagem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mensagem', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
        ))
        db.send_create_signal('editor_objetos', ['Mensagem'])

        # Adding model 'Passivo'
        db.create_table('editor_objetos_passivo', (
            ('comportamento_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['editor_objetos.Comportamento'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('editor_objetos', ['Passivo'])

        # Adding model 'Agente'
        db.create_table('editor_objetos_agente', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('instancia', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='instancia', null=True, blank=True, to=orm['editor_objetos.InstanciaObjeto'])),
            ('proximidade', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3)),
            ('comportamento', self.gf('django.db.models.fields.CharField')(default='Agressivo', max_length=1)),
        ))
        db.send_create_signal('editor_objetos', ['Agente'])


    def backwards(self, orm):
        # Deleting model 'Comportamento'
        db.delete_table('editor_objetos_comportamento')

        # Deleting model 'Mensagem'
        db.delete_table('editor_objetos_mensagem')

        # Deleting model 'Passivo'
        db.delete_table('editor_objetos_passivo')

        # Deleting model 'Agente'
        db.delete_table('editor_objetos_agente')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'editor_objetos.agente': {
            'Meta': {'object_name': 'Agente'},
            'comportamento': ('django.db.models.fields.CharField', [], {'default': "'Agressivo'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instancia': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'instancia'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.InstanciaObjeto']"}),
            'nome': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'proximidade': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'})
        },
        'editor_objetos.autor': {
            'Meta': {'object_name': 'Autor', '_ormbases': ['auth.User']},
            'dica_senha': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'icone_autor': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'editor_objetos.avatar': {
            'Meta': {'object_name': 'Avatar'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'aventura_avatar': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventura_avatar'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.Aventura']"}),
            'aventureiro': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventureiro'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.Jogador']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inst_objeto': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'inst_objeto'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.InstanciaObjeto']"}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': "'0'"}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': "'0'"}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'publico': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'editor_objetos.aventura': {
            'Meta': {'object_name': 'Aventura'},
            'autor': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'Autor'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'fim': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'editor_objetos.comportamento': {
            'Meta': {'object_name': 'Comportamento'},
            'agente': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'agente'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.Agente']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos_inicial': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'pos_inicial'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.PosicaoGeografica']"})
        },
        'editor_objetos.condicao': {
            'Meta': {'object_name': 'Condicao'},
            'enredo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'enredos'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.Enredo']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ligacao': ('django.db.models.fields.CharField', [], {'default': "'GET_OBJ'", 'max_length': '10'}),
            'missao': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'condicoes_missao'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.Missao']"}),
            'nome': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'operador': ('django.db.models.fields.CharField', [], {'default': "'AND'", 'max_length': '10'})
        },
        'editor_objetos.condicaodialogo': {
            'Meta': {'object_name': 'CondicaoDialogo', '_ormbases': ['editor_objetos.Condicao']},
            'condicao_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['editor_objetos.Condicao']", 'unique': 'True', 'primary_key': 'True'}),
            'prefixo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'prefixo_cd_avateres'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.Avatar']"}),
            'referencia_sufixo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'ref_sufixo_cd_inst_obj'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.InstanciaObjeto']"}),
            'sufixo': ('django.db.models.fields.CharField', [], {'default': "'DIALOGO_INICIAL'", 'max_length': '10'})
        },
        'editor_objetos.condicaojogador': {
            'Meta': {'object_name': 'CondicaoJogador', '_ormbases': ['editor_objetos.Condicao']},
            'condicao_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['editor_objetos.Condicao']", 'unique': 'True', 'primary_key': 'True'}),
            'prefixo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'prefixo_cj_avateres'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.Avatar']"}),
            'quantidade': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'sufixo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'sufixo_cj_inst_obj'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.InstanciaObjeto']"})
        },
        'editor_objetos.condicaoobjeto': {
            'Meta': {'object_name': 'CondicaoObjeto', '_ormbases': ['editor_objetos.Condicao']},
            'condicao_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['editor_objetos.Condicao']", 'unique': 'True', 'primary_key': 'True'}),
            'prefixo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'prefixo_co_inst_obj'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.InstanciaObjeto']"}),
            'sufixo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'sufixo_co_inst_obj'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.InstanciaObjeto']"})
        },
        'editor_objetos.enredo': {
            'Meta': {'object_name': 'Enredo'},
            'descricao': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'enredo': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'STX'", 'max_length': '10'})
        },
        'editor_objetos.icone': {
            'Meta': {'object_name': 'Icone'},
            'icone': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'editor_objetos.instanciaobjeto': {
            'Meta': {'object_name': 'InstanciaObjeto'},
            'aventura': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventura_inst_obj'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.Aventura']"}),
            'dialogo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'encenacao': ('django.db.models.fields.CharField', [], {'default': "'DS'", 'max_length': '14', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagem_camera': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'imagem_camera'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.TipoImagem']"}),
            'imagem_mapa': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'imagem_mapa'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.TipoImagem']"}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'objeto': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'instancias_objeto'", 'blank': 'True', 'to': "orm['editor_objetos.Objeto']"}),
            'proximidade': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'sugestao_objeto': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'sugestoes'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.Sugestao']"}),
            'visivel': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'editor_objetos.jogador': {
            'Meta': {'object_name': 'Jogador'},
            'aventura': ('django.db.models.fields.related.ManyToManyField', [], {'default': "''", 'related_name': "'aventuras_jogador'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['editor_objetos.Aventura']"}),
            'dica_senha': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'editor_objetos.mensagem': {
            'Meta': {'object_name': 'Mensagem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mensagem': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'})
        },
        'editor_objetos.missao': {
            'Meta': {'object_name': 'Missao'},
            'aventuras': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventuras'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.Aventura']"}),
            'descricao': ('django.db.models.fields.CharField', [], {'default': "'descreva o objetivo da miss\\xc3\\xa3o'", 'max_length': '200'}),
            'enredo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'enredo_missao'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.Enredo']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'tempo': ('django.db.models.fields.TimeField', [], {'null': 'True'})
        },
        'editor_objetos.nivelautor': {
            'Meta': {'object_name': 'NivelAutor'},
            'autor': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'autor'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.Autor']"}),
            'aventura': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventura'", 'null': 'True', 'blank': 'True', 'to': "orm['editor_objetos.Aventura']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nivel': ('django.db.models.fields.CharField', [], {'default': "'Principal'", 'max_length': '1'})
        },
        'editor_objetos.objeto': {
            'Meta': {'object_name': 'Objeto'},
            'coletavel': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'dialogo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'icone_objeto': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'icones'", 'to': "orm['editor_objetos.Icone']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'quantidade': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '100'}),
            'tipo_objeto': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'objetos'", 'to': "orm['editor_objetos.TipoObjeto']"})
        },
        'editor_objetos.passivo': {
            'Meta': {'object_name': 'Passivo', '_ormbases': ['editor_objetos.Comportamento']},
            'comportamento_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['editor_objetos.Comportamento']", 'unique': 'True', 'primary_key': 'True'})
        },
        'editor_objetos.posicaogeografica': {
            'Meta': {'object_name': 'PosicaoGeografica'},
            'altitude': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instancia_objeto': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'pos_inst_objeto'", 'blank': 'True', 'to': "orm['editor_objetos.InstanciaObjeto']"}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {})
        },
        'editor_objetos.sugestao': {
            'Meta': {'object_name': 'Sugestao'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'proximidade': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'sugestao': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'STX'", 'max_length': '10'})
        },
        'editor_objetos.tipoimagem': {
            'Meta': {'object_name': 'TipoImagem'},
            'descricao': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_play': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nome_img': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'IM'", 'max_length': '10'})
        },
        'editor_objetos.tipoobjeto': {
            'Meta': {'object_name': 'TipoObjeto'},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'posicoes_geograficas': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['editor_objetos']