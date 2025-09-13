from django.db import models
from django.forms import ValidationError

from capitulos.models import Exercicio
from django.contrib.auth.models import User

# Create your models here.
class Comentario(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, related_name="comentarios", on_delete=models.CASCADE)
    exercicio = models.ForeignKey(Exercicio, related_name="comentarios", on_delete=models.CASCADE)
    body = models.TextField()
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='respostas', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
    
    def __str__(self):
        return 'Comment by {}'.format(self.usuario.username)
    
    def clean(self):
        errors = {}

        if self.parent:
            if self.parent.exercicio != self.exercicio:
                errors['parent'] = 'A resposta deve estar associada ao mesmo exercício do comentário pai.'

        if errors:
            raise ValidationError(errors)
