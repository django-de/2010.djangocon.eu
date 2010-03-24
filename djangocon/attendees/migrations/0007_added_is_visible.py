
from south.db import db
from django.db import models
from djangocon.attendees.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'TicketType.is_visible'
        db.add_column('attendees_tickettype', 'is_visible', orm['attendees.tickettype:is_visible'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'TicketType.is_visible'
        db.delete_column('attendees_tickettype', 'is_visible')
        
    
    
    models = {
        'attendees.attendee': {
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '250'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'payment_data': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'payment_total': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '25'}),
            'ticket_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attendees.TicketType']", 'null': 'True'}),
            'vat_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'voucher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attendees.Voucher']", 'null': 'True', 'blank': 'True'})
        },
        'attendees.ticketblock': {
            'date_valid_from': ('django.db.models.fields.DateTimeField', [], {}),
            'date_valid_to': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'max_attendees': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'attendees.tickettype': {
            'date_valid_from': ('django.db.models.fields.DateTimeField', [], {}),
            'date_valid_to': ('django.db.models.fields.DateTimeField', [], {}),
            'fee': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'max_attendees': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'vatid_needed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'voucher_needed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
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
