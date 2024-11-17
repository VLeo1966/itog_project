# orders/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Order


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})

def order_success(request):
    return render(request, 'orders/order_success.html')  # Страница подтверждения заказа

