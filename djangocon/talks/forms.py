from django import forms
from django.db.models import get_model

from djangocon.talks.models import TALK_LEVEL_CHOICES

class TalkForm(forms.ModelForm):
    speaker_name = forms.CharField(label="Name")
    speaker_email = forms.EmailField(label="E-Mail")
    speaker_website = forms.URLField(label="Website")
    speaker_twitter = forms.CharField(label="Twitter")
    
    class Meta:
        model = get_model('talks', 'Talk')
        fields = ('title', 'abstract', 'description', 'level',)
    
    def save(self, commit=True):
        if self.cleaned_data.get('speaker_twitter', None):
            Speaker = get_model('speakers', 'Speaker')
            s, created = Speaker.objects.get_or_create(twitter=self.cleaned_data['speaker_twitter'], defaults={
                'name': self.cleaned_data['speaker_name'],
                'email': self.cleaned_data['speaker_email'],
                'website': self.cleaned_data['speaker_website'],
            })
        talk = super(TalkForm, self).save(commit)
        talk.speakers = [s,]
        talk.save()