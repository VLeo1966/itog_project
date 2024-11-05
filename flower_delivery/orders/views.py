# orders/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})

def order_success(request):
    return render(request, 'orders/order_success.html')  # Страница подтверждения заказа


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)