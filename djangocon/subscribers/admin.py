from django.contrib import admin

from subscribers.models import *

admin.site.register(Subscriber, admin.ModelAdmin)
admin.site.register(Tagline, admin.ModelAdmin)