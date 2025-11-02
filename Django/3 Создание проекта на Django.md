# Создание проекта на Django

Пошаговое руководство по созданию вашего первого Django проекта.

## 1. Подготовка окружения

### Создание виртуального окружения (рекомендуется)
```bash
# Создаем виртуальное окружение
python -m venv myenv

# Активируем виртуальное окружение
# Windows:
myenv\Scripts\activate
# Linux/Mac:
source myenv/bin/activate
```

### Установка Django
```bash
# Установка последней версии Django
pip install django

# Или конкретной версии
pip install django==4.2.0

# Проверяем установку
python -m django --version
```

## 2. Создание проекта

### Основная команда
```bash
# Создаем новый проект
django-admin startproject mysite

# Переходим в папку проекта
cd mysite
```

### Дополнительные опции создания
```bash
# Создание проекта в указанной директории
django-admin startproject mysite /path/to/your/project

# Создание проекта с точкой для текущей директории
django-admin startproject mysite .
```

## 3. Структура созданного проекта

После выполнения команды создается следующая структура:

```
mysite/                 # Корневая директория проекта
│
├── manage.py          # Утилита для управления проектом
│
└── mysite/            # Пакет проекта (основные настройки)
    ├── __init__.py    # Пустой файл, делает папку Python пакетом
    ├── settings.py    # Настройки проекта
    ├── urls.py        # Маршрутизация URL
    ├── asgi.py        # Конфигурация для ASGI-серверов
    └── wsgi.py        # Конфигурация для WSGI-серверов
```

## 4. Первоначальная настройка

### Проверка работы проекта
```bash
# Запускаем сервер разработки
python manage.py runserver

# Или на конкретном порту
python manage.py runserver 8080
```

После запуска откройте браузер и перейдите по адресу `http://127.0.0.1:8000/`

### Выполнение первоначальных миграций
```bash
# Создаем таблицы в базе данных
python manage.py migrate
```

### Создание суперпользователя
```bash
python manage.py createsuperuser
# Следуйте инструкциям для создания администратора
```

## 5. Создание приложений внутри проекта

### Что такое приложение в Django?
Приложение — это модуль, который реализует конкретную функциональность.

```bash
# Создаем приложение для блога
python manage.py startapp blog

# Создаем приложение для пользователей
python manage.py startapp users

# Создаем приложение для продуктов
python manage.py startapp products
```

### Структура после создания приложений
```
mysite/
│
├── manage.py
├── db.sqlite3
│
├── mysite/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── blog/               # Приложение блога
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── ...
│
└── users/              # Приложение пользователей
    ├── migrations/
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── views.py
    └── ...
```

## 6. Настройка settings.py

### Регистрация приложений
```python
# mysite/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Наши приложения
    'blog',
    'users',
    'products',
]
```

### Настройка базы данных (опционально)
```python
# Для PostgreSQL вместо SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Настройка языка и времени
```python
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True
```

## 7. Настройка URLs

### Основной файл маршрутизации
```python
# mysite/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('users/', include('users.urls')),
    path('', include('products.urls')),  # главная страница
]
```

### Создание URLs для приложения
```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
]
```

## 8. Полный пример workflow

```bash
# 1. Создаем виртуальное окружение
python -m venv myproject_env
source myproject_env/bin/activate  # Linux/Mac

# 2. Устанавливаем Django
pip install django

# 3. Создаем проект
django-admin startproject myproject
cd myproject

# 4. Создаем приложения
python manage.py startapp blog
python manage.py startapp users

# 5. Настраиваем приложения в settings.py
# Добавляем 'blog' и 'users' в INSTALLED_APPS

# 6. Выполняем миграции
python manage.py migrate

# 7. Создаем суперпользователя
python manage.py createsuperuser

# 8. Запускаем сервер
python manage.py runserver
```

## 9. Полезные команды для нового проекта

```bash
# Проверка настроек
python manage.py check

# Создание миграций для моделей
python manage.py makemigrations

# Просмотр SQL миграций
python manage.py sqlmigrate blog 0001

# Запуск тестов
python manage.py test

# Сбор статических файлов
python manage.py collectstatic
```

## 10. Рекомендации для нового проекта

1. **Используйте виртуальное окружение** для изоляции зависимостей
2. **Создавайте отдельные приложения** для каждой функциональности
3. **Настройте .gitignore** сразу
4. **Используйте environment variables** для чувствительных данных
5. **Создайте requirements.txt**
   ```bash
   pip freeze > requirements.txt
   ```

Теперь у вас есть полностью настроенный Django проект, готовый к разработке!
