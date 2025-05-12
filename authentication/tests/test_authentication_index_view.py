from django.test import TestCase
from django.urls import resolve, reverse

from authentication.views import IndexView

class IndexViewsTest(TestCase):
    def test_index_view_function_is_correct(self):
        view = resolve(reverse('authentication:index'))
        self.assertIs(view.func.view_class, IndexView)
    
    def test_index_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('authentication:index'))
        self.assertEqual(response.status_code, 200)
    
    def test_index_view_loads_correct_template(self):
        response = self.client.get(reverse('authentication:index'))
        self.assertTemplateUsed(response, 'authentication/pages/index.html')