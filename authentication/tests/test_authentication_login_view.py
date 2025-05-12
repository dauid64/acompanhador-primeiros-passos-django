from django.test import TestCase
from django.urls import resolve, reverse

from authentication.forms.cadastro_form import LoginForm
from authentication.views import LoginView
from django.contrib.auth.models import User

from parameterized import parameterized

class LoginViewsTest(TestCase):
    def setUp(self):
        data_user = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@gmail.com",
            "username": "testuser",
            "password": "testpassword",
        }
        self.data_login = {
            "username": data_user['username'],
            "password": data_user['password'],
        }

        self.user = User.objects.create_user(
            username=data_user['username'],
            email=data_user['email'],
            password=data_user['password'],
            first_name=data_user['first_name'],
            last_name=data_user['last_name'],
        )

    def test_login_view_function_is_correct(self):
        view = resolve(reverse('authentication:login'))
        self.assertIs(view.func.view_class, LoginView)
    
    def test_login_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('authentication:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_view_loads_correct_template(self):
        response = self.client.get(reverse('authentication:login'))
        self.assertTemplateUsed(response, 'authentication/pages/login.html')
    
    def test_login_view_context_data(self):
        response = self.client.get(reverse('authentication:login'))
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], LoginForm)
    
    def test_login_view_post_valid_data(self):
        response = self.client.post(reverse('authentication:login'), data=self.data_login)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('authentication:index'))
    
    @parameterized.expand(
        [
            ("username", ""),
            ("password", ""),
        ]
    )
    def test_login_view_post_empty_data(self, field, value):
        invalid_data = self.data_login.copy()
        invalid_data[field] = value
        response = self.client.post(reverse('authentication:login'), data=invalid_data)
        result_form = response.context['form']
        self.assertEqual(response.status_code, 400)
        self.assertFalse(result_form.is_valid())
        self.assertIn(field, result_form.errors)
        self.assertEqual(result_form.errors[field], ['Este campo é obrigatório.'])
    
    @parameterized.expand(
        [
            ("username", "wronguser"),
            ("password", "wrongpassword"),
        ]
    )
    def test_login_view_post_invalid_credentials(self, field, value):
        invalid_data = self.data_login.copy()
        invalid_data[field] = value
        response = self.client.post(reverse('authentication:login'), data=invalid_data)
        result_form = response.context['form']
        self.assertEqual(response.status_code, 400)
        self.assertFalse(result_form.is_valid())
        self.assertIn('__all__', result_form.errors)
        self.assertEqual(result_form.errors['__all__'], ['Nome de usuário ou senha inválida.'])


    
    