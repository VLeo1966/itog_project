from django.db import models
from django.contrib.auth.models import User
from catalog.models import Flower
from django.utils import timezone


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Пользователь")
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, verbose_name="Цветок")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая цена", null=True)
    order_date = models.DateTimeField(default=timezone.now, verbose_name="Дата заказа")  # Default value set to timezone.now
    address = models.CharField(max_length=255, verbose_name="Адрес доставки", null=True)
    email = models.EmailField(verbose_name="Email", null=True)
    phone = models.CharField(max_length=15, verbose_name="Телефон", null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price  # Calculate total price before saving
        super().save(*args, **kwargs)





