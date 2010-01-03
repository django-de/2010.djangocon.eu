from django.db import models
from djangocon.speakers.models import Speaker

class Talk(models.Model):
    title = models.CharField(max_length=255)
    speakers = models.ManyToManyField(Speaker, related_name='speakers')
    abstract = models.TextField()
    accepted = models.BooleanField()
    scheduled = models.BooleanField()

    @property
    def speakers_list(self):
        return ', '.join(['%s' % speaker for speaker in self.speakers.all()])

    def __unicode__(self):
        return '%s' % self.title
