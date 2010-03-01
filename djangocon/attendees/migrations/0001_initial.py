
from south.db import db
from django.db import models
from djangocon.attendees.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Voucher'
        db.create_table('attendees_voucher', (
            ('id', orm['attendees.Voucher:id']),
            ('code', orm['attendees.Voucher:code']),
            ('remarks', orm['attendees.Voucher:remarks']),
            ('date_valid', orm['attendees.Voucher:date_valid']),
            ('is_used', orm['attendees.Voucher:is_used']),
        ))
        db.send_create_signal('attendees', ['Voucher'])
        
        # Adding model 'Attendee'
        db.create_table('attendees_attendee', (
            ('id', orm['attendees.Attendee:id']),
            ('first_name', orm['attendees.Attendee:first_name']),
            ('last_name', orm['attendees.Attendee:last_name']),
            ('email', orm['attendees.Attendee:email']),
            ('state', orm['attendees.Attendee:state']),
            ('voucher', orm['attendees.Attendee:voucher']),
            ('vat_id', orm['attendees.Attendee:vat_id']),
        ))
        db.send_create_signal('attendees', ['Attendee'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Voucher'
        db.delete_table('attendees_voucher')
        
        # Deleting model 'Attendee'
        db.delete_table('attendees_attendee')
        
    
    
    models = {
        'attendees.attendee': {
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '250'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '25'}),
            'vat_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'voucher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attendees.Voucher']", 'null': 'True', 'blank': 'True'})
        },
        'attendees.voucher': {
            'code': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'date_valid': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_used': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
        }
    }
    
    complete_apps = ['attendees']
