# catalog/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Flower
from orders.models import Order


def flower_list(request):
    flowers = Flower.objects.all()
    cart = request.session.get('cart', {})

    # Подсчет общей суммы корзины
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    return render(request, 'catalog/flower_list.html', {'flowers': flowers, 'cart': cart,
                                                        'total_price': total_price})


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


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if request.method == 'POST':
        for item_id, item in cart.items():
            flower = Flower.objects.get(id=item_id)
            Order.objects.create(
                user=request.user,
                flower=flower,
                quantity=item['quantity'],
                price=item['price'],
                address = request.user.profile.address,
                email = request.user.email,
                phone = request.user.profile.phone
            )
        # Очищаем корзину после оформления заказа
        request.session['cart'] = {}
        return redirect('order_success')  # Перенаправляем на страницу подтверждения заказа

    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'catalog/checkout.html', {'cart': cart, 'total_price': total_price})


def order_success(request):
    return render(request, 'catalog/order_success.html')
