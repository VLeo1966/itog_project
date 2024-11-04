# orders/models.py
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Flower


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Пользователь")
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, verbose_name="Цветок")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")

    def total_price(self):
        return self.quantity * self.price

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

