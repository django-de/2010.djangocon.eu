from django.shortcuts import render_to_response
from django.views.generic import date_based, list_detail
from django.template.context import RequestContext
from django.http import Http404

from taggit.models import Tag

from djangocon.blog.models import Post


def extra_context():
    return {
        'blog_tags': Post.tags.all(),
        'blog_months': Post.objects.published().dates('published', 'month', order='DESC'),
    }
    
def blog_index(request):
    return date_based.archive_index(
        request,
        queryset=Post.objects.published(),
        date_field='published',
        allow_empty=False,
        num_latest=40,
        template_object_name='post_list',
        extra_context=extra_context())        
    
def blog_archive_month(request, year, month):
    return date_based.archive_month(
        request,
        queryset=Post.objects.published(),
        date_field='published',
        allow_empty=False,
        year=year,
        month=month,
        template_object_name='post',
        extra_context=extra_context())
    
def blog_archive_tag(request, slug):
    try:
        tag = Post.tags.get(slug=slug)
    except Tag.DoesNotExist:
        return Http404()
    context = extra_context()
    context['tag'] = tag    
    return render_to_response('blog/post_archive_tag.html',
        context, context_instance=RequestContext(request)) 

def blog_detail(request, year, month, day, slug):
    return date_based.object_detail(
        request,
        queryset=Post.objects.published(),
        date_field='published',
        year=year,
        month=month,
        day=day,
        slug=slug,
        template_object_name='post',
        extra_context=extra_context())
