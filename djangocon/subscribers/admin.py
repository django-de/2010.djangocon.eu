from django.contrib import admin

from djangocon.subscribers.models import *

admin.site.register(Subscriber, admin.ModelAdmin)
admin.site.register(Tagline, admin.ModelAdmin)