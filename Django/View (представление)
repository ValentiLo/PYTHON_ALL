В Django **view** (представление) — это функция или класс, который обрабатывает веб-запрос и возвращает веб-ответ. Вот различные примеры views:

## 1. Простая функция-based view

```python
from django.http import HttpResponse
from django.shortcuts import render

# Самый простой view
def hello_world(request):
    return HttpResponse("Привет, мир!")

# View с параметром
def greet_user(request, name):
    return HttpResponse(f"Привет, {name}!")

# View с HTML
def about(request):
    html = """
    <html>
        <body>
            <h1>О нас</h1>
            <p>Это страница о нашей компании.</p>
        </body>
    </html>
    """
    return HttpResponse(html)
```

## 2. View с использованием шаблонов

```python
from django.shortcuts import render

def home_page(request):
    context = {
        'title': 'Главная страница',
        'message': 'Добро пожаловать на наш сайт!',
        'users': ['Анна', 'Петр', 'Мария']
    }
    return render(request, 'home.html', context)

def product_detail(request, product_id):
    # Пример с данными о продукте
    product_data = {
        'id': product_id,
        'name': 'Пример товара',
        'price': 1000,
        'description': 'Описание товара'
    }
    return render(request, 'product_detail.html', {'product': product_data})
```

## 3. View с обработкой форм

```python
from django.shortcuts import render, redirect
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Обработка данных формы
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Сохранение или отправка email
            # ...
            
            return redirect('success_page')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')
```

## 4. View с разными HTTP методами

```python
from django.http import JsonResponse

def api_example(request):
    if request.method == 'GET':
        data = {
            'message': 'Это GET запрос',
            'status': 'success'
        }
        return JsonResponse(data)
    
    elif request.method == 'POST':
        # Обработка POST данных
        name = request.POST.get('name', 'Неизвестно')
        return JsonResponse({'received_name': name})
```

## 5. Class-Based Views (CBV)

```python
from django.views import View
from django.shortcuts import render
from .models import Article

class ArticleListView(View):
    def get(self, request):
        articles = Article.objects.all()
        return render(request, 'article_list.html', {'articles': articles})

class ArticleDetailView(View):
    def get(self, request, article_id):
        article = Article.objects.get(id=article_id)
        return render(request, 'article_detail.html', {'article': article})
```

## 6. View с проверкой аутентификации

```python
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

def admin_only_view(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Доступ запрещен")
    return render(request, 'admin_panel.html')
```

## 7. View с обработкой ошибок

```python
from django.shortcuts import render
from django.http import Http404
from .models import Product

def product_view(request, product_slug):
    try:
        product = Product.objects.get(slug=product_slug)
    except Product.DoesNotExist:
        raise Http404("Товар не найден")
    
    return render(request, 'product.html', {'product': product})

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
```

## 8. Практический пример блога

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm

def post_list(request):
    posts = Post.objects.filter(published=True).order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'form': form
    })
```

## Настройка URLs для views

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('blog/', views.post_list, name='post_list'),
    path('blog/<slug:slug>/', views.post_detail, name='post_detail'),
    path('api/example/', views.api_example, name='api_example'),
    
    # Class-Based Views
    path('articles/', views.ArticleListView.as_view(), name='article_list'),
]
```

## Шаблоны для views

```html
<!-- home.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
    
    <ul>
    {% for user in users %}
        <li>{{ user }}</li>
    {% endfor %}
    </ul>
</body>
</html>
```

**Ключевые моменты:**
- View всегда принимает `request` первым параметром
- Возвращает `HttpResponse` или его подклассы
- Может использовать шаблоны через `render()`
- Может быть функцией или классом
- Обрабатывает различную логику приложения
