from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

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

@login_required
def new(request):
    if request.user.is_authenticated:
        return render(request, 'blog/new.html', {'author': request.user.get_username })
    else:
        return render(request, 'blog/login_redirect.html')

def new_author(request):
    if request.user.is_authenticated:
        return render(request, 'blog/new_author.html')
    else:
        return render(request, 'blog/login_redirect.html')

def create(request):
    try:
        handle     = request.POST['author_handle']
        post_title = request.POST['post_title']
        post_text  = request.POST['post_text']

        author = Author.objects.filter(handle=handle)[0]
        blog_post = BlogPost(text=post_text, author=author, title=post_title, post_date=timezone.now())
        blog_post.save()
    except:
        # Redisplay the question voting form.
        return HttpResponse("something broke.")
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('blog:detail', args=(blog_post.id,)))

def create_author(request):
    try:
        handle     = request.POST['author_handle']
        first_name = request.POST['first_name']
        surname    = request.POST['surname']

        author = Author(handle=handle, first_name=first_name, surname=surname, init_date=timezone.now())
        author.save()
    except:
        # Redisplay the question voting form.
        return HttpResponse("something broke.")
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('blog:author_detail', args=(author.id,)))
