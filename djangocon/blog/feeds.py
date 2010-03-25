from django.conf import settings
from django.contrib.syndication.feeds import Feed

from djangocon.blog.models import Post

class LatestFeed(Feed):
    title = 'djangocon.eu'
    description = 'blog'
    link = '/blog/rss/'

    def items(self):
        return Post.objects.published()[:10]

    def item_pubdate(self, item):
        return item.published
