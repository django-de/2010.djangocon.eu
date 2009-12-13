from django.contrib import admin
from schedule.models import Track, Day, Slot

class TrackAdmin(admin.ModelAdmin):
    pass

admin.site.register(Track, TrackAdmin)

class DayAdmin(admin.ModelAdmin):
    list_display = ('date', 'track',)
    list_filter = ('track',)

admin.site.register(Day, DayAdmin)

class SlotAdmin(admin.ModelAdmin):
    list_display = ('talk', 'day', 'starttime', 'endtime',)
    list_filter = ('day',)

admin.site.register(Slot, SlotAdmin)