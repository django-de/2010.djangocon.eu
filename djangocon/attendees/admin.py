from django.contrib import admin
from djangocon.attendees.models import Attendee, Voucher

class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'first_name', 'last_name', 'email', 'ticket_type', 'state',)
    list_filter = ('state', 'ticket_type',)
    search_fields = ('first_name', 'last_name', 'email',)

admin.site.register(Attendee, AttendeeAdmin)

class VoucherAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'is_used',)
    list_filter = ('is_used',)

admin.site.register(Voucher, VoucherAdmin)