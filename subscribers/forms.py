from django import forms

class SubscriberForm(forms.Form):
    email = forms.EmailField()
    tagline = forms.CharField(required=False, max_length=140)
