import os
import sys


from datetime import datetime
from decimal import Decimal
from pathlib import Path

import asyncio

import django
from asgiref.sync import sync_to_async
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from django.conf import settings

# Настройка Django для взаимодействия с базой данных
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')
django.setup()  # Инициализация Django, должна быть до импорта моделей

from django.contrib.auth.models import User

from catalog.models import Flower
from orders.models import Order
from users.models import Profile


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



# Команда для просмотра каталога с изображениями


# Команда для просмотра каталога с изображениями
@dp.message(Command("catalog"))
async def show_catalog(message: Message):
    try:
        # Проверяем, есть ли цветы в каталоге
        if await check_flowers_exist():
            flowers = await get_all_flowers()
            for flower in flowers:
                # Генерация пути к изображению
                image_path = Path(settings.MEDIA_ROOT) / flower.image.name if flower.image else None

                # Ограничиваем описание до 500 символов, чтобы сохранить место для других полей
                description = flower.description[:500] + '...' if len(flower.description) > 500 else flower.description

                # Подготовка подписи, добавляя ID перед названием
                caption = f"ID цветка: {flower.id}\n{flower.name}\nОписание: {description}\nЦена: {flower.price} руб."
                if len(caption) > 1024:
                    caption = caption[:1021] + "..."  # Обрезаем до 1024 символов

                # Проверяем, есть ли изображение для цветка
                if image_path and image_path.exists():
                    # Используем FSInputFile для отправки изображения
                    photo = FSInputFile(image_path)
                    await bot.send_photo(
                        chat_id=message.chat.id,
                        photo=photo,
                        caption=caption
                    )
                else:
                    # Если изображения нет, отправляем только текстовую информацию
                    await message.reply(
                        f"ID: {flower.id}\n{flower.name}\nОписание: {description}\nЦена: {flower.price} руб.\n(Изображение отсутствует)"
                    )
            # Инструкция для заказа
            await message.reply("Введите /login <имя_пользователя> <пароль> для авторизации в системе \nВведите /order <ID цветка> <количество> для оформления заказа.")
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
        telegram_id = message.from_user.id  # это уникальный идентификатор пользователя в Telegram
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


# Команда /help
@dp.message(Command("help"))
async def send_help(message: Message):
    help_text = (
        "📚 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать список команд\n"
        "/login <имя_пользователя> <пароль> - Авторизоваться в системе\n"
        "/catalog - Просмотр каталога цветов\n"
        "/order <ID цветка> <количество> - Создать заказ на выбранный цветок\n"
        "/profile - Просмотр информации профиля\n"
        "/logout - Выйти из системы\n"
    )
    await message.reply(help_text)


# Команда /profile
@dp.message(Command("profile"))
async def view_profile(message: Message):
    telegram_id = message.from_user.id
    user = await get_user_by_telegram_id(telegram_id)

    if user:
        profile = user.profile
        profile_info = (
            f"👤 Профиль:\n\n"
            f"Имя пользователя: {user.username}\n"
            f"Адрес: {profile.address or 'не указан'}\n"
            f"Телефон: {profile.phone or 'не указан'}\n"
            f"Email: {profile.email or 'не указан'}\n"
            f"Дата регистрации: {user.date_joined.strftime('%Y-%m-%d')}\n"
        )
        await message.reply(profile_info)
    else:
        await message.reply("Вы не авторизованы. Пожалуйста, используйте /login для входа в систему.")


# Команда /logout
@dp.message(Command("logout"))
async def logout_user(message: Message):
    telegram_id = message.from_user.id
    user = await get_user_by_telegram_id(telegram_id)

    if user:
        # Убираем telegram_id из профиля для деавторизации
        await remove_telegram_id_from_profile(telegram_id)
        await message.reply("Вы успешно вышли из системы. Чтобы войти снова, используйте команду /login.")
    else:
        await message.reply("Вы не авторизованы. Пожалуйста, сначала выполните вход с помощью команды /login.")

# Асинхронная функция для удаления telegram_id из профиля
@sync_to_async
def remove_telegram_id_from_profile(telegram_id):
    try:
        profile = Profile.objects.get(telegram_id=telegram_id)
        profile.telegram_id = None
        profile.save()
    except Profile.DoesNotExist:
        pass


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())