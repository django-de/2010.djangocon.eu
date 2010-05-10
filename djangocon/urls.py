from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

handler500 = 'djangocon.utils.views.server_error'

urlpatterns = patterns('',
    (r'^barn/', include(admin.site.urls)),
    url(r'^markitup/', include('markitup.urls'))
)

urlpatterns += patterns('djangocon',
    url(r'^$', 'utils.views.home', name='home'),
    url(r'^clear/$', 'subscribers.views.clear', name='clear'),
    url(r'^talks/', include('djangocon.talks.urls'), name='talks'),
    url(r'^blog/', include('djangocon.blog.urls'), name='blog'),
    url(r'^attendees/', include('djangocon.attendees.urls'), name='attendees'),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^legal/$', 'direct_to_template', {'template': 'legal_notices.html'}, name='legal_notices'),
    url(r'^register/$', 'direct_to_template', {'template': 'register.html'}, name='register'),
    url(r'^about/$', 'direct_to_template', {'template': 'about.html'}, name='about'),
    url(r'^wiki/$', 'redirect_to', {'url': 'http://djangocon.pbworks.com/'}, name='wiki'),
    url(r'^venue/$', 'direct_to_template', {'template': 'venue.html'}, name='venue'),
    url(r'^sponsoring/$', 'direct_to_template', {'template': 'sponsoring.html'}, name='sponsoring'),
    url(r'^schedule/$', 'direct_to_template', {'template': 'schedule.html'}, name='schedule'),
)

# Static Media File Serving
if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
        (r'', include('staticfiles.urls')),
    )
