
from south.db import db
from django.db import models
from djangocon.subscribers.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Subscriber'
        db.create_table('subscribers_subscriber', (
            ('id', orm['subscribers.Subscriber:id']),
            ('subscribe_date', orm['subscribers.Subscriber:subscribe_date']),
            ('email', orm['subscribers.Subscriber:email']),
            ('subscribed_from', orm['subscribers.Subscriber:subscribed_from']),
        ))
        db.send_create_signal('subscribers', ['Subscriber'])
        
        # Adding model 'Tagline'
        db.create_table('subscribers_tagline', (
            ('id', orm['subscribers.Tagline:id']),
            ('tagline', orm['subscribers.Tagline:tagline']),
            ('subscriber', orm['subscribers.Tagline:subscriber']),
        ))
        db.send_create_signal('subscribers', ['Tagline'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Subscriber'
        db.delete_table('subscribers_subscriber')
        
        # Deleting model 'Tagline'
        db.delete_table('subscribers_tagline')
        
    
    
    models = {
        'subscribers.subscriber': {
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscribe_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'subscribed_from': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        },
        'subscribers.tagline': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taglines'", 'to': "orm['subscribers.Subscriber']"}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['subscribers']
