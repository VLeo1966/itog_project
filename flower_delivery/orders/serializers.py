# orders/serializers.py
from rest_framework import serializers
from catalog.models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'flower', 'quantity', 'price', 'order_date', 'address', 'email', 'phone', 'total_price']
