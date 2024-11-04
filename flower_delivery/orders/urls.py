# orders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('order_success/', views.order_success, name='order_success'),  # Страница подтверждения заказа
]
