# catalog/views.py
from django.shortcuts import render, redirect
from .models import Flower
from django.shortcuts import render


def flower_list(request):
    flowers = Flower.objects.all()
    cart = request.session.get('cart', {})

    # Подсчет общей суммы корзины
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    return render(request, 'catalog/flower_list.html', {'flowers': flowers, 'cart': cart, 'total_price': total_price})


def add_to_cart(request, flower_id):
    flower = Flower.objects.get(id=flower_id)
    cart = request.session.get('cart', {})

    if str(flower_id) in cart:
        cart[str(flower_id)]['quantity'] += 1
    else:
        cart[str(flower_id)] = {
            'name': flower.name,
            'price': float(flower.price),
            'quantity': 1,
            'total_price_per_item': float(flower.price)  # Начальная стоимость за единицу
        }

    # Обновляем `total_price_per_item` в зависимости от количества
    cart[str(flower_id)]['total_price_per_item'] = cart[str(flower_id)]['price'] * cart[str(flower_id)]['quantity']

    request.session['cart'] = cart
    return redirect('flower_list')


def clear_cart(request):
    # Очистка корзины
    request.session['cart'] = {}
    return redirect('flower_list')


def checkout(request):
    cart = request.session.get('cart', {})
    for item_id, item in cart.items():
        item['total_price_per_item'] = item['price'] * item['quantity']
    total_price = sum(item['total_price_per_item'] for item in cart.values())
    return render(request, 'catalog/checkout.html', {'cart': cart, 'total_price': total_price})
