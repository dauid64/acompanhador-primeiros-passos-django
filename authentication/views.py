from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render

from authentication.forms.cadastro_form import CadastroForm

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
            }
        )

class LoginView(TemplateView):
    template_name = 'authentication/pages/login.html'

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {}
        )