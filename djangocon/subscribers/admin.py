from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from django.shortcuts import get_object_or_404, render_to_response
from djangocon.subscribers.models import *
from datetime import datetime

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribe_date',)
    list_filter = ('subscribe_date',)

    def get_urls(self):
        urls = super(SubscriberAdmin, self).get_urls()
        info = self.admin_site.name, self.model._meta.app_label, self.model._meta.module_name,
        new_urls = patterns("",
            url("^export/$", self.admin_site.admin_view(self.export_view), name='%sadmin_%s_%s_export' % info),
        )
        return new_urls + urls

    def export_view(self, request, extra_context=None):
        response = render_to_response(
            'admin/subscribers/subscriber/export.csv',
            {'subscribers': self.model.objects.all()},
            mimetype='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="subscribers_%s.csv"' % datetime.now().strftime('%Y-%m-%d')
        return response

admin.site.register(Subscriber, SubscriberAdmin)

admin.site.register(Tagline, admin.ModelAdmin)