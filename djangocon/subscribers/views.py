from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.views.generic.simple import direct_to_template as render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest

from djangocon.subscribers.models import Subscriber
from djangocon.subscribers.forms import SubscriberForm


@require_POST
def subscribe(request):
    form = SubscriberForm(request.POST)
    if form.is_valid():
        subscriber, created = Subscriber.objects.get_or_create(
            email=form.cleaned_data['email'].lower())
        response = HttpResponse()
        if created:
            response.status_code = 201 # created
            response['content-length'] = 0
            if not settings.DEBUG:
                # FIXME: send a thank-you-for-subscribing email
                pass
        return response
    else:
        return HttpResponseBadRequest()

def unsubscribe(request, hash, template_name="subscribers/unsubscribe.html", extra_context=None):
    ctx = extra_context and extra_context.copy() or {}
    try:
        subscriber = Subscriber.objects.get(hash__iexact=hash)
        ctx['subscriber'] = subscriber.email
        subscriber.delete()
    except Subscriber.DoesNotExist:
        ctx['subscriber'] = None
    return render(request, template_name, ctx)

