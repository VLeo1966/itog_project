# catalog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.flower_list, name='flower_list'),  # Главная страница каталога
]
