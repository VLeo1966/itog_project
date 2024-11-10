import os
import sys
import django
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from django.utils import timezone
from datetime import datetime
from decimal import Decimal
from django.db import IntegrityError

# Настройка Django для взаимодействия с базой данных
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')
django.setup()  # Инициализация Django, должна быть до импорта моделей

from catalog.models import Flower
from orders.models import Order
from users.models import Profile
from django.contrib.auth.models import User

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



# Асинхронная функция для привязки Telegram ID к пользователю
@sync_to_async
def link_telegram_id_to_user(telegram_id, username):
    try:
        user = User.objects.get(username=username)
        user.profile.telegram_id = telegram_id
        user.profile.save()
        return user
    except User.DoesNotExist:
        return None


# Асинхронная функция для поиска пользователя по Telegram ID
@sync_to_async
def get_user_by_telegram_id(telegram_id):
    try:
        profiles = Profile.objects.filter(telegram_id=telegram_id)
        if profiles.exists():
            # Предупреждаем о возможных дубликатах, используя первый профиль
            if profiles.count() > 1:
                print(f"Warning: Multiple profiles found for telegram_id {telegram_id}. Using the first one.")
            return profiles.first().user
        return None
    except Profile.DoesNotExist:
        return None


# Асинхронная функция для создания заказа
@sync_to_async
def create_order_in_db(user, flower, quantity, address, email, phone):
    return Order.objects.create(
        user=user,
        flower=flower,
        quantity=quantity,
        price=flower.price,
        address=address,
        email=email,
        phone=phone,
        order_date=datetime.now()
    )


# Команда /login для привязки Telegram ID к пользователю
@dp.message(Command("login"))
async def login_user(message: Message):
    try:
        _, username, password  = message.text.split(maxsplit=2)
        telegram_id = message.from_user.id
        user = await link_telegram_id_to_user(telegram_id, username)

        if user:
            await message.reply(f"Вы успешно вошли как {user.username}.")
        else:
            await message.reply(
                "Пользователь не найден. Если у вас нет аккаунта, пожалуйста, зарегистрируйтесь на сайте: https://ваш_сайт.ru/registration")
    except ValueError:
        await message.reply("Пожалуйста, введите команду в формате /login <имя_пользователя> <пароль>.")



# Команда для создания заказа
@dp.message(Command("order"))
async def create_order(message: Message):
    telegram_id = message.from_user.id
    user = await get_user_by_telegram_id(telegram_id)

    if user:
        try:
            # Разделяем команду на части
            parts = message.text.split()

            if len(parts) != 3:
                raise ValueError("Неверный формат. Используйте команду в формате /order <ID цветка> <количество>")

            _, flower_id, quantity = parts
            flower_id = int(flower_id)
            quantity = int(quantity)

            # Получаем информацию о цветке
            flower = await sync_to_async(Flower.objects.get)(id=flower_id)

            # Проверяем, что у цветка есть цена
            if flower.price is None or not isinstance(flower.price, (int, float, Decimal)):
                await message.reply("Ошибка: у выбранного цветка нет установленной цены.")
                return

            # Получаем данные из профиля пользователя
            address = user.profile.address
            email = user.profile.email
            phone = user.profile.phone

            # Создаём заказ
            order = await create_order_in_db(user, flower, quantity, address, email, phone)

            # Отправляем подтверждение
            total_price = flower.price * quantity
            await message.reply(f"Заказ успешно создан!\n"
                                f"Цветок: {flower.name}\n"
                                f"Количество: {quantity}\n"
                                f"Сумма: {total_price} руб.\n"
                                f"Дата заказа: {order.order_date}")
        except ValueError as ve:
            # Обработка ошибок при неверном формате данных
            await message.reply(f"Ошибка: {str(ve)}")
        except Flower.DoesNotExist:
            # Если цветок с таким ID не найден
            await message.reply("Ошибка: цветок с таким ID не найден.")
        except Exception as e:
            # Обработка других ошибок
            await message.reply(f"Произошла ошибка: {str(e)}")
    else:
        await message.reply("Вы не авторизованы. Пожалуйста, используйте /login для авторизации.")



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())