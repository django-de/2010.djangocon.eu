import datetime

from django.db import models

class Subscriber(models.Model):
    """
    A subscriber who is interested in receiving updates via email.
    """
    
    subscribe_date = models.DateTimeField(default=datetime.datetime.now)
    email = models.EmailField()
    subscribed_from = models.IPAddressField()
        
    class Meta:
        ordering = ['subscribe_date',]
    
    def __unicode__(self):
        return self.email


class Tagline(models.Model):
    """
    A tagline from a given subscriber.
    """
    
    tagline = models.CharField(max_length=70)
    subscriber = models.ForeignKey(Subscriber, related_name='taglines')
    
    def __unicode__(self):
        return self.tagline