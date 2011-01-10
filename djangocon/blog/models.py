import datetime

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User

from markdown import markdown
from smartypants import smartyPants
from djangocon.utils.models import DateAwareModel


class PublicManager(models.Manager):
    """Returns published posts which are not in the future."""

    def published(self):
        return self.get_query_set().filter(draft=False, publish_date__lte=datetime.datetime.now)

class Post(DateAwareModel):
    """A blog post."""
    author = models.ForeignKey(User, related_name='blog_posts', help_text='If left blank, will default to your user.')
    title = models.CharField('Title', blank=False, max_length=140)
    slug = models.SlugField('Slug', max_length=140, unique=True)
    draft = models.BooleanField('Draft', default=False, help_text='If checked, will not appear in the public site.')
    body_markdown = models.TextField('Body', blank=False, help_text = "Use markdown syntax")
    body = models.TextField('Body', blank=True)
    objects = PublicManager()
    
    class Meta:
        ordering = ('-publish_date',)
        unique_together = ('publish_date', 'slug')
        verbose_name = 'Blog Post'
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.body = unicode(markdown(smartyPants(self.body_markdown)))
        super(BlogPost, self).save(*args, **kwargs)
    
    @permalink
    def get_absolute_url(self):
        return('blogpost_detail', (), {
            'year': self.publish_date.year,
            'month': self.publish_date.month,
            'day': self.publish_date.day,
            'slug': self.slug,
        })

