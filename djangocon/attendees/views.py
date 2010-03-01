from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect
from djangocon.attendees.models import Attendee, TICKET_FEES
from djangocon.attendees.forms import RegisterForm
from django.conf import settings

#from django.views.decorators.csrf import csrf_exempt

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            attendee = form.save()
            return HttpResponseRedirect(reverse('attendees_paypal_redirect', kwargs={'id': attendee.pk}))
    else:
        form = RegisterForm()

    return render_to_response('attendees/register.html', {'form': form}, RequestContext(request))

def paypal_redirect(request, id):
    attendee = get_object_or_404(Attendee, pk=id, state='new')
    total_sum = TICKET_FEES.get(attendee.ticket_type, 0)

    # debug stuff for testing
    if settings.DEBUG and attendee.ticket_type == 'regular':
        total_sum = 1

    attendee.payment_total = total_sum
    attendee.save()

    return HttpResponseRedirect("https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=%(to)s&item_name=%(item)s&amount=%(amount).2f&currency_code=EUR&notify_url=%(ipn)s&return=%(return)s&cancel_return=%(cancel_return)s&no_note=1&no_shipping=1&business_url=http://www.djangocon.eu&business_cs_email=kontakt@djangocon.eu&custom=%(custom)s&item_number=%(itemno)s" % {
        'to': settings.PAYPAL_TO,
        'item': settings.PAYPAL_ITEM,
        'itemno': '1',
        'amount': float(total_sum),
        'custom': u"%s|%s" % (attendee.pk, attendee.email),
        'ipn': '%s/attendees/payment/callback/' % settings.PAYPAL_CALLBACK_HOST,
        'return': '%s/attendees/payment/done/' % settings.PAYPAL_CALLBACK_HOST,
        'cancel_return': '%s/attendees/payment/cancel/' % settings.PAYPAL_CALLBACK_HOST
    })

#@csrf_exempt
def paypal_callback(request):
    custom = request.REQUEST.get('custom')
    payment_status = request.REQUEST.get('payment_status')

    attendee_id, attendee_email = custom.split("|")

    try:
        attendee = Attendee.objects.get(pk=attendee_id)
    except Attendee.DoesNotExist:
        return HttpResponse('invalid')

    if not payment_status == 'Completed':
        attendee.state = 'payment_pending'
        attendee.save()
        return HttpResponse('waiting')

    try:
        pp = {}
        for item in request.REQUEST.items():
            pp[item[0]] = item[1]
        attendee.payment_data = json.dumps(pp)
    except:
        pass
    attendee.state = 'payment_received'
    attendee.save()
    return HttpResponse('ok')
