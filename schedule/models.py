from django.db import models
from talks.models import Talk

class Track(models.Model):
    name = models.CharField(max_length=75)

    def __unicode__(self):
        return self.name

class Day(models.Model):
    track = models.ForeignKey(Track)
    date = models.DateField()

    def __unicode__(self):
        return '%s - %s' % (self.track, self.date)

    class Meta:
        ordering = ('date',)

class Slot(models.Model):
    day = models.ForeignKey(Day)
    starttime = models.TimeField()
    endtime = models.TimeField()
    talk = models.ForeignKey(Talk, limit_choices_to={'accepted': True, 'scheduled': False})

    def save(self, *args, **kwargs):
        self.talk.scheduled = True
        self.talk.save()
        super(Slot, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s/%s/%s: %s' % (self.day.track, self.day, self.starttime, self.talk)

    class Meta:
        ordering = ('day__date', 'starttime',)
