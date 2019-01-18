from django.db import models
from django.utils import timezone

class Author(models.Model):
    # Author's Screen Name
    handle     = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20)
    surname    = models.CharField(max_length=20)
    init_date  = models.DateTimeField('Account Established Date')

class BlogPost(models.Model):
    # Author's Screen Name
    author    = models.ForeignKey(Author, on_delete=models.CASCADE)
    # Post details
    title     = models.CharField(max_length=50, unique=True)
    text      = models.CharField(max_length=1000)
    post_date = models.DateTimeField('Date Posted')

    def get_recent_blogs():
        recent_blogs = BlogPost.objects.order_by('post_date')[:10]
        return recent_blogs
