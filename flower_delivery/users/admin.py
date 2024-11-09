# users/admin.py
from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone', 'email', 'telegram_id')  # Показываем в админке


admin.site.register(Profile, ProfileAdmin)

