from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from djangocon.attendees.models import Voucher, Attendee, TICKET_TYPES
from djangocon.attendees.utils import validate_vatid

class RegisterForm(forms.Form):
    ticket_type = forms.ChoiceField(label=_('Ticket type'), choices=TICKET_TYPES, required=True)
    first_name = forms.CharField(label=_('First name'), required=True)
    last_name = forms.CharField(label=_('Last name'), required=True)
    email = forms.EmailField(label=_('E-Mail'), required=True)
    voucher = forms.CharField(label=_('Voucher'), max_length=12, required=False)
    vat_id = forms.CharField(label=_('VAT-ID'), max_length=20, required=False)

    def clean_voucher(self):
        if len(self.cleaned_data['voucher']) > 0:
            try:
                voucher = Voucher.objects.valid().get(code=self.cleaned_data['voucher'])
                return self.cleaned_data['voucher']
            except:
                raise forms.ValidationError(_('Voucher verification failed.'))
        return ''

    def clean_vat_id(self):
        if len(self.cleaned_data['vat_id']) > 0 and len(settings.VAT_ID) > 0:
            if not validate_vatid(settings.VAT_ID, self.cleaned_data['vat_id']):
                  raise forms.ValidationError(_('VAT-ID verification failed.'))
            return self.cleaned_data['vat_id']
        return ''

    def clean(self):
        if 'ticket_type' in self.cleaned_data:
            if self.cleaned_data['ticket_type'] == 'student' and len(self.cleaned_data.get('voucher', '')) < 1:
                raise forms.ValidationError(_("You need a voucher to use the student rate."))
            if self.cleaned_data['ticket_type'] == 'business_novat' and len(self.cleaned_data.get('vat_id', '')) < 1:
                raise forms.ValidationError(_("You need a VAT-ID to use the business rate without VAT."))
        return self.cleaned_data

    def save(self, *args, **kwargs):
        new_attendee = Attendee.objects.create(
            ticket_type = self.cleaned_data['ticket_type'],
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name'],
            email = self.cleaned_data['email'],
            vat_id = self.cleaned_data.get('vat_id', ''),
        )

        if len(self.cleaned_data['voucher']) > 0:
            try:
                voucher = Voucher.objects.get(code=self.cleaned_data['voucher'])
                voucher.is_used = True
                voucher.save()
                new_attendee.voucher = voucher
                new_attendee.save()
            except:
                pass

        return new_attendee
