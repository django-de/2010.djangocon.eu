from django.conf.urls.defaults import *

from djangocon.blog.models import Post
from djangocon.blog.feeds import LatestBlogPostFeed

urlpatterns = patterns('djangocon.blog.views',
    url(r'^$', 'blog', name='blog'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        'blogpost_detail', name='blogpost_detail'),
)

urlpatterns += patterns ('',
    url(r'rss/$', LatestBlogPostFeed, name='blog_rss'),
)
