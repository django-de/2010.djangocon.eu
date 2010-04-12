from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import datetime
import uuid
from urllib import urlencode
from urllib2 import urlopen

ATTENDEE_STATES = (
    ('new', _('new')),
    ('payment_started', _('payment started')),
    ('payment_pending', _('payment pending')),
    ('payment_received', _('payment received')),
    ('arrived', _('arrived')),
    ('canceled', _('canceled')),
)

class VoucherManager(models.Manager):
    def valid(self):
        return self.filter(date_valid__gte=datetime.now(), is_used=False)

class Voucher(models.Model):
    code = models.CharField(_('Code'), max_length=12, blank=True)
    remarks = models.CharField(_('Remarks'), max_length=254, blank=True)
    date_valid = models.DateTimeField(_('Date (valid)'), blank=False, help_text=_('The voucher is valid until this date'))
    is_used = models.BooleanField(_('Is used'), default=False)

    objects = VoucherManager()

    def __unicode__(self):
        return '%s %s' % (_('Voucher'), self.code)

    def save(self, *args, **kwargs):
        if len(self.code) < 1:
            self.code = str(uuid.uuid4())[-12:]
        super(Voucher, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Voucher')
        verbose_name_plural = _('Vouchers')

class TicketTypeManager(models.Manager):
    def available(self):
        return self.filter(date_valid_from__lte=datetime.now(), date_valid_to__gte=datetime.now(), is_active=True)

class TicketType(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    fee = models.FloatField(_('Fee'), default=0)
    remarks = models.CharField(_('Remarks'), max_length=254, blank=True)
    max_attendees = models.PositiveIntegerField(_('Max attendees'), default=0, help_text='0 means no limit')
    is_active = models.BooleanField(_('Is active'), default=False)
    is_visible = models.BooleanField(_('Is visible'), help_text=_('Should this ticket type displayed on the startpage?'), default=True)
    voucher_needed = models.BooleanField(_('Voucher needed'), default=False)
    vatid_needed = models.BooleanField(_('VAT-ID needed'), default=False)
    date_valid_from = models.DateTimeField(_('Date (valid from)'), blank=False)
    date_valid_to = models.DateTimeField(_('Date (valid to)'), blank=False)

    objects = TicketTypeManager()

    def __unicode__(self):
        return '%s (%.2f EUR)' % (self.name, self.fee)

    @property
    def attendees_count(self):
        return self.attendee_set.count()

    class Meta:
        ordering = ('name', 'vatid_needed', 'voucher_needed',)
        verbose_name = _('Ticket type')
        verbose_name_plural = _('Ticket type')

class TicketBlockManager(models.Manager):
    def current(self):
        return self.get(date_valid_from__lte=datetime.now(), date_valid_to__gte=datetime.now(), is_active=True)

    def current_or_none(self):
        try:
            return self.current()
        except:
            return None

class TicketBlock(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    max_attendees = models.PositiveIntegerField(_('Max attendees'), default=0)
    is_active = models.BooleanField(_('Is active'), default=False)
    date_valid_from = models.DateTimeField(_('Date (valid from)'), blank=False)
    date_valid_to = models.DateTimeField(_('Date (valid to)'), blank=False)

    objects = TicketBlockManager()

    def __unicode__(self):
        return '%s (%s - %s)' % (self.name, self.date_valid_from, self.date_valid_to)

    @property
    def open(self):
        return self.max_attendees > self.attendees_count

    @property
    def attendees_count(self):
        return Attendee.objects.filter(date_added__gte=self.date_valid_from, date_added__lte=self.date_valid_to).count()

    class Meta:
        verbose_name = _('Ticket block')
        verbose_name_plural = _('Ticket block')

class Attendee(models.Model):
    first_name = models.CharField(_('First name'), max_length=250, blank=False)
    last_name = models.CharField(_('Last name'), max_length=250, blank=False)
    email = models.EmailField(_('E-Mail'), max_length=250, blank=False)
    date_added = models.DateTimeField(_('Date (added)'), blank=False, default=datetime.now)
    ticket_type = models.ForeignKey('TicketType', verbose_name=_('Ticket type'), null=True, blank=False)
    state = models.CharField(_('State'), max_length=25, choices=ATTENDEE_STATES, default=ATTENDEE_STATES[0][0], blank=False)
    voucher = models.ForeignKey('Voucher', verbose_name=_('Voucher'), blank=True, null=True)
    vat_id = models.CharField(_('VAT-ID'), max_length=250, blank=True)
    payment_total = models.FloatField(_('Payment Total'), default=0)
    payment_data = models.TextField(_('Payment Data'), blank=True, default='')

    def __unicode__(self):
        return '%s %s - %s - %s' % (_('Attendee'), self.pk, self.ticket_type, self.state)

    def payment_fee(self):
        if not self.ticket_type.vatid_needed:
            return self.payment_total / 1.19
        else:
            return self.payment_total

    def payment_tax(self):
        if not self.ticket_type.vatid_needed:
            return self.payment_total - (self.payment_total / 1.19)
        else:
            return 0.0

    class Meta:
        verbose_name = _('Attendee')
        verbose_name_plural = _('Attendees')



def add_or_update_campaign_monitor_record(sender, **kwargs):
    attendee = kwargs['instance']
    data = urlencode({
        'ApiKey': settings.CAMPAIGNMONITOR_APIKEY,
        'ListID': settings.CAMPAIGNMONITOR_ATTENDEES_LIST_ID,
        'Email': attendee.email,
        'Name': u"%s %s" % (attendee.first_name, attendee.last_name),
    })
    url = urlopen('http://api.createsend.com/api/api.asmx/Subscriber.AddAndResubscribe', data)

#post_save.connect(add_or_update_campaign_monitor_record, sender=Attendee)

def delete_campaign_monitor_record(sender, **kwargs):
    attendee = kwargs['instance']
    data = urlencode({
        'ApiKey': settings.CAMPAIGNMONITOR_APIKEY,
        'ListID': settings.CAMPAIGNMONITOR_ATTENDEES_LIST_ID,
        'Email': attendee.email,
    })
    url = urlopen('http://api.createsend.com/api/api.asmx/Subscriber.Unsubscribe', data)

#post_delete.connect(delete_campaign_monitor_record, sender=Attendee)

