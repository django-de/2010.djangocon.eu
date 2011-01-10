from django.contrib.syndication.feeds import Feed

from djangocon.blog.models import Post

class LatestBlogPostFeed(Feed):
    title = 'djangocon.eu'
    description = 'blog'
    link = '/blog/rss/'
    
    def items(self):
        return Post.objects.published().order_by('-publish_date')[:10]
    
    def item_title(self, item):
        return item.title
    
    def item_pubdate(self, item):
        return item.publish_date
    
    def item_description(self, item):
        return item.body
