from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField

class Author(models.Model):
    # Author's Screen Name
    handle     = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20)
    surname    = models.CharField(max_length=20)
    bio        = models.CharField(max_length=1000, default="Bio coming soon.")
    init_date  = models.DateTimeField('Account Established Date')

class BlogPost(models.Model):
    # Author's Screen Name
    author     = models.ForeignKey(Author, on_delete=models.CASCADE)
    # Post details
    title      = models.CharField(max_length=100, unique=True)
    meta_tags  = models.CharField(max_length=200, unique=False, default="")
    # Just the image name
    banner_img = models.CharField(max_length=100, unique=False, default="")
    post_date  = models.DateTimeField('Date Posted')
    text       = HTMLField()

    def get_recent_blogs():
        recent_blogs = BlogPost.objects.order_by('-post_date')[:10]
        return recent_blogs
