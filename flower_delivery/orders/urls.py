# orders/urls.py
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('order_success/', views.order_success, name='order_success'),  # Страница подтверждения заказа
    path('api/', include(router.urls)),  # Включаем URL-ы из DefaultRouter с префиксом "api/"
]

