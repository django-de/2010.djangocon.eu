from django.views.decorators.cache import cache_page
from django.views.generic.simple import direct_to_template as render
from djangocon.subscribers.forms import SubscriberForm

@cache_page(60*60) # Cache for 1hr.
def placeholder(
        request,
        template_name="core/placeholder.html",
        extra_context=None):
    ctx = extra_context and extra_context.copy() or {}
    ctx['form'] = SubscriberForm()
    return render(request, template_name, ctx)

@cache_page(60*60) # Cache for 1hr
def cached_direct(request, template_name, extra_context=None):
    ctx = extra_context and extra_context.copy() or {}
    return render(request, template_name, ctx)


