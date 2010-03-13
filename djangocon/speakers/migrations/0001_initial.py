
from south.db import db
from django.db import models
from djangocon.speakers.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Speaker'
        db.create_table('speakers_speaker', (
            ('id', orm['speakers.Speaker:id']),
            ('name', orm['speakers.Speaker:name']),
            ('email', orm['speakers.Speaker:email']),
            ('website', orm['speakers.Speaker:website']),
            ('twitter', orm['speakers.Speaker:twitter']),
        ))
        db.send_create_signal('speakers', ['Speaker'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Speaker'
        db.delete_table('speakers_speaker')
        
    
    
    models = {
        'speakers.speaker': {
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }
    
    complete_apps = ['speakers']
