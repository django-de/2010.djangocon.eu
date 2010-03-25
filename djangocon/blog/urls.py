from django.conf.urls.defaults import *

from djangocon.blog.models import Post
from djangocon.blog.feeds import LatestFeed

urlpatterns = patterns('djangocon.blog.views',
    url(r'^$', 'blog_index', name='blog_index'),
    
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        'blog_archive_month', name='blog_archive_month'),
    
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        'blog_detail', name='blog_detail'),
    
    url(r'^tag/(?P<slug>[-\w]+)/$',
        'blog_archive_tag', name='blog_archive_tag'),
)

urlpatterns += patterns('',
    url(r'^rss/$', 
        'django.contrib.syndication.views.feed',
        {'feed_dict': {'latest': LatestFeed}, 'url': 'latest',}
        , name='blog_rss'),
)
