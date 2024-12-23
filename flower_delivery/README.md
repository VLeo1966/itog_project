# FlowerDelivery

FlowerDelivery — это веб-приложение для заказа и доставки цветов, интегрированное с Telegram-ботом. Пользователи могут просматривать каталог цветов, добавлять их в корзину, оформлять заказы и получать уведомления через Telegram. Приложение построено на Django с использованием Bootstrap для стилизации.

## Функции

- **Регистрация и авторизация пользователей**: Пользователи могут регистрироваться и входить в систему для создания заказов.
- **Каталог цветов**: Доступ к каталогу с описаниями, ценами и изображениями цветов.
- **Корзина**: Возможность добавлять цветы в корзину перед оформлением заказа.
- **Оформление заказа**: Система оформления заказа с указанием количества и способа доставки.
- **Telegram-уведомления**: Уведомления о заказах отправляются через Telegram-бота.
- **Личный кабинет**: Просмотр профиля, истории заказов и управление информацией.
- **Администрирование**: Управление заказами и каталогом цветов для администратора.

## Установка и настройка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/yourusername/flowerdelivery.git
    cd flowerdelivery
    ```

2. Создайте виртуальное окружение и активируйте его:

    ```bash
    python -m venv venv
    source venv/bin/activate  # для Linux/MacOS
    venv\Scripts\activate  # для Windows
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Настройте переменные окружения и Telegram-бота:

    - Создайте файл `.env` и добавьте туда необходимые переменные, такие как ключ API Telegram-бота, секретный ключ Django и конфигурации базы данных.
  
5. Выполните миграции и соберите статику:

    ```bash
    python manage.py migrate
    python manage.py collectstatic
    ```

6. Запустите сервер:

    ```bash
    python manage.py runserver
    ```

## Использование

1. **Каталог**: Чтобы просмотреть каталог через бота, используйте команду `/catalog`. Каталог также доступен на сайте.
2. **Оформление заказа**: Для оформления заказа используйте команду `/order <ID цветка> <количество>` в Telegram.
3. **Уведомления**: Подключите Telegram-бот для получения уведомлений о заказах и подтверждений.

## Структура проекта

- `bot/` — логика Telegram-бота для обработки заказов и уведомлений.
- `catalog/` — приложения для управления каталогом цветов. 
- `orders/` — оформление заказа.
- `users/` — управление профилями пользователей.
 

## Требования

- Python 3.10+
- Django 4.0+
- Aiogram для Telegram-бота
- PostgreSQL или SQLite

## Лицензия

Этот проект лицензирован под лицензией MIT. Подробнее см. файл LICENSE.

## Авторы

- [Ваше Имя](https://github.com/yourusername)

