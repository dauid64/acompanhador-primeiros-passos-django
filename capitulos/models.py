from random import randrange
from django.db import models
from django.contrib.auth.models import User
from prose.fields import RichTextField

class Capitulo(models.Model):
    titulo = models.CharField(max_length=200)
    numero = models.IntegerField()

    def __str__(self):
        return str(self.numero) + " - " + self.titulo
    
class Exercicio(models.Model):
    ordem = models.IntegerField(default=randrange(1000, 9999))
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE, related_name='exercicios')
    nome = models.CharField(max_length=200)
    enunciado = RichTextField()
    link = models.URLField(max_length=200)

    class Meta:
        ordering = ['ordem']
        constraints = [
            models.UniqueConstraint(fields=['capitulo', 'ordem'], name='unique_capitulo_ordem')
        ]

    def __str__(self):
        return f"Exercício {self.id} - {self.capitulo.titulo}"

class ExercicioUsuario(models.Model):
    class Rating(models.IntegerChoices):
        MUITO_RUIM = "0"
        RUIM = "1"
        MAIS_OU_MENOS = "2"
        BOM = "3"
        MUITO_BOM = "4"

    class RatingDificulty(models.IntegerChoices):
        MUITO_FACIL = "0"
        FACIL = "1"
        MEDIO = "2"
        DIFICIL = "3"
        MUITO_DIFICIL = "4"

    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE, related_name='exercicios_usuario')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercicios_usuario')
    dificuldade = models.IntegerField(choices=Rating.choices, null=True, blank=True, default=RatingDificulty.MUITO_FACIL)
    nota = models.IntegerField(null=True, blank=True, choices=Rating.choices, default=Rating.MUITO_BOM)
    feito = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['exercicio', 'usuario'], name='unique_exercicio_usuario')
        ]

    def __str__(self):
        return f"Exercício {self.exercicio.id} - {self.usuario.username}"