
from south.db import db
from django.db import models
from djangocon.schedule.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Slot'
        db.create_table('schedule_slot', (
            ('id', orm['schedule.Slot:id']),
            ('day', orm['schedule.Slot:day']),
            ('starttime', orm['schedule.Slot:starttime']),
            ('endtime', orm['schedule.Slot:endtime']),
            ('talk', orm['schedule.Slot:talk']),
        ))
        db.send_create_signal('schedule', ['Slot'])
        
        # Adding model 'Track'
        db.create_table('schedule_track', (
            ('id', orm['schedule.Track:id']),
            ('name', orm['schedule.Track:name']),
        ))
        db.send_create_signal('schedule', ['Track'])
        
        # Adding model 'Day'
        db.create_table('schedule_day', (
            ('id', orm['schedule.Day:id']),
            ('track', orm['schedule.Day:track']),
            ('date', orm['schedule.Day:date']),
        ))
        db.send_create_signal('schedule', ['Day'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Slot'
        db.delete_table('schedule_slot')
        
        # Deleting model 'Track'
        db.delete_table('schedule_track')
        
        # Deleting model 'Day'
        db.delete_table('schedule_day')
        
    
    
    models = {
        'schedule.day': {
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Track']"})
        },
        'schedule.slot': {
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Day']"}),
            'endtime': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'starttime': ('django.db.models.fields.TimeField', [], {}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['talks.Talk']"})
        },
        'schedule.track': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
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
    
    complete_apps = ['schedule']
