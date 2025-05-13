from django.db import models
from django.contrib.auth.models import User

class Capitulo(models.Model):
    titulo = models.CharField(max_length=200)
    numero = models.IntegerField()
    link = models.URLField(max_length=200)

    def __str__(self):
        return self.titulo
    
class Exercicio(models.Model):
    class Dificuldade(models.TextChoices):
        MUITO_FACIL = 'Muito Fácil'
        FACIL = 'Fácil'
        MEDIO = 'Médio'
        DIFICIL = 'Difícil'
        MUITO_DIFICIL = 'Muito Difícil'

    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE, related_name='exercicios')
    enunciado = models.TextField()

    def __str__(self):
        return f"Exercício {self.id} - {self.capitulo.titulo}"

class ExercicioUsuario(models.Model):
    class Dificuldade(models.TextChoices):
        MUITO_FACIL = 'Muito Fácil'
        FACIL = 'Fácil'
        MEDIO = 'Médio'
        DIFICIL = 'Difícil'
        MUITO_DIFICIL = 'Muito Difícil'

    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE, related_name='exercicios_usuario')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercicios_usuario')
    dificuldade = models.CharField(choices=Dificuldade.choices, max_length=20, null=True, blank=True)
    nota = models.IntegerField(null=True, blank=True)
    feito = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['exercicio', 'usuario'], name='unique_exercicio_usuario')
        ]

    def __str__(self):
        return f"Exercício {self.exercicio.id} - {self.usuario.username}"