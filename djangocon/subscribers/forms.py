from django import forms

from djangocon.utils.html5widgets import EmailInput
from djangocon.subscribers.models import Subscriber

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        widgets = {
            'email': EmailInput(),
        }

