from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
#from django.template.context import RequestContext


from django.template import RequestContext, loader

from subscribers.models import *
from subscribers.forms import SubscriberForm


def home(request):
    """
    Render the homepage.
    """
    edc_subscribed = 'edc_subscribed' in request.COOKIES
    
    print edc_subscribed
    
    taglines = Tagline.objects.order_by('?')[:50]
    
    return render_to_response(
        'base.html',
        {
            'edc_subscribed': edc_subscribed,
            'taglines': taglines,
        },
        context_instance=RequestContext(request))


def subscribe(request):
    """
    Add a subscription. Meant to be called via AJAX.
    """
    if not request.method == 'POST':
        return HttpResponseBadRequest()
    
    sf = SubscriberForm(request.POST)
    if sf.is_valid():
        
        s, created = Subscriber.objects.get_or_create(
            email=sf.email,
            defaults={'subscribed_from':request.META['REMOTE_ADDR'],})
        
        if sf.tagline:
            t = Tagline(tagline=sf.tagline, subscriber=s)
            t.save()
        
        response = HttpResponse()
        response.set_cookie('edc_subscribed', max_age=31556926)
        return response
    else:
        return HttpResponseBadRequest()