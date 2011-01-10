from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

from staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()


handler500 = 'djangocon.utils.views.server_error'

urlpatterns = patterns('',
    (r'^', include('djangocon.core.urls')),
    (r'^', include('djangocon.subscribers.urls')),
    (r'^blog/', include('djangocon.blog.urls')),
    (r'^barn/', include(admin.site.urls)),
)

# Static Media File Serving
if settings.SERVE_STATIC_FILES:
    urlpatterns += staticfiles_urlpatterns()
