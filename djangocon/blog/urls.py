from django.conf.urls.defaults import *

from djangocon.blog.models import Post
from djangocon.blog.feeds import LatestFeed

entry_info_dict = {
    'queryset': Post.objects.published(),
    'date_field': 'published',
    'extra_context': {
        'blog_tags': Post.tags.all(),
        'blog_months': Post.objects.published().dates('published', 'month', order='DESC')
    } 
}

tag_info_dict = {
    'queryset': Post.tags.all(),
    'template_name': 'blog/post_archive_tag.html',
}

urlpatterns = patterns('django.views.generic',
    url(r'^$',
        'date_based.archive_index',
        entry_info_dict,
        'blog_index'),
    #(r'^(?P<year>\d{4})/$',
    #    'archive_year',
    #    entry_info_dict,
    #    'blog_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        'date_based.archive_month',
        entry_info_dict,
        'blog_archive_month'),
    #(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
    #    'archive_day',
    #    entry_info_dict,
    #    'blog_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        'date_based.object_detail',
        entry_info_dict,
        'blog_detail'),
    
    url(r'^tag/(?P<slug>[-\w]+)/$',
        'list_detail.object_detail',
        tag_info_dict,
        'blog_archive_tag'),
)
urlpatterns += patterns('',
    url(r'^rss/$', 
        'django.contrib.syndication.views.feed',
        {'feed_dict': {'latest': LatestFeed}, 'url': 'latest',}
        , name='blog_rss'),
)
