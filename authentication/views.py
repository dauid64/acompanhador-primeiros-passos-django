from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from authentication.forms.cadastro_form import CadastroForm, LoginForm

class IndexView(TemplateView):
    template_name = 'authentication/pages/index.html'

class CadastroView(View):
    template_name = 'authentication/pages/cadastro.html'

    def get(self, request, *args, **kwargs):
        form = CadastroForm()
        return render(
            request,
            self.template_name,
            {
                'form': form
            }
        )

    def post(self, request, *args, **kwargs):
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authentication:login')
        return render(
            request,
            self.template_name,
            {
                'form': form
            },
            status=400
        )

class LoginView(TemplateView):
    template_name = 'authentication/pages/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(
            request,
            self.template_name,
            {
                'form': form
            }
        )
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('authentication:home')
            else:
                form.add_error(None, "Nome de usuário ou senha inválida.")
        return render(
            request,
            self.template_name,
            {
                'form': form
            },
            status=400
        )

@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('authentication:index')

@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'authentication/pages/home.html'