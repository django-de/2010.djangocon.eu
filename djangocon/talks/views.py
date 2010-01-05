# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from djangocon.talks.forms import TalkForm
from djangocon.talks.models import Talk

def submit(request):
    context = {}
    if request.method == 'POST':
        form = TalkForm(request.POST)
        if form.is_valid():
            form.save()
            context['message'] = 'Thanks for your proposal! We will review it and let you know … Wanna propose another one?'
            speaker_data = {
                'speaker_name': form.cleaned_data.get('speaker_name', ''),
                'speaker_twitter': form.cleaned_data.get('speaker_twitter', ''),
                'speaker_website': form.cleaned_data.get('speaker_website', ''),
                'speaker_email': form.cleaned_data.get('speaker_email', ''),
            }
            form = TalkForm()
            form.initial.update(speaker_data)
    else:
        form = TalkForm()
    context['form'] = form
    return render_to_response('talks/submit.html', context, context_instance=RequestContext(request))