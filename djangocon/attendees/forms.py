from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from djangocon.attendees.models import Voucher, Attendee, TicketType, TicketBlock
from djangocon.attendees.utils import validate_vatid

class RegisterForm(forms.Form):
    ticket_type = forms.ModelChoiceField(label=_('Ticket type'), queryset=TicketType.objects.available(), required=True)
    first_name = forms.CharField(label=_('First name'), required=True)
    last_name = forms.CharField(label=_('Last name'), required=True)
    email = forms.EmailField(label=_('E-Mail'), required=True)
    voucher = forms.CharField(label=_('Voucher'), max_length=12, required=False)
    vat_id = forms.CharField(label=_('VAT-ID'), max_length=20, required=False)

    def clean_voucher(self):
        if not self.cleaned_data.get('ticket_type', None):
            return self.cleaned_data.get('voucher', '')

        if len(self.cleaned_data['voucher']) > 0:
            try:
                voucher = Voucher.objects.valid().get(code=self.cleaned_data['voucher'])
                return self.cleaned_data['voucher']
            except:
                raise forms.ValidationError(_('Voucher verification failed.'))
        elif self.cleaned_data['ticket_type'].voucher_needed:
            raise forms.ValidationError(_("A valid voucher is required to purchase the selected ticket."))
        return ''

    def clean_ticket_type(self):
        try:
            if self.cleaned_data['ticket_type'].max_attendees > 0 and self.cleaned_data['ticket_type'].attendees_count > self.cleaned_data['ticket_type'].max_attendees:
                raise forms.ValidationError(_('Ticket sold out.'))
            return self.cleaned_data['ticket_type']
        except:
            raise forms.ValidationError(_('Ticket sold out.'))

    def clean_vat_id(self):
        if not self.cleaned_data.get('ticket_type', None):
            return self.cleaned_data.get('vat_id', '')

        if len(settings.VAT_ID) > 0:
            if len(self.cleaned_data['vat_id']) > 0:
                if not validate_vatid(settings.VAT_ID, self.cleaned_data['vat_id']):
                      raise forms.ValidationError(_('VAT-ID verification failed.'))
                return self.cleaned_data['vat_id']
            elif self.cleaned_data['ticket_type'].vatid_needed:
                raise forms.ValidationError(_("A VAT-ID is required to purchase the selected ticket."))
            else:
                return ''
        else:
            return self.cleaned_data['vat_id']

    def clean(self):
        current_block = TicketBlock.objects.current_or_none()
        if not current_block or not current_block.open:
            raise forms.ValidationError(_("The current block of tickets is sold out!"))
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
