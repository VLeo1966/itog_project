# catalog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.flower_list, name='flower_list'),  # Главная страница каталога
    path('add_to_cart/<int:flower_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
]
