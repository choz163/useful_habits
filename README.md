# Habit Tracker Backend

Полноценный бэкенд трекера привычек на Django + Django REST Framework + Celery + Telegram-бот.  
Позволяет пользователям:

- создавать, редактировать, удалять и просматривать свои привычки;
- публиковать привычки для общего доступа;
- получать ежедневные напоминания в Telegram;
- регистрироваться и входить через JWT;
- смотреть Swagger-документацию.

---

## Основные технологии

- Python 3.9+
- Django 4.2
- Django REST Framework
- Celery + Redis (брокер и backend для задач)
- python-telegram-bot
- djangorestframework-simplejwt (JWT-аутентификация)
- drf-yasg (авто-документация Swagger)
- pytest + pytest-django + pytest-cov (тесты и покрытие)
- flake8 (статический анализ)

---

## Критерии выполненного задания

1. CORS настроен (django-cors-headers)  
2. Интеграция с Telegram-ботом + Celery-beat  
3. Пагинация 5 привычек на страницу  
4. Переменные окружения через `.env`  
5. Все модели и валидаторы на месте  
6. CRUD-эндпоинты + публичный список  
7. Права доступа: свои CRUD, чужие только read  
8. Отложенные задачи через Celery  
9. Покрытие тестами ≥ 80% (pytest-cov)  
10. Flake8 без ошибок (исключая миграции)  
11. Swagger UI: `/swagger/`  
12. README с инструкцией

---

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/choz163/useful_habits.git
cd habit-tracker
Копировать

2. Виртуальное окружение и зависимости

python3 -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

pip install --upgrade pip
pip install -r requirements.txt
Копировать

3. Настройка переменных окружения

Создайте файл .env в корне проекта:


SECRET_KEY=любая_строка_для_секретного_ключа
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CELERY_BROKER_URL=redis://localhost:6379/0
TELEGRAM_TOKEN=ваш_токен_бота_из_BotFather

4. Применение миграций

python manage.py makemigrations
python manage.py migrate
Копировать

5. Запуск Redis

Убедитесь, что запущен Redis на localhost:6379.


6. Запуск Celery

В одном терминале:


celery -A config worker --loglevel=info
Копировать

В другом — планировщик задач (beat):


celery -A config beat --loglevel=info
Копировать

7. Запуск Django-сервера

python manage.py runserver
Копировать

Теперь API доступно по http://127.0.0.1:8000/.



Telegram-бот


В чате с ботом /start

Бот сохранит ваш chat_id для рассылок

Celery-beat каждую минуту выполняет задачу send_reminders, сравнивая текущее время с полем Habit.time и отправляет уведомления



Документация API

Swagger UI: http://127.0.0.1:8000/swagger/


Основные эндпоинты


POST /api/auth/login/ — получить JWT (поле username, password)

POST /api/auth/refresh/ — обновить токен

GET /api/habits/my/ — список своих привычек (JWT-заголовок)

POST /api/habits/my/ — создать привычку

GET /api/habits/public/ — список публичных

GET|PUT|DELETE /api/habits/{id}/ — операции над конкретной привычкой


Все CRUD-операции защищены, за исключением списка публичных привычек.



Тестирование и покрытие

# Запустить все тесты и получить текстовый + HTML-отчет
pytest

# Открыть HTML-отчет
open htmlcov/index.html  # Mac/Linux
start htmlcov\index.html # Windows
Копировать


Порог покрытия 80%: в pytest.ini стоит --cov-fail-under=80.

Отчётные файлы:

терминал: неохваченные строки

htmlcov/ — подробный HTML





Статический анализ

flake8 .
Копировать

Конфиг в .flake8:



max line length = 120

исключены миграции



Структура проекта

├── config/        # django-проект
│   ├── settings.py
│   ├── celery.py
│   └── urls.py
├── habits/               # приложение с моделью Habit
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   └── urls.py
├── notifications/        # Telegram + Celery задачи
│   ├── models.py
│   ├── bot.py
│   └── tasks.py
├── tests/                # pytest-тесты
├── requirements.txt
├── pytest.ini
├── .coveragerc
├── .flake8
└── README.md


CI/CD и деплой на сервер

Настройка CI/CD

Для настройки CI/CD вы можете использовать GitHub Actions, GitLab CI или другой инструмент. Пример конфигурации для GitHub Actions:



Создайте файл .github/workflows/ci.yml:


name: CI

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    services:
      redis:
        image: redis:latest
        ports:
          - 6379:6379

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest
Копировать

Деплой на сервер

Для деплоя на сервер используйте Docker. Пример Dockerfile:


FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
Копировать


Создайте образ Docker:


docker build -t habit-tracker .
Копировать


Запустите контейнер:


docker run -d -p 8000:8000 --env-file .env habit-tracker
Копировать

Теперь ваше приложение доступно на сервере по адресу http://<ваш_сервер>:8000/.



Полезные команды


python manage.py createsuperuser — создать администратора

python manage.py shell — Django shell

pytest --maxfail=1 --disable-warnings -q — быстрый прогон тестов



Контакты и поддержка

Если возникли вопросы, откройте issue в репозитории или напишите на почту: your.email@example.com.


Спасибо за использование Habit Tracker!

