from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from authentication.forms.cadastro_form import CadastroForm, LoginForm
from capitulos.models import Capitulo, Exercicio, ExercicioUsuario
from django.db.models import Count, Q

class IndexView(TemplateView):
    template_name = 'authentication/pages/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('authentication:home')
        return render(request, self.template_name)

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

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'authentication/pages/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        usuario = self.request.user
        capitulos = Capitulo.objects.annotate(
            total_exercicios=Count('exercicios', distinct=True),
            exercicios_feitos=Count(
                'exercicios__exercicios_usuario',
                filter=Q(exercicios__exercicios_usuario__usuario=usuario, exercicios__exercicios_usuario__feito=True),
                distinct=True
            )
        )

        for capitulo in capitulos:
            if capitulo.total_exercicios > 0:
                capitulo.percentual_exercicios_completos = (capitulo.exercicios_feitos / capitulo.total_exercicios) * 100
            else:
                capitulo.percentual_exercicios_completos = 0

        total_exercicios_feitos = ExercicioUsuario.objects.filter(usuario=usuario, feito=True).count()
        total_exercicios = Exercicio.objects.count()
        percentual_total_exercicios_completos = total_exercicios_feitos / total_exercicios * 100 if total_exercicios > 0 else 0

        ctx['percentual_total_exercicios_completos'] = round(percentual_total_exercicios_completos, 2)
        ctx['capitulos'] = capitulos
        return ctx