from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.template import RequestContext, loader

from djangocon.subscribers.models import *
from djangocon.subscribers.forms import SubscriberForm

cookie = 'edc_subscribed'

def home(request):
    """
    Render the homepage.
    """
    
    set_cookie = False
    if request.method == 'POST':
        sf = SubscriberForm(request.POST)
        if sf.is_valid():
            s, created = Subscriber.objects.get_or_create(
                email=sf.cleaned_data['email'],
                defaults={'subscribed_from':request.META['REMOTE_ADDR'],})
            
            if sf.cleaned_data['tagline']:
                t = Tagline(tagline=sf.cleaned_data['tagline'], subscriber=s)
                t.save()
            
            set_cookie = True
            sf = SubscriberForm()
    else:
        sf = SubscriberForm()
    
    context = {}
    context['edc_subscribed'] = set_cookie or cookie in request.COOKIES
    context['taglines'] = Tagline.objects.order_by('?')[:50]
    context['form'] = sf
    
    response = render_to_response(
        'startpage.html', context,
        context_instance=RequestContext(request))
    if set_cookie:
        response.set_cookie(cookie, max_age=31556926)
    return response

def clear(request):
    """
    Clears the subscription cookie.
    """
    response = HttpResponseRedirect(reverse('home'))
    response.delete_cookie(cookie)
    return response