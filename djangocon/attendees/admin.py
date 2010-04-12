from django.contrib import admin
from djangocon.attendees.models import Attendee, Voucher, TicketType, TicketBlock
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'first_name', 'last_name', 'email', 'date_added', 'ticket_type', 'state',)
    list_filter = ('state', 'ticket_type',)
    search_fields = ('first_name', 'last_name', 'email',)

    actions = ['resend_confirmation',]

    def resend_confirmation(self, request, queryset):
        sent = 0
        for attendee in queryset.filter(state='payment_received'):
            send_mail(
                'Booking confirmation',
                render_to_string('attendees/mail_payment_received.html', {'attendee': attendee}),
                settings.DEFAULT_MAIL_FROM,
                [attendee.email, 'kontakt@django-de.org',],
                fail_silently=True
            )
            sent += 1

        if sent == 1:
            message_bit = '1 mail was'
        else:
            message_bit = '%s mails were' % sent
        self.message_user(request, '%s successfully sent.' % message_bit)
    resend_confirmation.short_description = 'Resend confirmation to selected %(verbose_name_plural)s'

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