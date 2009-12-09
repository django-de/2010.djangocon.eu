from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
#from django.template.context import RequestContext


from django.template import RequestContext, loader

from subscribers.models import *
from subscribers.forms import SubscriberForm

cookie = 'edc_subscribed'


def home(request):
    """
    Render the homepage.
    """
    context = {}
    context['edc_subscribed'] = cookie in request.COOKIES    
    context['taglines'] = Tagline.objects.order_by('?')[:50]
    context['form'] = SubscriberForm()
    
    return render_to_response(
        'base.html', context,
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
            email=sf.cleaned_data['email'],
            defaults={'subscribed_from':request.META['REMOTE_ADDR'],})
        
        if sf.cleaned_data['tagline']:
            t = Tagline(tagline=sf.cleaned_data['tagline'], subscriber=s)
            t.save()
        
        response = HttpResponseRedirect(reverse('home'))
        response.set_cookie(cookie, max_age=31556926)
        return response
    else:
        return HttpResponseBadRequest()

def clear(request):
    """
    Clears the subscription cookie.
    """
    response = HttpResponseRedirect(reverse('home'))
    response.delete_cookie(cookie)
    return response