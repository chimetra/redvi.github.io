---
layout: post
title: Markdown и подсветка синтаксиса в Ruby On Rails
date: 2013-11-02 08:10
tags: [ruby]
slug: rails-markdown
author: redVi
summary: "О том, как заставить rails понимать markdown разметку и подсветку синтаксиса."
---

При написании статей уже давно не принято использовать простую HTML-разметку. Набирать каждый раз HTML-теги вручную &mdash; не самое приятное времяпрепровождение. Зачастую для этих целей используются user-friendly редакторы а-ля TinyMCE. И выглядят неплохо, и справиться с ними в силах любой необременённый излишками знания пользователь. Минус один: html-разметка, получаемая на выходе, может совсем не радовать глаз автора и мохнатые лапки поисковых &laquo;пауков&raquo;.

По другую сторону стоя&#x301;т облегчённые языки разметки, самым популярным из которых является markdown. Вот его-то мы и будем подключать к Rails-проекту.

Для начала установим необходимые гемы. Для этого их следует прописать в Gemfile:

```ruby
# Gemfile

gem 'redcarpet', '~> 3.0.0'
gem 'pygments.rb'
```

И дать команду:

```console
$ bundle install
```

После чего обратимся к созданию helper'а, призванного сгенерировать html из файла с разметкой markdown. За генерацию страниц в html из markdown в ответе `redcarpet`. К тому же благодаря `pygments.rb` у нас появляется возможность подсветки синтаксиса в коде.

```ruby
# helpers/application_helper.rb

module ApplicationHelper

  class HTMLwithPygments < Redcarpet::Render::HTML
    require 'pygments.rb'
    def block_code(code, language)
      Pygments.highlight(code, :lexer => language)
    end
  end

  def markdown(text, options = {})
    renderer = HTMLwithPygments.new(hard_wrap: true)
    options={
      autolink: true,
      no_intra_emphasis: true,
      fenced_code_blocks: true,
      lax_html_blocks: true,
      strikethrough: true,
      superscript: true,
      space_after_headers: true,
      underline: true,
      highlight: true,
      quote: true
    }
    Redcarpet::Markdown.new(renderer, options).render(text).html_safe
  end
end
```

Для подсветки синтаксиса нужно написать блок кода и указать необходимый ЯП, вот так:

<pre><code>
~~~ruby
puts "Hello!"
~~~
</code></pre>

Функция `markdown` принимает на вход текст с указанными опциями и генерирует html-страницу. Подробно об имеющихся опциях и их значении можно прочесть на [странице проекта](https://github.com/vmg/redcarpet).

Осталось лишь вывести наш текст на обозрение массам:

```css+erb
<%# posts/show.html.erb %>

<%= link_to @post.title, post_path(@post) %>
  <%= markdown @post.content %>
```

С этим способом в базе данных текст хранится в формате markdown, а перед тем, как страница будет отображена, `redcarpet` переводит её в html-формат. С точки зрения производительности не самый лучший вариант.

Но есть и другой способ: сгенерировать html перед тем, как сохранять файл в базу данных при помощи `before_save`.

```ruby
# post.rb
#
# Table name: posts
#
#  id         :integer     not null, primary key
#  title      :string(255)
#  content    :text
#  slug       :string(255)
#  summary    :string(255)
#  created_at :datetime
#  updated_at :datetime

class Post < ActiveRecord::Base
  before_save :render_content

  def render_content
    require 'redcarpet'
    renderer = HTMLwithPygments
    extensions = {fenced_code_blocks: true}
    redcarpet = Redcarpet::Markdown.new(renderer, extensions)
    self.content = redcarpet.render self.content
  end
  class HTMLwithPygments < Redcarpet::Render::HTML
    require 'pygments.rb'
    def block_code(code, language)
      Pygments.highlight(code, :lexer => language)
    end
  end
end
```

Если ресурс не относится к техническим и статья не предназначена для вывода блоков кода можно обойтись без `pygments`:

```ruby
# post.rb

class Post < ActiveRecord::Base
  before_save :render_content

  def render_content
    require 'redcarpet'
    renderer = Redcarpet::Render::HTML.new
    extensions = {fenced_code_blocks: true}
    redcarpet = Redcarpet::Markdown.new(renderer, extensions)
    self.content = redcarpet.render self.content
  end
end
```

Теперь в базе будет лежать готовая html-страница.

Для корректного вывода такой странички нам нужно использовать стандартный фильтр `html_safe`:

```css+erb
<%# posts/show.html.erb %>

<%= link_to @post.title, post_path(@post) %>
  <%= @post.content.html_safe %>
```

Ещё раз: в первом примере (при генерации &laquo;на лету&raquo;) страница сохраняется в формате markdown, каждый раз перед тем как вывести её содержимое `redcarpet` генерирует текст из markdown в html.

Во втором примере отображается предварительно сгенерированный html-код. Так что вы вольны выбирать, какой из вариантов удобнее в каждом конкретном случае.
