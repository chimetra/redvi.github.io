Title: Создание уникальных URL в Ruby On Rails
Date: 2013-10-15 13:15
Tags: Ruby
Slug: rails-slug-url
Author: redVi
Summary: Создание уникальных URL в Ruby On Rails


В [предыдущем посте](http://www.unix-lab.org/posts/get-absolute-url/) к рассмотрению был предложен вопрос о назначении собственных уникальных URL-адресов страницы и получения их полного пути. Сегодня тема та же, но другой фреймворк: для сравнения посмотрим как того же самого результата можно добиться в Ruby On Rails.

Собственно, почему вдруг Ruby? Нет, не будет утверждений будто он хуже или лучше Python'а, просто случайно попался на пути и весьма заинтриговал автора. Этого достаточно, чтобы черкнуть о нём пару строк. Не исключено (если дружба наша с Ruby станет крепнуть), что время от времени здесь будут появляться небольшие заметки о Ruby или Ruby On Rails.

Подробных объяснений базовых вещей сегодня не предвидится. Если читателю ранее не доводилось встречаться с Rails, есть [добротное пошаговое руководство](http://ruby.railstutorial.org/ruby-on-rails-tutorial-book), достаточное для быстрого старта и понимания приведённого ниже материала.

Зададим маршрут в `app/config/routes.rb`:

```ruby
# routes.rb:
get 'articles/:slug' => 'articles#show'
```

Это указание на то, что при обращении к странице будет вызван метод `show` из контроллёра `articles_controller.rb`, отвечающего за вывод публикаций.

Перепроводим маршруты:

```console
$ rake routes
```

Далее обратимся к указанному выше контроллёру. Он содержит различные методы, оперирующие нашей моделью. В примере ниже находит публикацию по определённым параметрам.

```ruby
# articles_controller.rb`

def show
  @article=Article.find_by_slug!(params[:id])
end

private
  def article_params
    params.require(:article).permit(:title, :content, :slug)
  end
```

Собственно, модель. Здесь нас и поджидаем самое интересное. Перед тем, как публикация будет записана в БД, создаётся поле `slug`. Для указания этого действия мы определяем `before_create`, в который передаём название функции &mdash; `create_slug`.

Можно каждый раз при создании статьи назначать её `slug` вручную. Или же создавать это поле автоматически, исходя из названия статьи.

Если с английским языком всё более или менее понятно, то автоматический перевод с кириллицы на латиницу может совсем не радовать, поэтому в общем случае предлагается использовать первый вариант.

```ruby
# article.rb

class Article < ActiveRecord::Base
  before_create :create_slug

  default_scope order: 'articles.created_at DESC' # сортировка статей
  validates :slug, presence: true, length: {maximum:30} # валидация

  def to_param
    "#{slug}/".downcase # как выводить в URL
  end

  def create_slug
    # если в модели определено поле slug, slug задаётся вручную
    self.slug=self.slug.parameterize
    # если поле slug не определено, генерируется автоматически
    # исходя из значения поля title (заголовок статьи)
    # self.slug=self.title.parameterize
  end
end
```

Наконец, пример вывода страницы публикации.

```ruby
# show.html.erb

<% provide(:title, @article.title) %>
<h2><%= link_to @article.title, article_path(@article) %></h2>
<h5><%= @article.created_at.strftime("%d %B") %></h5>
<%= @article.content %>
```
