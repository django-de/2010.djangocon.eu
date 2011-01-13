from django import http
from django.conf import settings
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from djangocon.subscribers.models import Subscriber
from djangocon.subscribers.forms import SubscriberForm
from djangocon.blog.models import Post
from djangocon.attendees.models import TicketType

try:
    subscription_cookie = getattr(settings, 'SUBSCRIPTION_COOKIE_NAME')
except AttributeError:
    raise ImproperlyConfigured("SUBSCRIPTION_COOKIE_NAME must be specified in settings.")

def server_error(request, template_name='500.html'):
    """
    A custom 500 error handler.

    Templates: `500.html`
    Context:
        MEDIA_URL
            Path of media files (e.g. "media.example.org")
        STATIC_URL
            Path of static files (e.g. "static.example.org")
    """
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(Context({
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
    })))

def home(request):
    """
    Renders the homepage.
    
    Templates: `home.html`
    Context:
        
    """
    
    set_cookie = False
    if request.method == 'POST':
        sf = SubscriberForm(request.POST)
        if sf.is_valid():
            s, created = Subscriber.objects.get_or_create(
                email=sf.cleaned_data['email'],
                defaults={'subscribed_from':request.META['REMOTE_ADDR'],})
                        
            set_cookie = True
            sf = SubscriberForm()
    else:
        sf = SubscriberForm()
    
    context = {}
    context['blogpost'] = Post.objects.published().latest()
    context['tickettypes'] = TicketType.objects.filter(is_visible=True)
    context['form'] = sf
    context['subscribed'] = set_cookie or subscription_cookie in request.COOKIES
    
    response = render_to_response(
        'home.html',
        context,
        context_instance=RequestContext(request))
    if set_cookie:
        response.set_cookie(subscription_cookie, max_age=31556926)
    return response
