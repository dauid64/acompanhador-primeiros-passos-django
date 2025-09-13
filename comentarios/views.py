from django.http import JsonResponse
from django.views.generic import CreateView
from comentarios.forms import ComentarioForm
from comentarios.models import Comentario
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class ComentariosCreateView(CreateView):
    model = Comentario
    form_class = ComentarioForm

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        mensagem_criada = form.save()
        return JsonResponse({
            "id": mensagem_criada.id,
            "nome_usuario": mensagem_criada.usuario.username,
            "body": mensagem_criada.body,
            "created_at": mensagem_criada.created_at.strftime("%d/%m/%Y %H:%M:%S"),
            "parent_id": mensagem_criada.parent_id,
            "is_reply": bool(mensagem_criada.parent_id)
        })
    