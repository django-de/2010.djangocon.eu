from django.db import models

class Speaker(models.Model):
    name = models.CharField(max_length=75)
    email = models.EmailField()
    website = models.URLField(blank=True)
    twitter = models.CharField(max_length=75, blank=True)

    def __unicode__(self):
        return self.name
