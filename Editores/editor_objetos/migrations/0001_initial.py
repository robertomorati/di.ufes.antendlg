# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TipoObjeto'
        db.create_table('editor_objetos_tipoobjeto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('posicoes_geograficas', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3)),
            ('dialogo', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('editor_objetos', ['TipoObjeto'])

        # Adding model 'Icone'
        db.create_table('editor_objetos_icone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('icone', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('editor_objetos', ['Icone'])

        # Adding model 'Sugestao'
        db.create_table('editor_objetos_sugestao', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(default=0, max_length=1)),
            ('sugestao', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('proximidade', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3)),
        ))
        db.send_create_signal('editor_objetos', ['Sugestao'])

        # Adding model 'Objeto'
        db.create_table('editor_objetos_objeto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('quantidade', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=100)),
            ('coletavel', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tipo_objeto', self.gf('django.db.models.fields.related.ForeignKey')(related_name='objetos', to=orm['editor_objetos.TipoObjeto'])),
            ('icone_objeto', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='icones', to=orm['editor_objetos.Icone'])),
        ))
        db.send_create_signal('editor_objetos', ['Objeto'])

        # Adding model 'Dialogo'
        db.create_table('editor_objetos_dialogo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dialogo', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('editor_objetos', ['Dialogo'])

        # Adding model 'PosicaoGeografica'
        db.create_table('editor_objetos_posicaogeografica', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('altitude', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('editor_objetos', ['PosicaoGeografica'])

        # Adding model 'InstanciaObjeto'
        db.create_table('editor_objetos_instanciaobjeto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('proximidade', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3)),
            ('visivel', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('encenacao', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('dialogo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dialogo_objeto', to=orm['editor_objetos.Dialogo'])),
            ('sugestao', self.gf('django.db.models.fields.related.ForeignKey')(default='Selecione a sugest\xc3\xa3o.', related_name='sugestao_objeto', blank=True, to=orm['editor_objetos.Sugestao'])),
        ))
        db.send_create_signal('editor_objetos', ['InstanciaObjeto'])

        # Adding M2M table for field posicao_geografica_ on 'InstanciaObjeto'
        db.create_table('editor_objetos_instanciaobjeto_posicao_geografica_', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('instanciaobjeto', models.ForeignKey(orm['editor_objetos.instanciaobjeto'], null=False)),
            ('posicaogeografica', models.ForeignKey(orm['editor_objetos.posicaogeografica'], null=False))
        ))
        db.create_unique('editor_objetos_instanciaobjeto_posicao_geografica_', ['instanciaobjeto_id', 'posicaogeografica_id'])

        # Adding model 'ImagemObjeto'
        db.create_table('editor_objetos_imagemobjeto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imagem', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('editor_objetos', ['ImagemObjeto'])

        # Adding model 'TipoImagem'
        db.create_table('editor_objetos_tipoimagem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(default=0, max_length=1)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('editor_objetos', ['TipoImagem'])

        # Adding model 'Autor'
        db.create_table('editor_objetos_autor', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('dica_senha', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('editor_objetos', ['Autor'])

        # Adding model 'Aventura'
        db.create_table('editor_objetos_aventura', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('inicio', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('fim', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(default=0.0, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(default=0.0, blank=True)),
        ))
        db.send_create_signal('editor_objetos', ['Aventura'])

        # Adding model 'NivelAutor'
        db.create_table('editor_objetos_nivelautor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('editor_objetos', ['NivelAutor'])


    def backwards(self, orm):
        # Deleting model 'TipoObjeto'
        db.delete_table('editor_objetos_tipoobjeto')

        # Deleting model 'Icone'
        db.delete_table('editor_objetos_icone')

        # Deleting model 'Sugestao'
        db.delete_table('editor_objetos_sugestao')

        # Deleting model 'Objeto'
        db.delete_table('editor_objetos_objeto')

        # Deleting model 'Dialogo'
        db.delete_table('editor_objetos_dialogo')

        # Deleting model 'PosicaoGeografica'
        db.delete_table('editor_objetos_posicaogeografica')

        # Deleting model 'InstanciaObjeto'
        db.delete_table('editor_objetos_instanciaobjeto')

        # Removing M2M table for field posicao_geografica_ on 'InstanciaObjeto'
        db.delete_table('editor_objetos_instanciaobjeto_posicao_geografica_')

        # Deleting model 'ImagemObjeto'
        db.delete_table('editor_objetos_imagemobjeto')

        # Deleting model 'TipoImagem'
        db.delete_table('editor_objetos_tipoimagem')

        # Deleting model 'Autor'
        db.delete_table('editor_objetos_autor')

        # Deleting model 'Aventura'
        db.delete_table('editor_objetos_aventura')

        # Deleting model 'NivelAutor'
        db.delete_table('editor_objetos_nivelautor')


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
            'dica_senha': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'editor_objetos.aventura': {
            'Meta': {'object_name': 'Aventura'},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'fim': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'editor_objetos.dialogo': {
            'Meta': {'object_name': 'Dialogo'},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'dialogo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'editor_objetos.icone': {
            'Meta': {'object_name': 'Icone'},
            'icone': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'editor_objetos.imagemobjeto': {
            'Meta': {'object_name': 'ImagemObjeto'},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagem': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'editor_objetos.instanciaobjeto': {
            'Meta': {'object_name': 'InstanciaObjeto'},
            'dialogo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dialogo_objeto'", 'to': "orm['editor_objetos.Dialogo']"}),
            'encenacao': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'posicao_geografica_': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pos_geo_inst_objeto'", 'symmetrical': 'False', 'to': "orm['editor_objetos.PosicaoGeografica']"}),
            'proximidade': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'sugestao': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Selecione a sugest\\xc3\\xa3o.'", 'related_name': "'sugestao_objeto'", 'blank': 'True', 'to': "orm['editor_objetos.Sugestao']"}),
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
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {})
        },
        'editor_objetos.sugestao': {
            'Meta': {'object_name': 'Sugestao'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proximidade': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'sugestao': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'})
        },
        'editor_objetos.tipoimagem': {
            'Meta': {'object_name': 'TipoImagem'},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'})
        },
        'editor_objetos.tipoobjeto': {
            'Meta': {'object_name': 'TipoObjeto'},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'dialogo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'posicoes_geograficas': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['editor_objetos']