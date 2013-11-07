# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ImagemObjeto'
        db.delete_table('editor_objetos_imagemobjeto')

        # Adding field 'TipoImagem.img'
        db.add_column('editor_objetos_tipoimagem', 'img',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PosicaoGeografica.instancia_objeto'
        db.add_column('editor_objetos_posicaogeografica', 'instancia_objeto',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='pos_inst_objeto', blank=True, to=orm['editor_objetos.InstanciaObjeto']),
                      keep_default=False)

        # Removing M2M table for field instancia_objeto on 'PosicaoGeografica'
        db.delete_table('editor_objetos_posicaogeografica_instancia_objeto')

        # Adding field 'InstanciaObjeto.aventura'
        db.add_column('editor_objetos_instanciaobjeto', 'aventura',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='aventura', blank=True, to=orm['editor_objetos.Aventura']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'ImagemObjeto'
        db.create_table('editor_objetos_imagemobjeto', (
            ('imagem', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('editor_objetos', ['ImagemObjeto'])

        # Deleting field 'TipoImagem.img'
        db.delete_column('editor_objetos_tipoimagem', 'img')

        # Deleting field 'PosicaoGeografica.instancia_objeto'
        db.delete_column('editor_objetos_posicaogeografica', 'instancia_objeto_id')

        # Adding M2M table for field instancia_objeto on 'PosicaoGeografica'
        db.create_table('editor_objetos_posicaogeografica_instancia_objeto', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('posicaogeografica', models.ForeignKey(orm['editor_objetos.posicaogeografica'], null=False)),
            ('instanciaobjeto', models.ForeignKey(orm['editor_objetos.instanciaobjeto'], null=False))
        ))
        db.create_unique('editor_objetos_posicaogeografica_instancia_objeto', ['posicaogeografica_id', 'instanciaobjeto_id'])

        # Deleting field 'InstanciaObjeto.aventura'
        db.delete_column('editor_objetos_instanciaobjeto', 'aventura_id')


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
        'editor_objetos.autor': {
            'Meta': {'object_name': 'Autor', '_ormbases': ['auth.User']},
            'dica_senha': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'icone_autor': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
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
        'editor_objetos.icone': {
            'Meta': {'object_name': 'Icone'},
            'icone': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'editor_objetos.instanciaobjeto': {
            'Meta': {'object_name': 'InstanciaObjeto'},
            'aventura': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'aventura'", 'blank': 'True', 'to': "orm['editor_objetos.Aventura']"}),
            'dialogo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'encenacao': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'num_instancia': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'objeto': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'instancias_objeto'", 'blank': 'True', 'to': "orm['editor_objetos.Objeto']"}),
            'proximidade': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'sugestao': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'sugestao_objeto'", 'blank': 'True', 'to': "orm['editor_objetos.Sugestao']"}),
            'visivel': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'editor_objetos.nivelautor': {
            'Meta': {'object_name': 'NivelAutor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'proximidade': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'sugestao': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'})
        },
        'editor_objetos.tipoimagem': {
            'Meta': {'object_name': 'TipoImagem'},
            'descricao': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'})
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