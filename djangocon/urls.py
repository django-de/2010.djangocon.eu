from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^$', 'subscribers.views.home', name='home'),
    url(r'^subscribe/$', 'subscribers.views.subscribe', name='subscribe'),
    url(r'^clear/$', 'subscribers.views.clear', name='clear'),
)

# Static Media File Serving
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'', include('staticfiles.urls')),
    )