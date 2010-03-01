from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('djangocon.attendees.views',
    url(r'^$', 'register', name='attendees_register'),
    url(r'^payment/(?P<id>\d+)/$', 'paypal_redirect', name='attendees_paypal_redirect'),
    url(r'^payment/callback/$', 'paypal_callback', name='attendees_paypal_callback'),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^payment/done/$', 'direct_to_template', {'template': 'attendees/payment_done.html'}, name='attendees_paypal_done'),
    url(r'^payment/cancel/$', 'direct_to_template', {'template': 'attendees/payment_cancel.html'}, name='attendees_paypal_cancel'),
)