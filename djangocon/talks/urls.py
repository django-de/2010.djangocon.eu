from django.conf.urls.defaults import *

urlpatterns = patterns('djangocon.talks.views',
    url(r'^submit/$', 'submit', name='talks-submit'),
)
