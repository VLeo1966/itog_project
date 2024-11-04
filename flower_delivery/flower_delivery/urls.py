# flower_delivery/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Указываем users в качестве корневого маршрута
    path('orders/', include('orders.urls')),
    path('', include('catalog.urls'))  # Каталог цветов
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Добавляем маршрут для медиа-файлов
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



