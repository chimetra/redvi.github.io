Title: Django: постраничный вывод статей
Date: 2013-08-03 08:10
Tags: Django
Slug: django-pagination
Author: redVi
Summary: О том, как сделать постраничный вывод новостей в django.

Ни один сайт не состоит только лишь из одной страницы. Будь то блог, новостной портал или даже домашняя страничка Васи Пупочкина. Материала много, страницы нужно как-то выводить. Вывод всех публикаций на одной странице является по сути своей идеей порочной: бесконечно прокручивать список статей неудобно для пользователя, а про нагрузку на сервер лучше даже не вспоминать.

Для решения этой задачи в Django есть несколько способов и сегодня предлагается рассмотреть один из них: стандартный пагинатор. Рассмотрим пример, где нужно получить список всех публикаций и затем вывести их постранично.

В примере используются всё те же модели, что и [в предыдущем посте](django-first-steps.html). В класс `Paginator` следует передать список объектов и количество элементов, которые нужно отображать на одной странице. Далее используются методы класса для доступа к этим элементам.

###Модель публикации

```python
# models.py

class Post(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    timestamp = models.DateTimeField()
    author = models.ForeignKey(User)
    meta_keywords = models.CharField(blank=True, max_length=200)
    meta_description = models.TextField(blank=True, max_length=250)
```

###«Вьюха»

`post_lists` &mdash; получаем список всех публикаций, отсортированных по времени создания.

`paginator` &mdash; передаём классу `Paginator` наш список, указываем количество элементов на одну страницу

`paginator.page(1)` &mdash; возвращает объект `Page` по переданному индексу (начинается с единицы). Вызывает исключение `InvalidPage`, если указанная страница не существует.

`paginator.page(paginator.num_pages)` &mdash; отобразить общее количество страниц

```python
# views.py

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import Post

def news(request):
    '''Show all news'''
    posts_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts_list, 8)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    vars = dict(
        posts=posts,
        )
    return render_to_response('news.html', vars, context_instance=RequestContext(request))
```

###Шаблон

`for post in posts` &mdash; итерация по элементам

`post.has_previous` &mdash; возвращает `True` в случае, если предыдущая страница существует

`post.has_next` &mdash; возвращает `True` в случае, если следующая страница существует

`post.number` &mdash; выведет номер страницы

`post.previous_page_number` &mdash; вернуть предыдущую страницу

`post.next_page_number` &mdash; вернуть следующую страницу

```html
# news.html

{% extends 'base.html' %}
{% block title %}News{% endblock %}
{% block content %}
    <div id="post">
        {% for post in posts %}
        <ul>
        <li><a href="{% url 'news:one_new' post.id %}">{{ post.title}}</a></li>
        </ul>
        {{ post.timestamp }}
        {{ post.author }}<br />
        {{ post.body|truncatewords:80|safe }}<br />
         <a href="{% url 'news:one_new' post.id %}">Читать полностью</a>
        {% endfor %}
    <div id="pages" align="center">
        {% if posts.has_previous %}
            <a href="?page={{ posts.previous_page_number }}">Previous</a>
        {% endif %}
    <span class="current">
        Page {{ posts.number }} of {{ posts.paginator.num_pages }}.
    </span>
        {% if posts.has_next %}
            <a href="?page={{ posts.next_page_number }}">Next</a>
        {% endif %}
    </div>
    </div>
{% endblock %}
```

Страница документации: [Pagination](https://docs.djangoproject.com/en/dev/topics/pagination/)

