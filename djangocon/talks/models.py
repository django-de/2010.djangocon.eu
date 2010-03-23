# -*- coding: utf-8 -*-

from django.db import models

from djangocon.speakers.models import Speaker

TALK_LEVEL_BEGINNER = 1
TALK_LEVEL_INTERMEDIATE = 2
TALK_LEVEL_ADVANCED = 3
TALK_LEVEL_CHOICES = (
    (TALK_LEVEL_BEGINNER, 'Beginner'),
    (TALK_LEVEL_INTERMEDIATE, 'Intermediate'),
    (TALK_LEVEL_ADVANCED, 'Advanced'),
)

class Talk(models.Model):
    title = models.CharField(verbose_name="Talk title", max_length=255)
    speakers = models.ManyToManyField(Speaker, related_name='speakers')
    abstract = models.TextField(help_text="Max 100 words; will be published in the schedule")
    description = models.TextField(help_text="Detailed outline for review; will not be published")
    level = models.PositiveSmallIntegerField(verbose_name="Audience level", choices=TALK_LEVEL_CHOICES)
    
    accepted = models.BooleanField()
    scheduled = models.BooleanField()
    
    @property
    def speakers_list(self):
        return ', '.join(['%s' % speaker for speaker in self.speakers.all()])
    
    def __unicode__(self):
        return '%s' % self.title
