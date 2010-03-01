from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import datetime
import uuid

ATTENDEE_STATES = (
    ('new', _('new')),
    ('payment_pending', _('payment pending')),
    ('payment_received', _('payment received')),
    ('arrived', _('arrived')),
    ('canceled', _('canceled')),
)

TICKET_TYPES = (
    ('regular', _('Regular')),
    ('student', _('Student')),
    ('business', _('Business')),
    ('business_novat', _('Business (no VAT)')),
)

TICKET_FEES = {
    'regular':345,
    'student': 210,
    'business': 535.5,
    'business_novat': 450,
}

class VoucherManager(models.Manager):
    def valid(self):
        return self.filter(date_valid__gte=datetime.now(), is_used=False)

class Voucher(models.Model):
    code = models.CharField(_('Code'), max_length=12, blank=True)
    remarks = models.CharField(_('Remarks'), max_length=254, blank=True)
    date_valid = models.DateTimeField(_('Date (valid)'), blank=False)
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

class Attendee(models.Model):
    first_name = models.CharField(_('Last name'), max_length=250, blank=False)
    last_name = models.CharField(_('First name'), max_length=250, blank=False)
    email = models.EmailField(_('E-Mail'), max_length=250, blank=False)
    ticket_type = models.CharField(_('Ticket type'), max_length=25, choices=TICKET_TYPES, default=TICKET_TYPES[0][0], blank=False)
    state = models.CharField(_('State'), max_length=25, choices=ATTENDEE_STATES, default=ATTENDEE_STATES[0][0], blank=False)
    voucher = models.ForeignKey('Voucher', verbose_name=_('Voucher'), blank=True, null=True)
    vat_id = models.CharField(_('VAT-ID'), max_length=250, blank=True)
    payment_total = models.FloatField(_('Payment Total'), default=0)
    payment_data = models.TextField(_('Payment Data'), blank=True, default='')

    def __unicode__(self):
        return '%s %s - %s - %s' % (_('Attendee'), self.pk, self.ticket_type, self.state)

    class Meta:
        verbose_name = _('Attendee')
        verbose_name_plural = _('Attendee')
