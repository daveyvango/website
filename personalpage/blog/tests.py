from django.test import TestCase

from blog.models import Author, BlogPost

class BlogTestCase(TestCase):
    def test_index_rc(self):
        """
        Make sure index gives 200
        """
        response = self.client.git(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)

class SessionTestCase(TestCase):
    def test_session_creation(self):
        pass
