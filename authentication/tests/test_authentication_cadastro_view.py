from django.test import TestCase
from django.urls import resolve, reverse

from authentication.forms.cadastro_form import CadastroForm
from authentication.views import CadastroView
from parameterized import parameterized
from django.contrib.auth.models import User

class CadastroViewsTest(TestCase):
    def setUp(self):
        self.data_cadastro = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "testpassword",
        }

    def test_cadastro_view_function_is_correct(self):
        view = resolve(reverse('authentication:cadastro'))
        self.assertIs(view.func.view_class, CadastroView)
    
    def test_cadastro_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('authentication:cadastro'))
        self.assertEqual(response.status_code, 200)
    
    def test_cadastro_view_loads_correct_template(self):
        response = self.client.get(reverse('authentication:cadastro'))
        self.assertTemplateUsed(response, 'authentication/pages/cadastro.html')
    
    def test_cadastro_view_context_data(self):
        response = self.client.get(reverse('authentication:cadastro'))
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], CadastroForm)
    
    def test_cadastro_view_post_valid_data(self):
        response = self.client.post(reverse('authentication:cadastro'), data=self.data_cadastro)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('authentication:login'))

    @parameterized.expand(
        [
            ("first_name", ""),
            ("last_name", ""),
            ("username", ""),
            ("email", ""),
            ("password", ""),
        ]
    )
    def test_cadastro_view_post_empty_data(self, field, value):
        invalid_data = self.data_cadastro.copy()
        invalid_data[field] = value
        response = self.client.post(reverse('authentication:cadastro'), data=invalid_data)
        result_form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertFalse(result_form.is_valid())
        self.assertIn(field, result_form.errors)
        self.assertEqual(result_form.errors[field], ['Este campo é obrigatório.'])

    @parameterized.expand(
            [
                ("username", "Usuário já cadastrado."),
                ("email", "Email já cadastrado.")
            ]
    )
    def test_cadastro_view_post_with_existing_data(self, field, error_message):
        new_user = {
            "first_name": "new_test",
            "last_name": "new_test",
            "username": "new_test_user",
            "email": "newtest@gmail.com",
            "password": "newtestpassword",
        }
        new_user[field] = "existing_value@gmail.com"
        User.objects.create(**new_user)

        invalid_data = self.data_cadastro.copy()
        invalid_data[field] = "existing_value@gmail.com"

        response = self.client.post(reverse('authentication:cadastro'), data=invalid_data)
        result_form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertFalse(result_form.is_valid())
        self.assertIn(field, result_form.errors)
        self.assertEqual(result_form.errors[field], [error_message])