from django.test import TestCase
from django.urls import reverse

class AuthenticationURLsTest(TestCase):
    def test_index_url_is_correct(self):
        url = reverse('authentication:index')
        self.assertEqual(url, '/')
    
    def test_cadastro_url_is_correct(self):
        url = reverse('authentication:cadastro')
        self.assertEqual(url, '/cadastro/')

    def test_login_url_is_correct(self):
        url = reverse('authentication:login')
        self.assertEqual(url, '/login/')