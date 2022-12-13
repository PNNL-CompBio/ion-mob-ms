from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_home) #localhost:8000/api/
]
