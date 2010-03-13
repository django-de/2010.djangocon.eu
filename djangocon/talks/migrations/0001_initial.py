# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from djangocon.talks.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Talk'
        db.create_table('talks_talk', (
            ('id', orm['talks.Talk:id']),
            ('title', orm['talks.Talk:title']),
            ('abstract', orm['talks.Talk:abstract']),
            ('description', orm['talks.Talk:description']),
            ('level', orm['talks.Talk:level']),
            ('accepted', orm['talks.Talk:accepted']),
            ('scheduled', orm['talks.Talk:scheduled']),
        ))
        db.send_create_signal('talks', ['Talk'])
        
        # Adding ManyToManyField 'Talk.speakers'
        db.create_table('talks_talk_speakers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('talk', models.ForeignKey(orm.Talk, null=False)),
            ('speaker', models.ForeignKey(orm['speakers.Speaker'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Talk'
        db.delete_table('talks_talk')
        
        # Dropping ManyToManyField 'Talk.speakers'
        db.delete_table('talks_talk_speakers')
        
    
    
    models = {
        'speakers.speaker': {
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'talks.talk': {
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'scheduled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['speakers.Speaker']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['talks']
