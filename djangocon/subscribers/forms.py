from django import forms

class SubscriberForm(forms.Form):
    email = forms.EmailField()
    tagline = forms.CharField(label="Tagline (optional)", required=False, max_length=50)
    
class SubscriberEmailForm(forms.Form):
    email = forms.EmailField()


