from django import template
from django.template.loader import render_to_string
from djangocon.blog.utils import make_cloud
from djangocon.blog.models import Post
from taggit.models import Tag
register = template.Library()

@register.simple_tag
def blog_tagcloud():
    return render_to_string(
        'blog/tagcloud.html',
        {'tags': make_cloud(Tag.objects.all())}
    )
