import hashlib
import datetime

from django.db import models

from djangocon.utils.models import TimeStampedModel

class Subscriber(TimeStampedModel):
    """
    A subscriber who is interested in receiving updates via email.
    """
    email = models.EmailField()
    hash = models.CharField(max_length=64, blank=True)
        
    class Meta:
        ordering = ['timestamp',]
    
    def __unicode__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        self.hash = hashlib.md5(self.email).hexdigest()
        super(Subscriber, self).save(*args, **kwargs)

