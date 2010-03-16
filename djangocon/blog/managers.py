import datetime

from django.db.models import Manager

class PublishedManager(Manager):
    """
    Returns only blog posts which are published.
    """
    def published(self):
        return self.get_query_set().filter(draft=False, published__lte=datetime.datetime.now())