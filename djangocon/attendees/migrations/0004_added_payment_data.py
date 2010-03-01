
from south.db import db
from django.db import models
from djangocon.attendees.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Attendee.payment_data'
        db.add_column('attendees_attendee', 'payment_data', orm['attendees.attendee:payment_data'])
        
        # Changing field 'Voucher.code'
        # (to signature: django.db.models.fields.CharField(max_length=12, blank=True))
        db.alter_column('attendees_voucher', 'code', orm['attendees.voucher:code'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Attendee.payment_data'
        db.delete_column('attendees_attendee', 'payment_data')
        
        # Changing field 'Voucher.code'
        # (to signature: django.db.models.fields.CharField(max_length=12))
        db.alter_column('attendees_voucher', 'code', orm['attendees.voucher:code'])
        
    
    
    models = {
        'attendees.attendee': {
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '250'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'payment_data': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'payment_total': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '25'}),
            'ticket_type': ('django.db.models.fields.CharField', [], {'default': "'regular'", 'max_length': '25'}),
            'vat_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'voucher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attendees.Voucher']", 'null': 'True', 'blank': 'True'})
        },
        'attendees.voucher': {
            'code': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'date_valid': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_used': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'})
        }
    }
    
    complete_apps = ['attendees']
