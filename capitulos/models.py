from django.db import models
from django.contrib.auth.models import User
from prose.fields import RichTextField

class Capitulo(models.Model):
    titulo = models.CharField(max_length=200)
    numero = models.IntegerField()

    def __str__(self):
        return self.titulo
    
class Exercicio(models.Model):
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE, related_name='exercicios')
    nome = models.CharField(max_length=200)
    enunciado = RichTextField()
    link = models.URLField(max_length=200)

    def __str__(self):
        return f"Exercício {self.id} - {self.capitulo.titulo}"

class ExercicioUsuario(models.Model):
    class Rating(models.IntegerChoices):
        MUITO_RUIM = "0"
        RUIM = "1"
        MAIS_OU_MENOS = "2"
        BOM = "3"
        MUITO_BOM = "4"

    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE, related_name='exercicios_usuario')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercicios_usuario')
    dificuldade = models.IntegerField(choices=Rating.choices, null=True, blank=True)
    nota = models.IntegerField(null=True, blank=True, choices=Rating.choices)
    feito = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['exercicio', 'usuario'], name='unique_exercicio_usuario')
        ]

    def __str__(self):
        return f"Exercício {self.exercicio.id} - {self.usuario.username}"