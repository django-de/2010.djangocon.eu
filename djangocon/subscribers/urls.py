from django.conf.urls.defaults import *

urlpatterns = patterns('djangocon.subscribers.views',
    url(r'^subscribe/$', 'subscribe', name='subscribe'),
    url(r'^unsubscribe/(?P<hash>[0-9a-fA-F]+)/$', 'unsubscribe', name='unsubscribe'),
)


