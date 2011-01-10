from django.contrib import admin

from djangocon.blog.models import Post

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('author', 'draft', 'title', 'publish_date',)
    list_filter = ('author', 'draft',)
    list_display_links = ('title',)
    date_hierarchy = 'publish_date'
    fieldsets = (
        ('Metadata', {
            'fields': ('title', 'slug', 'draft', 'publish_date')
        }),
        ('Authorship', {
            'classes': ('collapse',),
            'fields': ('author', 'modified_date', 'created_date',),
        }),
        ('Body', {
            'fields': ('body_markdown',),
        }),
    )
    readonly_fields = ('modified_date', 'created_date',)
    prepopulated_fields = {'slug': ('title',)}
    
    def formfield_for_foreignkey(self, dbfield, request, **kwargs):
        ff = super(BlogPostAdmin, self).formfield_for_foreignkey(dbfield, request, **kwargs)
        if dbfield.name == 'author':
            ff.initial = request.user
        return ff

admin.site.register(Post, BlogPostAdmin)
        

