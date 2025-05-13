

from authentication import views
from django.urls import path


app_name = "authentication"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("cadastro/", views.CadastroView.as_view(), name="cadastro"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),
]
