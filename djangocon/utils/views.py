from django import http
from django.conf import settings
from django.template import Context, loader

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
