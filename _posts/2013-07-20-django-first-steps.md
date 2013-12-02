---
layout: post
title: "Django: первые страницы"
date: 2013-07-20 11:40
tags: [python]
summary: "Пример первоначальной настройки и наполнения сайта на Django"
---

Не правда ли, было бы любопытно опробовать знаменитый фреймворк Django для создания сайтов разной степени сложности? Если вам по душе узнавать что-то новое или вы по каким-либо причинам решили отказаться от разработки на PHP — Django как раз то, что вам нужно. В сегодняшнем посте будут оговорены элементарные, но такие необходимые вещи: создание проекта и приложения, модели и отображения, шаблонов с использованием стандартных фильтров. Не исключено, что автор продолжит начатую тему и в последующем будет опубликован ряд постов об этом популярном фреймворке.

Далее предполагается, что у читателя установлен `Python3` и `Django >=1.5`: именно на них рассчитаны наши последующие телодвижения. Устанавливать необходимые для конкретного проекта приложения лучше используя [virtualenw и pip](http://www.unix-lab.org/posts/virtualenv/). Так вы сможете избавить себя от чтения руководств по установке и захламления системных файлов.

## Создание проекта и приложения

Проект — основной каталог, где будут располагаться те или иные приложения, также проект содержит основные настройки будущего сайта. Создадим корневой каталог для проекта и сам проект:

```console
$ mkdir djcode && cd djcode
$ django-admin.py startproject pySite
```

Просмортим появившиеся каталоги:

```console
$ tree pySite
pySite
├── manage.py
└── pySite
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

Вкратце:

`manage.py` — отвечает за управление проектом, например, командой `python manage.py runserver` можно запустить сервер для тестовой разработки.

`__init__.py` — нужен для того, чтобы python рассматривал каталог `pySite` как пакет.

`settings.py` — файл настроек проекта: настройки языка, часового пояса, соединения с базой данных, подключаемых приложений и прочего.

`urls.py` — настройки URL-адресов для сайта

`wsgi.py` — конфигурация модуля `wsgi` для веб-сервера

Хорошо, когда проект расширяемый. Ещё лучше, если его легко сопровождать. Оба этих условия выполняются в Django. Чтобы расширить функционал сайта, следует создать для него какое-либо приложение: галерею, форум, блоги. Затем лишь подключить его в `settings.py` и подправить свой `urls.py`, дабы при переходе по определённому адресу пользователь перенаправлялся к страницам приложения. Поэтому давайте создадим какое-нибудь приложение. Пусть оно отвечает за публикацию новостей и хранится в том же каталоге, что и основной проект.

```console
$ django-admin.py startapp news
$ tree pySite
pySite
|-- pySite
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   |-- views.py
|   `-- wsgi.py
|-- manage.py
|-- news
|   |-- admin.py
|   |-- __init__.py
|   |-- models.py
|   |-- tests.py
|   |-- urls.py
|   `-- views.py
```

Вкратце:

`models.py` — файл для взаимодействия с базой данных

`urls.py` — отдельный файл url'ов. Он может быть пустым, если вы решите использовать для всех адресов `urls.py` проекта

`admin.py` — создаётся вручную, нужен исключительно для удобства: настройка отображения моделей в административной панели

`views.py` — самое интересное, управляет логикой приложения

С приложением определились. Отлично! Пора браться за настройки.

## Настройки для сайта

Заглянем в файл `settings.py` и настроим его под свои скромные пока нужды.

`PROJECT_PATH` — указание на то, где Django нужно искать корень проекта. Лучше использовать запись, приведённую ниже, чем писать полный путь вроде `~/home/user/djcode/pySite`.

`DEBUG = True` — отладка влючена, Django будет выводить информативные сообщения об ошибках.

`DATABASES` — настройки для вашей базы данных. В примере это `sqlite3`, который не требует особого к себе отношения, но и полноценной базой данных для сайта на production-сервере быть не может. Чтобы использовать `sqlite3`, достаточно создать в директории проекта файл `sqlite.db`. О настройке PostgreSQL [читаем отдельно](http://www.unix-lab.org/posts/postgresql/).

```python
from os.path import abspath, join, dirname


PROJECT_PATH = abspath(join(dirname(__file__), '..'))
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  join(PROJECT_PATH, 'sqlite.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
```

Идём дальше. Желательно сразу создать и подключить директорию, где будет храниться статика: css, javascript и изображения.  Кроме того, нам понадобится директория под наши html-файлы.

`STATIC_URL` — относительный url для статики

`STATICFILES_DIRS` — директория, где расположены соответствующие файлы

`TEMPLATE_LOADERS` — модули для работы с шаблонами

`TEMPLATE_DIRS` — указание на директорию, где лежат html-шаблоны

`ROOT_URLCONF` — главный файл url'ов

`INSTALLED_APPS` — подключенные приложения, вниз добавим наш news.

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = (join(PROJECT_PATH, 'static'),)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

ROOT_URLCONF = 'pySite.urls'
TEMPLATE_DIRS = (
    join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'news',
)
```

Теперь можно проверить сайт на работоспособность. Для этого, находясь в директории с `manage.py` следует ввести команду:

```console
$ python manage.py syncdb
$ python manage.py runserver
```

Первая команда создаст записи в базе данных и предложит создать суперпользователя, если вы подключили приложение административной панели, вторая — запустит тестовый сервер разработки.

По адресу `127.0.0.1:8000/` должно появиться стандартное окно приветствия Django.

## Создание модели и представления, конфигурация `urls.py`

Следующим шагом будет настройка моделей для взаимодействия с БД, создание представления (логика приложения), настройка файла `urls.py`.

В примере ниже создаётся класс `Post`, подкласс абстрактного класса `models.Model`. Мы хотим видеть у нашего поста название (`title`), его тело (`body`), дату создания (`timestamp`) и автора (`author`). Обратите внимание на `models.*Field`. Каждая модель соответствует указанному полю.

Так, `models.CharField` выведет несколько символов, максимальное их значение 150, этого должно хватить для названия;

`models.TextField` позволит вводить неограниченное число символов: полноценный текст;

`models.ForeignKey` указывает на то, что у поста может быть один автор.

Эти таблицы будут созданы в базе данных при синхронизации.

```python
# ~/djcode/pySite/news/models.py

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    timestamp = models.DateTimeField()
    author = models.ForeignKey(User)


    def __unicode__(self):
        return self.title
        return self.body
```

Теперь создадим наше первое представление. Оно призвано выводить список постов на одной странице. О том, как сделать постраничный вывод поговорим [в следующий раз](http://www.unix-lab.org/posts/django-pagination/).

```python
# djcode/pySite/news/views.py

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from .models import Post


def news(request):
    ''' Show all news '''
    posts = Post.objects.all().order_by('-timestamp')
    return render_to_response('news/news.html', {'posts':posts})
```

Совсем не сложно, верно? Это простейшее представление, которое принимает все существующие посты и выводит их на определённой странице. Чуть ниже мы создадим эту страницу. Но сначала наполним сайт каким-нибудь содержимым. Административная панель уже подключена в нашем `INSTALLED_APPS`, осталось только зайти и проверить как отображаются созданные нами модели. Для отображения их в админке создадим ещё один файл (можно вписать это и в предыдущем файле `views`, но разделить их иногда удобнее):

```python
# djcode/pySite/news/admin.py

from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    models = Post
    list_display = ('title', 'timestamp')
    list_filter = ('timestamp',)


admin.site.register(Post, PostAdmin)
```

Раскомментируйте в вашем `~/djcode/pySite/pySite/urls.py` строки

```python
# djcode/pySite/pySite/urls.py

from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

)
```

После того, как вы зайдёте по адресу `127.0.0.1:8000/admin/` и создадите несколько постов, вы должны увидеть нечто подобное:

<a href="http://farm4.staticflickr.com/3828/9470173657_8ac19b5dab_b.jpg" data-lighter><img src="http://farm4.staticflickr.com/3828/9470173657_8ac19b5dab_b.jpg"/></a>

Вернёмся к шаблонам. Вообще, создание страниц мы разделим на два этапа: создание базовой страницы и остальных страниц, которые будут просто наследовать содержимое базового шаблона. Это будет весьма кстати, если только вам не хочется писать каждую страницу с нуля.



Так будет выглядеть шаблон базовой страницы:

```html+django
{% raw %}
# djcode/pySite/templates/base.html

{% load static from staticfiles %} <!-- подгружаем статику -->
{% load i18n  %}
<!DOCTYPE HTML>
<html>
<head>
{% block meta %}
<!-- подключаем наш css-файл, если он есть -->
<link rel="stylesheet" type="text/css" href="{% static "css/base.css" %}" />
{% endblock %}
<title>{% block title %}My Django Site{% endblock %}</title>
</head>
<body>
{% block header %}
    {% include "header.html" %} <!-- подключаем «шапку» сайта -->
{% endblock %}
<div id="content">
    {% block content %}{% endblock %} <!-- место для контента -->
</div>
{% block footer %} <!-- подключаем «подвал» сайта -->
    {% include "footer.html" %}
{% endblock %}
</body>
</html>
{% endraw %}
```

Теперь примемся за шаблон, который выведет все наши посты.

```html+django
{% raw %}
# djcode/pySite/templates/news/news.html

{% extends 'base.html' %} <!-- подключаем базовый шаблон -->
{% block title %}News{% endblock %}
{% block content %}
    <div id="post">
        {% for post in posts %} <!-- итерация по всем постам -->
            <dl>
              <dd><h3><a href="{% url 'news:one_new' post.id %}">{{ post.title }}</a></h3></dd>
            </dl>
        {{ post.timestamp }} <!-- дата публикации -->
        {{ post.author }} <!-- автор -->
        {{ post.body|truncatewords:80|safe }} <!-- обрезаем посты, вывод по 80 слов -->
        <!-- ссылаемся на полный текст поста -->
        <a href="{% url 'news:one_new' post.id %}">Читать полностью&raquo;</a>
        {% endfor %}
    </div>
{% endblock %}
{% endraw %}
```

Как уже, должно быть, заметил читатель, мы сразу влючили ссылку на пока несуществующее представление: вывод отдельного поста целиком. Что требуется для его создания? Дальнейшие наши шаги сводятся к созданию ещё одной функции: на этот раз она будет выводить отдельную страницу, подготовки для неё своего шаблона и настройке файла `urls.py`. Приступим.

```python
# djcode/pySite/news/views.py

# после функции news дописать
def one_new(request, post_id):
    ''' Show single news'''
    post = get_object_or_404(Post, pk=post_id)


    vars = dict(
        title=post.title,
        body=post.body,
        author=post.author,
        timestamp=post.timestamp,
        )

    return render_to_response('news/one_new.html', vars, context_instance=RequestContext(request))
```

Переменной post передаётся объект `Post` с его ID либо вызывается исключение `404`: страница не найдена. Определяется то, что должно быть выведено: название, автор, время создания. Возвращается страница `one_new.html`, которой мы сейчас и займёмся.

```html+django
{% raw %}
# djcode/pySite/templates/news/one_new.html

{% extends 'base.html' %} <!-- подключаем базовый шаблон -->
<!-- отображать название поста как title страницы-->
{% block title %}{{ title }}{% endblock %}
{% block content %}
Дата: {{ timestamp }}
Автор: {{ author }}
<h1>{{ title }}</h1>
<div>{{ body|safe|escape}}</div> <!-- экранировать HTML-->
<!-- escape переводит HTML-теги, если вы использовали их
    при написании статьи в админке -->
{% endblock %}
{% endraw %}
```

Для полного и безоблачного счастья напишем функцию и шаблон для главной страницы, с которой будем переходить на последние десять записей. Не волнуйтесь! Это очень простые операции, хотя если данный пост — первое, что встретилось вам на пути изучения Django, возможно, вы сможете разобраться не с первого чтения... но со второго точно ;)

Итак, представление и шаблон главной страницы:

```python
# djcode/pySite/pySite/views.py

from django.shortcuts import render_to_response
from django.template import RequestContext
from news.views import Post


# можно переписать как в news/views.py
def home(request):
    vars = dict (
            posts=Post.objects.all().order_by('-timestamp')[:10],
                )

    return render_to_response('index.html', vars, context_instance=RequestContext(request))
```

Собственно, шаблон для вывода последних десяти публикаций на главной:

```html+django
{% raw %}
# djcode/pySite/templates/index.html

{% extends "base.html" %}
{% block title %}Index Page{% endblock %}
{% block content %}
    <div id="post">
        <ul>
        {% for post in posts %}
            <li><a href="{% url 'news:one_new' post.id %}">{{ post.title }}</a></li>
        {% endfor %}
        </ul>
    </div>
{%endblock%}
{% endraw %}
```

Наконец, создадим два (в примере мы ведь отделяем все приложения друг от друга, чтобы их можно было подключать к другому проекту внесением одной лишь строки в `INSTALLED_APPS` и синхронизацией с БД) файла `urls.py`: один главный, другой  — персонально для созданного приложения news. При наличии пяти-десяти приложений это может быть удобным. Если приложение одно и со временем расширять функционал не требуется, создайте лишь один `urls.py`.

Импортируем необходимые модули, при входе на главную выводим представление, указанное в `pySite.views.home` функции, при входе на `http://127.0.0.1:8000/news` перенаправляем поиск в `news/urls.py`.

```python
# djcode/pySite/pySite/urls.py

from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'pySite.views.home', name='home'),
    url(r'^news/', include('news.urls', namespace='news')),
    url(r'^admin/', include(admin.site.urls)),

)
```

В следующем файле обрабатываем наши представления:

если пользователь заходит на страницу вывода всех новостей, использовать функцию `news.views.news`; если на конкретную новость — вывод выбранной новости из `news.views.one_new`:

```python
# djcode/pySite/news/urls.py

from django.conf.urls import patterns, include, url

urlpatterns = patterns('news.views',
    url(r'^$', 'news', name='news'),
    url(r'^(?P<post_id>\d+)/$', 'one_new', name='one_new'),

)
```

Дело сделано. Если всё прошло гладко, мы должны прийти примерно к подобному результату:

<a href="http://farm6.staticflickr.com/5343/9470178553_84ec6b3262_o.png" data-lighter><img src="http://farm6.staticflickr.com/5343/9470178553_84ec6b3262_o.png"/></a>

Успехов в изучении этого отличного фреймворка!
