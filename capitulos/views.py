from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, View

from capitulos.models import Capitulo, ExercicioUsuario
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from capitulos.forms.exercicio_usuario_form import ExercicioUsuarioNotaForm
from django.http import HttpResponse

@method_decorator(login_required, name='dispatch')
class CapituloDetailView(DetailView):
    model = Capitulo
    template_name = 'capitulos/pages/detail_capitulo.html'
    context_object_name = 'capitulo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        capitulo = self.object
        exercicios = capitulo.exercicios.all()
        usuario = self.request.user
        exercicios_usuario = []

        for exercicio in exercicios:
            exercicio_usuario, created = ExercicioUsuario.objects.get_or_create(
                exercicio=exercicio,
                usuario=usuario
            )
            exercicios_usuario.append(exercicio_usuario)

        context['exercicios_usuario'] = exercicios_usuario
        return context


@method_decorator(login_required, name='dispatch')
class DificuldadeUpdateView(View):
    def post(self, request, pk, *args, **kwargs):
        exercicio_usuario = get_object_or_404(ExercicioUsuario, id=pk)
        form = ExercicioUsuarioNotaForm(request.POST, instance=exercicio_usuario)
        if form.is_valid():
            exercicio_usuario = form.save(commit=False)
            exercicio_usuario.usuario = request.user
            exercicio_usuario.save()
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=400)