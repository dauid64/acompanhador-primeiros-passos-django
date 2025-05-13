from django.contrib import admin
from .models import Capitulo, Exercicio, ExercicioUsuario


@admin.register(Capitulo)
class CapituloAdmin(admin.ModelAdmin):
    list_display = ('numero', 'titulo', 'link')
    search_fields = ('titulo',)
    ordering = ('numero',)


@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'capitulo', 'enunciado_curto')
    search_fields = ('enunciado', 'capitulo__titulo')
    list_filter = ('capitulo',)

    def enunciado_curto(self, obj):
        return (obj.enunciado[:75] + '...') if len(obj.enunciado) > 75 else obj.enunciado
    enunciado_curto.short_description = 'Enunciado'


@admin.register(ExercicioUsuario)
class ExercicioUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'exercicio', 'dificuldade', 'nota', 'feito')
    list_filter = ('feito', 'dificuldade', 'usuario')
    search_fields = ('usuario__username', 'exercicio__enunciado')
    list_editable = ('feito', 'nota', 'dificuldade')
