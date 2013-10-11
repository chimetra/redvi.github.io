Title: Абсолютные пути URL в Django
Date: 2013-10-03 1:15
Tags: Django
Slug: get-absolute-url
Author: redVi
Summary: Как получить полный путь URL-страницы в Django

В одной из [предыдущих заметок](http://www.unix-lab.org/articles/django-first-steps.html), нами был написан шаблон для вывода списка публикаций на главной странице. Ссылка на полный текст публикации имеет вид `{% url 'articles:detail' post.id %}`, что позволяет получить определённую страницу по её идентификатору (`id`). За отображение страницы ответственность несёт представление `articles` из пространства имён (`namespace`) `detail`. В данном ниже примере для разнообразия используем другую модель, а также для упрощения понимания материала откажемся от использования пространств имён: одно приложение &mdash; одна модель &mdash; один urls.py.

И всё бы хорошо, но ссылки подобного вида иногда могут не подойти вам. Вот пара простых примеров, иллюстрирующих этот тезис:

- Вам нужно получить статью по slug
- Вам нужно отобразить ссылки на предыдущую и следующую статью

Что же, разберём указанные примеры по-порядку.

###Вид urls.py

Создание файла `urls.py`, отвечающего нашим запросам. Отображено использование обобщённых представлений, подробности о которых вы без труда найдёте в документации.

У нас имеется представление `IndexView`, на которое возложен вывод индексной страницы со списком последних публикаций, а также `DetailView`, которое выводит отдельную запись. В шаблоне к ним можно обращаться как к `latest_articles_list` и `detail` соответственно.

    :::python
    # urls.py

    from django.conf.urls import patterns, include, url
    from .views import IndexView, DetailView


    urlpatterns = patterns('',
        url(r'^$', IndexView.as_view(), name='latest_articles_list'),
        url(r'^articles/(?P<slug>[-\w]+)/$', DetailView.as_view(template_name = 'article.html'), name='detail'),
    )

###Обращение по первичному ключу

В случае, когда нужно получить объект по `slug`, нам важно знать, что любая модель имеет свой первичный ключ (`primary key`) и его можно переопределить. По-умолчанию первичным ключом является поле `id`, генерируемое автоматически. Таким образом, мы получаем URL вида:

    http://site.org/articles/1/
    http://site.org/articles/2/

А хотим видеть такие адреса:

    http://site.org/articles/krasivyi-url/
    http://site.org/articles/po-poly-slug/

Самым простым решением является переопределение первичного ключа, но в этом случае вы больше не сможете обращаться к полю модели по `id`.

    :::python
    # models.py

    from django.db import models


    class Article(models.Model):
        ''' Create Post '''
        title = models.CharField(max_length=150, verbose_name='Title')
        content = models.TextField()
        pub_date = models.DateField(auto_now=True, verbose_name='Create Date')
        update = models.DateField(auto_now=False, blank=True, null=True,verbose_name='Last Update')
        author = models.ForeignKey(to=User, verbose_name='Author')
        slug = models.SlugField(primary_key=True, max_length=250, unique=True)
        summary = models.TextField(blank=True, max_length=250, help_text='Meta Description')

Как мог заметить наблюдательный читатель, мы задали поле `slug` со значением `primary_key=True`. Предполагается, что в этом поле будет установлен устраивающий автора красивый URL. Теперь следует ссылаться на детальное представление публикации именно по этому полю. Конкретный пример будет приведён чуть ниже.

**Примечание**: если при создании представления вы используете обобщённые представления, вернуть публикацию по полю `slug`, не нагромождая ваше представление и не затрагивая `primary key`, также может быть очень легко. В этом вам посодействуют `DetailView` и `get_object_or_404`:

    # views.py

    from django.shortcuts import get_object_or_404
    from django.views.generic.detail import DetailView

    class DetailView(DetailView):
        """ Return detail data """
        model = Article
        context_object_name = 'article'

        def get_object(self):
            return get_object_or_404(Article, slug__iexact=self.kwargs['slug'])

Прежде, чем приступить к написанию шаблонов, решим второй вопрос: о получении абсолютных путей к объекту.

###Абсолютные пути

Итак, для примера мы решили, что будем выводить предыдущую и следующую статью при обращении к статье текущей. Если просто обращаться к статье по указанному ключу, можно поиметь некоторые проблемы. Наш URL имеет относительный путь, поэтому при наведении на любую ссылку внутри поста, которая сформирована также (то есть с указанием `{% url 'view' object.slug %}`), первичный ключ выбранной статьи просто будет добавлен к уже имеющемуся адресу. Вот так:

    имеем:
    http://site.org/articles/my-article
    при наведении на другую ссылку получим:
    http://site.org/articles/my-article/my-next-article

Поэтому мы добавим к нужной модели спасательный круг в виде метода `get_absolute_url` и сразу же выведем в шаблоне именно то, что нужно.

    :::python
    # models.py

    from django.db import models
    from django.core.urlresolvers import reverse


    class Article(models.Model):
        title = models.CharField(max_length=150, verbose_name='Title')
        content = models.TextField()
        ...

        def get_absolute_url(self):
            return reverse('detail', args=[str(self.slug)])


###Подготовка шаблонов

Теперь в шаблонах мы можем ссылаться на статью по её абсолютному адресу, используя `get_absolute_url`. Примеры:

подобным образом может выглядеть индексная страница со списком последних публикаций

    :::html
    <!--index.html-->
    {% extends "base.html" %}
    {% block content %}
    <div id="main">
        {% for article in latest_articles_list %}
          <a href="{{ article.get_absolute_url }}">{{ article.title }}</a>
        {% endfor %}
    </div>
    {% endblock content %}


а на странице детального представления можно добавить ссылки на предыдущий и следующий пост

    :::html
    <!--article.html-->
    {% extends "base.html" %}
    {% block content %}
    <div id="main">
    <h2><a href="{{ article.get_absolute_url }}">{{ article.title }}</a></h2>
    {{ article.content }}
    <div class="links">
    <a href="{{ article.get_next_by_pub_date.get_absolute_url }}">Next</a>
    <a href="#">on top</a>
    <a href="{{ article.get_previous_by_pub_date.get_absolute_url }}">Prev</a>
    </div>
    </div>
    {% endblock %}

`Model.get_next_by_pub_date` вернёт следующую публикацию, основываясь на дате её создания

`Model.get_previous_by_pub_date` отобразит предыдущую публикацию.

Применив к ним метод `get_absolute_url`, мы получим искомое решение.
