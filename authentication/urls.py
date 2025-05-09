

from authentication import views
from django.urls import path


app_name = "authentication"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),  
]
