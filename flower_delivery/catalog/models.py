# catalog/models.py
from django.db import models


class Flower(models.Model):
    name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='media/flowers/', blank=True, null=True)

    class Meta:
        verbose_name = 'Цветок'
        verbose_name_plural = 'Цветы'

    def __str__(self):
        return self.name



