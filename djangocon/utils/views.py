from django import http
from django.conf import settings
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response

from djangocon.subscribers.models import Tagline
from djangocon.blog.models import Post

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
    
    context = {}
    context['taglines'] = Tagline.objects.order_by('?')[:50]
    context['blogpost'] = Post.objects.latest()
    
    return render_to_response(
        'home.html',
        context,
        context_instance=RequestContext(request))
    