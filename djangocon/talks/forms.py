from django import forms
from django.db.models import get_model

from djangocon.talks.models import TALK_LEVEL_CHOICES

class TalkForm(forms.ModelForm):
    speaker_name = forms.CharField(label="Name")
    speaker_email = forms.EmailField(label="E-Mail")
    speaker_website = forms.URLField(label="Website", required=False)
    speaker_twitter = forms.CharField(label="Twitter", required=False)
    
    allow_recording = forms.BooleanField(label='I permit the recording and streaming of my talk', required=True)
    
    level = forms.ChoiceField(label='Audience level', widget=forms.RadioSelect(), choices=TALK_LEVEL_CHOICES, required=True)

    class Meta:
        model = get_model('talks', 'Talk')
        fields = ('title', 'abstract', 'description', 'level',)

    
    def save(self, commit=True):
        if self.cleaned_data.get('speaker_email', None):
            Speaker = get_model('speakers', 'Speaker')
            s, created = Speaker.objects.get_or_create(email=self.cleaned_data['speaker_email'], defaults={
                'name': self.cleaned_data.get('speaker_name', ''),
                'twitter': self.cleaned_data.get('speaker_twitter', ''),
                'website': self.cleaned_data.get('speaker_website', ''),
            })
        talk = super(TalkForm, self).save(commit)
        talk.speakers = [s,]
        talk.save()