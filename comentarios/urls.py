from django.urls import path

from comentarios.views import ComentariosCreateView

app_name = 'comentarios'

urlpatterns = [
    path("create", ComentariosCreateView.as_view(), name="create"),
]
