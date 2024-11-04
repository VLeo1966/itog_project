# catalog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.flower_list, name='flower_list'),  # Главная страница каталога
    path('add_to_cart/<int:flower_id>/', views.add_to_cart, name='add_to_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),  # маршрут для очистки корзины
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
]
