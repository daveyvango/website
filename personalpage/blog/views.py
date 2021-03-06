from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import BlogPost, Author
from .forms import UploadFileForm, FileHandler

def index(request):
    recent_blogs = BlogPost.get_recent_blogs()
    return render(request, 'blog/index.html', {'recent_blogs': recent_blogs})

def detail(request, blog_id):
    blog_post = BlogPost.objects.get(pk=blog_id)
    return render(request, 'blog/detail.html', {'blog_post': blog_post})

def detail_json(request, blog_id):
    blog_post = BlogPost.objects.get(pk=blog_id)
    blog_post_data = {
        'author':    blog_post.author.handle,
        'title':     blog_post.title,
        'text':      blog_post.text,
        'post_date': blog_post.post_date
    }
    return JsonResponse(blog_post_data);


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
        meta_tags  = request.POST['meta_tags']
        handle     = request.POST['author_handle']
        post_title = request.POST['post_title']
        post_text  = request.POST['post_text']
        file_form  = UploadFileForm(request.POST, request.FILES)
        file_handler = FileHandler()
        file_handler.write_file(request.FILES['banner_img'])
        banner_img = request.FILES['banner_img']

        author = Author.objects.filter(handle=handle)[0]
        blog_post = BlogPost(text=post_text, author=author, title=post_title, post_date=timezone.now(), banner_img=banner_img)
        blog_post.save()
    # MultiValueDictError, PermissionError
    except Exception as e:
        # Redisplay the question voting form.
        return HttpResponse('%s (%s)' % (e.message, type(e)))
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('blog:detail', args=[blog_post.id]))

def update(request):
    try:
        blog_post           = BlogPost.objects.get(pk=request.POST['blog_id'])
        handle              = request.POST['author_handle']
        blog_post.meta_tags = request.POST['meta_tags']
        blog_post.title     = request.POST['post_title']
        blog_post.text      = request.POST['post_text']

        file_form    = UploadFileForm(request.POST, request.FILES)
        file_handler = FileHandler()
        file_handler.write_file(request.FILES['banner_img'])
        blog_post.banner_img = request.FILES['banner_img']

        blog_post.author = Author.objects.filter(handle=handle)[0]
        blog_post.save()
    except Exception as e:
        # Redisplay the question voting form.
        return HttpResponse('%s (%s)' % (e.message, type(e)))
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('blog:detail', args=[blog_post.id]))

def delete(request):
    try:
        blog_post            = BlogPost.objects.get(pk=request.POST['blog_id'])
        blog_post.delete()
    except Exception as e:
        # Redisplay the question voting form.
        return HttpResponse('%s (%s)' % (e.message, type(e)))
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('blog:index'))

def create_author(request):
    try:
        handle     = request.POST['author_handle']
        first_name = request.POST['first_name']
        surname    = request.POST['surname']
        bio        = request.POST['bio']

        author = Author(handle=handle, first_name=first_name, surname=surname, init_date=timezone.now(), bio=bio)
        author.save()
    except:
        # Redisplay the question voting form.
        return HttpResponse("something broke.")
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('blog:author_detail', args=[author.id]))
