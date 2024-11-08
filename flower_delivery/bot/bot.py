import os
import sys
import django
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from asgiref.sync import sync_to_async


# Настройка Django для взаимодействия с базой данных
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')
django.setup()  # Инициализация Django, должна быть до импорта моделей


from catalog.models import Flower
from orders.models import Order


API_TOKEN = '7843222297:AAGIsnQ6v247JoCJUcUOfiNl_aCAf30fFho'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Команда /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Добро пожаловать в FlowerDelivery! Используйте /catalog для просмотра каталога цветов.")

@sync_to_async
def get_all_flowers():
    return list(Flower.objects.all())  # Преобразуем QuerySet в список для асинхронной обработки

# Асинхронная обертка для проверки существования цветов
@sync_to_async
def check_flowers_exist():
    return Flower.objects.exists()

# Асинхронная обертка для создания заказа
@sync_to_async
def create_order_in_db(flower, quantity):
    return Order.objects.get(
        user=None,  # Укажите пользователя, если он есть в контексте
        flower=flower,
        quantity=quantity,
        price=flower.price,
        address="ул. Пример, д. 1",  # Примерный адрес
        email="example@mail.com",  # Примерный email
        phone="+123456789"  # Примерный телефон
    )

# Асинхронная обертка для получения цветка по id
@sync_to_async
def get_flower_by_id(flower_id):
    return Flower.objects.get(id=flower_id)

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Добро пожаловать в FlowerDelivery! Используйте /catalog для просмотра каталога цветов.")

# Команда для просмотра каталога
@dp.message(Command("catalog"))
async def show_catalog(message: Message):
    try:
        if await check_flowers_exist():
            flowers = await get_all_flowers()
            catalog_text = "Каталог цветов:\n\n"
            for flower in flowers:
                catalog_text += f"{flower.id}. {flower.name} - {flower.price} руб.\n"
            catalog_text += "\nВведите /order <ID цветка> <количество> для заказа."
            await message.reply(catalog_text)
        else:
            await message.reply("Каталог пуст.")
    except Exception as e:
        await message.reply(f"Ошибка при загрузке каталога: {str(e)}")

# Команда для создания заказа
# Команда для создания заказа
@dp.message(Command("order"))
async def create_order(message: Message):
    try:
        # Разбираем сообщение для получения ID цветка и количества
        _, flower_id, quantity = message.text.split()
        flower_id = int(flower_id)
        quantity = int(quantity)

        # Получаем цветок из базы данных
        flower = await get_flower_by_id(flower_id)

        # Проверяем, что у цветка указана цена и она является числом
        if flower.price is None:
            await message.reply("Ошибка: у выбранного цветка нет установленной цены. Пожалуйста, выберите другой цветок или уточните информацию.")
            return
        elif not isinstance(flower.price, (int, float)):
            await message.reply("Ошибка: цена цветка указана некорректно. Пожалуйста, проверьте значение цены.")
            return

        # Вычисляем общую стоимость
        total_price = flower.price * quantity

        # Создаем заказ в базе данных
        order = await create_order_in_db(flower, quantity)

        # Отправляем подтверждение
        await message.reply(f"Заказ успешно создан! Сумма заказа: {total_price} руб.")
    except (ValueError, Flower.DoesNotExist) as e:
        await message.reply(f"Ошибка при создании заказа: {str(e)}")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {str(e)}")
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())