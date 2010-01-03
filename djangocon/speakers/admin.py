from django.contrib import admin
from djangocon.speakers.models import Speaker

class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website', 'twitter',)
    search_fields = ('name',)

admin.site.register(Speaker, SpeakerAdmin)