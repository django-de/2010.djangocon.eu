import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager
from markitup.fields import MarkupField

class PostManager(models.Manager):
    def published(self):
        return self.filter(published__gte=datetime.datetime.now(), draft=False)

class Post(models.Model):
    """A blog post."""
    author = models.ForeignKey(User, related_name='blog_posts')
    title = models.CharField(_('Title'), blank=False, max_length=80, unique=True)
    slug = models.SlugField(_('Slug'), unique=True)
    tease = MarkupField(_('Tease'), blank=True, help_text='Concise post description.')
    body = MarkupField(_('Body'), blank=False)
    published = models.DateTimeField(_('Publish Date'), default=datetime.datetime.now, help_text='Future-dated posts will only be published at the specified date and time.')
    updated_at = models.DateTimeField(_('Last Updated'), blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name="blog_posts_updated")
    draft = models.BooleanField(default=False, help_text='If checked, will not be displayed in the public site.')
    
    objects = PostManager()
    tags = TaggableManager()
    
    class Meta:
        ordering = ('-published',)
        verbose_name, verbose_name_plural = 'Blog Post', 'Blog Posts'
    
    def __unicode__(self):
        return self.title

    def save(self, **kwargs):
        self.updated_at = datetime.datetime.now()
        super(Post, self).save(**kwargs)

class PostResource(models.Model):
    """An external resource linked to a blog post."""
    post = models.ForeignKey(Post, related_name='resources')
    name = models.CharField(_('Name'), blank=False, max_length=80, unique=True)
    caption = models.CharField(_('Caption'), blank=True, max_length=255)
    url = models.URLField(_('URL'), blank=False, verify_exists=True)

    class Meta:
        ordering = ('name',)
        verbose_name, verbose_name_plural = 'Blog Post Resource', 'Blog Post Resources'

    def __unicode__(self):
        return self.name_en