
from south.db import db
from django.db import models
from djangocon.attendees.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'TicketBlock'
        db.create_table('attendees_ticketblock', (
            ('id', orm['attendees.ticketblock:id']),
            ('name', orm['attendees.ticketblock:name']),
            ('max_attendees', orm['attendees.ticketblock:max_attendees']),
            ('is_active', orm['attendees.ticketblock:is_active']),
            ('date_valid_from', orm['attendees.ticketblock:date_valid_from']),
            ('date_valid_to', orm['attendees.ticketblock:date_valid_to']),
        ))
        db.send_create_signal('attendees', ['TicketBlock'])
        
        # Changing field 'Attendee.ticket_type'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['attendees.TicketType'], null=True))
        db.alter_column('attendees_attendee', 'ticket_type_id', orm['attendees.attendee:ticket_type'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'TicketBlock'
        db.delete_table('attendees_ticketblock')
        
        # Changing field 'Attendee.ticket_type'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['attendees.TicketType'], null=True, blank=False))
        db.alter_column('attendees_attendee', 'ticket_type_id', orm['attendees.attendee:ticket_type'])
        
    
    
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
