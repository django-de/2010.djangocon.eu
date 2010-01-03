from django.contrib import admin
from djangocon.talks.models import Talk

class TalkAdmin(admin.ModelAdmin):
    list_display = ('title', 'speakers_list', 'accepted', 'scheduled',)
    list_filter = ('accepted', 'scheduled',)
    search_fields = ('title', 'abstract',)

admin.site.register(Talk, TalkAdmin)