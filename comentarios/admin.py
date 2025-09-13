from django.contrib import admin

from comentarios.models import Comentario

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'exercicio', 'created_at', 'active')
    search_fields = ('usuario__username', 'exercicio__nome', 'body')
    ordering = ('created_at',)
