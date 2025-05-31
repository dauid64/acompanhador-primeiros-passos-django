from django.urls import path

from capitulos.views import CapituloDetailView, DificuldadeUpdateView, NotaUpdateView, ExercicioUsuarioDetailView

app_name = "capitulos"

urlpatterns = [
    path("<int:pk>/", CapituloDetailView.as_view(), name="capitulo_detail"),
    path("<int:pk>/dificuldade/", DificuldadeUpdateView.as_view(), name="dificuldade_update"),
    path("<int:pk>/nota/", NotaUpdateView.as_view(), name="nota_update"),
    path("exercicio/<int:pk>/", ExercicioUsuarioDetailView.as_view(), name="exercicio_usuario_detail"),
]
