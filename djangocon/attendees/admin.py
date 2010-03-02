from django.contrib import admin
from djangocon.attendees.models import Attendee, Voucher, TicketType, TicketBlock

class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'first_name', 'last_name', 'email', 'date_added', 'ticket_type', 'state',)
    list_filter = ('state', 'ticket_type',)
    search_fields = ('first_name', 'last_name', 'email',)

admin.site.register(Attendee, AttendeeAdmin)

class VoucherAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'is_used',)
    list_filter = ('is_used',)

admin.site.register(Voucher, VoucherAdmin)

class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'fee', 'is_active', 'attendees_count', 'max_attendees','date_valid_from' , 'date_valid_to',)
    list_filter = ('is_active',)

admin.site.register(TicketType, TicketTypeAdmin)

class TicketBlockAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'is_active', 'open', 'attendees_count', 'max_attendees', 'date_valid_from', 'date_valid_to',)

admin.site.register(TicketBlock, TicketBlockAdmin)