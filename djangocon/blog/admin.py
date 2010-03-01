from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from blog.models import *

class PostResourceInline(admin.StackedInline):
    model = PostResource
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'draft', 'title', 'published',)
    list_filter = ('author', 'draft',)
    list_display_links = ('title',)
    date_hierarchy = 'published'
    fieldsets = (
        (_('Title'), {
            'fields': ('title', 'slug'),
        }),
        (_('Metadata'), {
            'fields': ('published', 'draft', 'author', 'updated_at', ),
        }),
        (_('Content'), {
            'fields': ('tease', 'body'),
        }),
    )
    readonly_fields = ('updated_at', 'author')
    prepopulated_fields = {'slug': ('title',)}
    save_as = True
    save_on_top = True
    inlines = (PostResourceInline,)
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.updated_by = request.user 
        obj.save()
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for i in instances:
            if not change:
                i.author = request.user
            i.updated_by = request.user
            i.save()
        formset.save_m2m()        
    
admin.site.register(Post, PostAdmin)