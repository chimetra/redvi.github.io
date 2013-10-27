---
layout: post
title: Установка PHPMyAdmin
date: 2012-06-16 08:25
tags: [server, windows]
slug: phpmyadmin
author: redVi
summary: Установка PHPMyAdmin на Windows
---

Что ж, [в предыдущем посте](http://www.unix-lab.org/posts/apache-php-mysql/) мы благополучно установили веб-сервер Apache, php, MySQL... Но с базами данных намного удобнее работать при помощи `PHPMyAdmin`. Давайте его установим.

Идём по адресу <http://www.phpmyadmin.net/home_page/downloads.php>, скачиваем архив. Желательно выбирать мультиязычный, где уже имеется русский. На родном языке всегда лучше.

Предварительно создаём папку pma и распаковываем архив по адресу, где живёт наш веб-сервер. В моём случае это `C:\Program Files (x86)\Apache Software Foundation\Apache2.2\htdocs`.

Приглядимся внимательно и обнаружим файл с говорящим названием `config.sample.inc.php`. Копируем его и сохраняем как `config.inc.php`. Теперь, если возникнет такая нужда, мы сможем редактировать этот файл конфигурации как душе угодно, но... Не пугайтесь, сейчас делать этого нам даже не придётся.

Хотя следует проверить настройки конфигурации PHP в `php.ini`:

```apache
extension=mysql.so
extension=mysqli.so
```

И, если вдруг возникнут проблемы, конфигурацию веб-сервера в `httpd.conf`:

Добавить в блок начинающийся строкой:

```apache
<IfModule alias_module>
```

Следующее:

```apache
Alias /phpmyadmin "C:\Program Files (x86)\Apache Software Foundation\Apache2.2\htdocs\pma"
```

Всё. Заходим <htttp://localhost/pma/index.php>

![phpmyadmin](http://3.bp.blogspot.com/-DecanRKA5bQ/T8JMELatxAI/AAAAAAAAAq8/kgKDLHRk-NY/s1600/phpmyadmin.png "phpmyadmin")

Вспоминаем пароль пользователя root, входим под этой учётной записью. Можно создавать свои базы данных и заполнять их содержимым.

![bd](http://4.bp.blogspot.com/-wkDN-gylCgs/T8JMT_El6II/AAAAAAAAArE/fLHjXx9SvYY/s1600/bd.png "base")

