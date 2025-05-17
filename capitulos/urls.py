from django.urls import path

from capitulos.views import CapituloDetailView, DificuldadeUpdateView

app_name = "capitulos"

urlpatterns = [
    path("<int:pk>/", CapituloDetailView.as_view(), name="capitulo_detail"),
    path("<int:pk>/dificuldade/", DificuldadeUpdateView.as_view(), name="dificuldade_update")
]
