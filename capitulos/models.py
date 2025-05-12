from django.db import models


class Capitulo(models.Model):
    titulo = models.CharField(max_length=200)
    numero = models.IntegerField()
    link = models.URLField(max_length=200)
    percentual_completo = models.FloatField(default=0)

    def __str__(self):
        return self.titulo
    
class Exercicio(models.Model):
    class Dificuldade(models.TextChoices):
        MUITO_FACIL = 'Muito Fácil'
        FACIL = 'Fácil'
        MEDIO = 'Médio'
        DIFICIL = 'Difícil'
        MUITO_DIFICIL = 'Muito Difícil'

    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE)
    enunciado = models.TextField()
    dificuldade = models.CharField(choices=Dificuldade.choices, max_length=20)
    nota = models.IntegerField()
    feito = models.BooleanField(default=False)

    def __str__(self):
        return f"Exercício {self.id} - {self.capitulo.titulo}"