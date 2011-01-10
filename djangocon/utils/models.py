import datetime
from django.db import models

class TimeStampedModel(models.Model):
    timestamp = models.DateTimeField(editable=False)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.timestamp = datetime.datetime.now()
        return super(TimeStampedModel, self).save(*args, **kwargs)

class DateAwareModel(models.Model):
    publish_date = models.DateTimeField(default=datetime.datetime.now)
    modified_date = models.DateTimeField(default=datetime.datetime.now)
    created_date = models.DateTimeField(editable=False, default=datetime.datetime.now)
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.modified_date = datetime.datetime.now()
        return super(DateAwareModel, self).save(*args, **kwargs)

