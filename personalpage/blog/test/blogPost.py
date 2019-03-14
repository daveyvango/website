from django.test import TestCase, Client, SimpleTestCase, TransactionTestCase, LiveServerTestCase
from django.utils import timezone
from django.urls import reverse

from blog.models import BlogPost, Author

from io import BytesIO

class CreateBlogPost(TestCase):

    @classmethod
    def setUpTestData(self):
        """
        Give ourselves an author and blog to test against every time
        """
        self.first_author = Author(
            handle='john',
            first_name='John',
            surname='Doe',
            bio='John Doe is a champ',
            init_date=timezone.now())

        self.first_author.save()

        self.first_blog   = BlogPost(
            author=self.first_author,
            title="New Post",
            meta_tags="blog post, testing",
            banner_img="image.jpg",
            post_date=timezone.now(),
            text="<h1>Html data</h1>")

        self.first_blog.save()
        print ("running setup")
        print (BlogPost.get_recent_blogs())

    def test_blog_creation(self):
        print ("Testing blog creation")
        c   = Client()
        img = BytesIO(b'blog/test/images/RH_logo_white.jpg')
        img.name = 'RH_logo_white.jpg'
        response = c.post(reverse('blog:create'), data={
            'post_title' : 'new blog',
            'banner_img' : img,
            'meta_tags'  : 'new blog, search for me',
            'post_text'  : '<h1>New blog post!</h1><p>It is a great post</p>',
            'author_handle' : 'john'}
            )

        self.assertEqual(response.status_code, 302)
        print ("Done blog creation")

    def test_single_blog_rc(self):
        """
        Make sure individual blog gives proper response
        """
        print ("Testing blog query")
        c = Client()
        response = c.get('/blog/1/')
        self.assertEqual(response.status_code, 200)

class BlogErrors(TestCase):

    def test_blog_not_found(self):
        """
        Make sure individual blog gives proper response
        """
        print ("Testing blog query")
        c = Client()
        with self.assertRaises(BlogPost.DoesNotExist):
            response = c.get('/blog/999/')
