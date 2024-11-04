# orders/admin.py
from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'flower', 'quantity', 'price', 'total_price', 'order_date', 'address', 'email', 'phone')


admin.site.register(Order, OrderAdmin)

