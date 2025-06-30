from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, View

from capitulos.models import Capitulo, ExercicioUsuario
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from capitulos.forms.exercicio_usuario_form import ExercicioUsuarioDificuldadeForm, ExercicioUsuarioNotaForm
from django.http import HttpResponse

@method_decorator(login_required, name='dispatch')
class CapituloDetailView(DetailView):
    model = Capitulo
    template_name = 'capitulos/pages/detail_capitulo.html'
    context_object_name = 'capitulo'

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        capitulo = self.object
        exercicios = capitulo.exercicios.all()
        usuario = self.request.user
        exercicios_usuario = []

        exercicios_usuarios_ja_existentes = ExercicioUsuario.objects.filter(
            exercicio__in=exercicios,
            usuario=usuario
        ).select_related('exercicio')
        exercicios_usuario.extend(exercicios_usuarios_ja_existentes)

        ids_exercicios_nao_existentes = set(exercicios.values_list('id', flat=True)) - set(exercicios_usuarios_ja_existentes.values_list('exercicio', flat=True))
        if ids_exercicios_nao_existentes:
            exericios_usuarios_para_criar = []
            for id_exercicio in ids_exercicios_nao_existentes:
                exercicio_usuario_para_criar = ExercicioUsuario(
                    exercicio_id=id_exercicio,
                    usuario=usuario
                )
                exericios_usuarios_para_criar.append(exercicio_usuario_para_criar)
            exercicios_usuarios_criados = ExercicioUsuario.objects.bulk_create(exericios_usuarios_para_criar)
            exercicios_usuarios_criados_ids = [obj.id for obj in exercicios_usuarios_criados]
            exercicios_usuarios_novos = ExercicioUsuario.objects.filter(
                id__in=exercicios_usuarios_criados_ids
            ).select_related('exercicio')
            exercicios_usuario.extend(exercicios_usuarios_novos)
        exercicios_usuario.sort(key=lambda x: x.exercicio.ordem)
        context['exercicios_usuario'] = exercicios_usuario
        return context


@method_decorator(login_required, name='dispatch')
class DificuldadeUpdateView(View):
    def post(self, request, pk, *args, **kwargs):
        exercicio_usuario = get_object_or_404(ExercicioUsuario, id=pk)
        if exercicio_usuario.usuario != request.user:
            return HttpResponse(status=401)
        form = ExercicioUsuarioDificuldadeForm(request.POST, instance=exercicio_usuario)
        if form.is_valid():
            exercicio_usuario = form.save(commit=False)
            exercicio_usuario.usuario = request.user
            exercicio_usuario.save()
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=400)


@method_decorator(login_required, name='dispatch')
class NotaUpdateView(View):
    def post(self, request, pk, *args, **kwargs):
        exercicio_usuario = get_object_or_404(ExercicioUsuario, id=pk)
        if exercicio_usuario.usuario != request.user:
            return HttpResponse(status=401)
        form = ExercicioUsuarioNotaForm(request.POST, instance=exercicio_usuario)
        if form.is_valid():
            exercicio_usuario = form.save(commit=False)
            exercicio_usuario.usuario = request.user
            exercicio_usuario.save()
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=400)

@method_decorator(login_required, name='dispatch')
class FeitoUpdateView(View):
    def post(self, request, pk, *args, **kwargs):
        exercicio_usuario = get_object_or_404(ExercicioUsuario, id=pk)
        if exercicio_usuario.usuario != request.user:
            return HttpResponse(status=401)
        feito = request.POST.get('feito', 'false').lower() == 'true'
        exercicio_usuario.feito = feito
        exercicio_usuario.save()
        return HttpResponse(status=204)


@method_decorator(login_required, name='dispatch')
class ExercicioUsuarioDetailView(DetailView):
    model = ExercicioUsuario
    template_name = 'capitulos/pages/detail_exercicio_usuario.html'
    context_object_name = 'exercicio_usuario'

    def get_queryset(self):
        return super().get_queryset().select_related('exercicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context