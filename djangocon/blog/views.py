from django.views.decorators.cache import cache_page
from django.views.generic import date_based, list_detail

from djangocon.blog.models import Post

@cache_page(60*5) # Cache for 5min.
def blogpost_detail(request, year, month, day, slug):
    return date_based.object_detail(
        request,
        queryset=Post.objects.published(),
        date_field='publish_date',
        month_format='%m',
        template_object_name='post',
        year=year, month=month, day=day, slug=slug)

@cache_page(60*5) # Cache for 5min.
def blog(request, page=None):
    return list_detail.object_list(
        request,
        queryset=Post.objects.published(),
        template_object_name='post',
        page=page)

