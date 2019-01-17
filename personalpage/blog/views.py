from django.shortcuts import render
from django.http import HttpResponse

from .models import BlogPost, Author

def index(request):
    recent_blogs = BlogPost.get_recent_blogs()
    return render(request, 'blog/index.html', {'recent_blogs': recent_blogs})

def detail(request, blog_id):
    blog_post = BlogPost.objects.get(pk=blog_id)
    return render(request, 'blog/detail.html', {'blog_post': blog_post})

def author_detail(request, author_id):
    author = Author.objects.get(pk=author_id)
    return render(request, 'blog/author_detail.html', {'author': author })

def create(request, blog_id):
    blog_post = BlogPost.objects.get(pk=blog_id)
    return render(request, 'blog/detail.html', {'blog_post': blog_post})

