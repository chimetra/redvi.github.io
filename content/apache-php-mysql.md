Title: Apache+PHP+MySQL под Windows
Date: 2012-05-26 08:25
Tags: Server, Windows
Slug: apache-php-mysql
Author: redVi
Summary: Настройка Apache, PHP и MySQL под Windows.

Тему о веб-серверах после опубликованных постов, где производилась установка [LAMP на ArchLinux](lamp.html), приводились [настройки Nginx](nginx.html) и прочее, хотелось закрыть. Но, как оказалось, не все хотят пользоваться готовыми пакетами, где кто-то уже сделал настройки по-своему, решил за вас. Что ж, поскольку есть спрос на данную тему, а инструкций по установке всего этого комплекта 3 в одном мало или же нет вовсе, посвятим сему сегодняшний пост.

## Apache

Скачивается с сайта: <apache.org>

![apache](http://4.bp.blogspot.com/-WQR3jhVhuFQ/T8DXh8wJYrI/AAAAAAAAAng/Y8V2Ig5FcfA/s1600/apache+org.png "apache")

Установка проста до безобразия. Запускаем инсталлятор, везде жмём "Next", призадумываемся, увидев строки, где нужно вписать имя домена и т.п. Пишем банальное "localhost" и при желании свой e-mail для уведомлений.

![http](http://4.bp.blogspot.com/-a7QNRFLH0SY/T8DXuB9qNQI/AAAAAAAAAno/zVe5eCNqmlc/s1600/apache.png "http")

Как ни в чём ни бывало продолжаем установку. В финале жмём "Finish"

![finish](http://4.bp.blogspot.com/-fIr5gxtMcno/T8DYQPR2aCI/AAAAAAAAAnw/esNWCZX-6PY/s1600/apache-install2.png "finish")

После успешной установки в трее появится служба, с помощью которой можно запустить/перезапустить/остановить веб-сервер. Для этого кликаем левой кнопкой мыши и, собственно, выбираем необходимое действо. Нажатие правой кнопкой позволит перейти к сервису Apache или же отключить службу.
Доступ к службам можно получить иначе:

```
Панель управления -> Система и безопасность -> Администрирование -> Службы
```

![service](http://4.bp.blogspot.com/-tSVUz_03dQw/T8DYYiPKvjI/AAAAAAAAAoA/5tSpYx9PDUw/s1600/apache-services.png "service")

Открываем любимый браузер, пишем в адресной строке <http://localhost> и видим в зависимости от версии продукта либо страницу как на изображении ниже, либо запись "It works!". И что бы это значило? Верно, значит мы всё сделали правильно.

![welcome](http://3.bp.blogspot.com/-h5dJPIxqJYE/T8DYfGYUaYI/AAAAAAAAAoI/1jCtpDVyn-o/s1600/apache+localhost4.png "welcome")

Посмотрим, что же нужно настроить в первую очередь.

Идём по пути `C:\Program Files (x86)\Apache Group\Apache2\conf` (или туда, где у вас установлен Apache и лежит файл `httpd.conf`). Открываем `httpd.conf`, находим строки "The following lines prevent .htaccess and .htpasswd files from being"

Под ними примерно такой код:

```apache
<Directory />
    Options FollowSymLinks
    AllowOverride None
</Directory>
```

`None` - изменить на `All`, это разрешит использование `.htaccess`, который в отличие от `httpd.conf` не требует перезапуска веб-сервера.

И, раз уж мы сюда зашли, давайте сразу подключим наш PHP, который сейчас будем устанавливать, дабы веб-сервер корректно обрабатывал файлы с расширением `.php` и наш код соответственно.

Итак, в том же `httpd.conf` находим строки `LoadModule` и где-нибудь ниже их дописываем:

```apache
#PHP
LoadModule php5_module "C:/php5/php5apache2_2.dll"
AddType application/x-httpd-php .php
AddType application/x-httpd-php-source .phps

AddType application/x-httpd-php .html
AddType application/x-httpd-php .htm
```

<b>ВНИМАНИЕ!</b> Путь `C:/php5/php5apache2_2.dll` указывает, что наш PHP будет находиться в папке `C:/php5`, учитываем это при установке. А вот какую версию php5apache подключать, зависит от того, какая версия apache у вас установлена. Чтобы не запутать читателя: Apache 2.2 - `php5apache2_2.dll`, Apache 2.3 - `php5apache2_3.dll`. Подключайте то, что необходимо вам.

## PHP

Далее идём на сайт <http://php.net/downloads.php> и скачиваем оттуда zip-архив с новой версией PHP.

Распаковываем, как условились, в `C:/php5`, предварительно создав папочку `php5`. Поскольку пути к PHP в Apache мы уже прописали, можно считать установку завершённой.  Кому нужен файл `php.ini` для тонкой настройки, идём в `C:/php5`, ищем `php.ini-development`, сохраняем его копию как `php.ini`.

Неплохо было бы сразу пройтись в `php.ini` и раскомментировать строки, начинающиеся с `;mysqli` и `musql`. То есть так:

```
было: ;mysqli
станет: mysqli
```

Проверим работоспособность PHP на нашем сервере. В корневой папке Apache есть ещё папка - `htdocs`. Нам туда. Заметили? Здесь лежит файл `index.html`, который показывал нам, что всё работает. Напишем пару строк кода на PHP и сохраним здесь же, только как `index.php`:

```html
<html>
<?php
  phpinfo()
?>
</html>
```

Переходим по адресу: <http://localhost/index/php>

![localhost](http://1.bp.blogspot.com/-4PYYfS0dyoY/T8DZvECRg-I/AAAAAAAAAoQ/jufK8sf65rU/s1600/index.png "localhost")

 Пока всё. Работоспособность нашего веб-сервера в связке с PHP не вызывает сомнений.

## MySQL

Идём на сайт <http://www.mysql.com/downloads/>, скеачиваем версию `MySQL Community Server`. Другие в данном случае не нужны.

Запускаем инсталлятор. Тип установки: `Typical`

![mysql](http://1.bp.blogspot.com/-QWjGO7pfuOk/T8DZ87-LBYI/AAAAAAAAAoY/acMquvuxA7A/s1600/mysql.png "MySQL")

Доходим до выбора типа конфигурации, выбираем расширенный:

![MySQL2](http://1.bp.blogspot.com/-c9NwybxAQDc/T8DaCXRDjpI/AAAAAAAAAog/FNKWO4i7gXA/s1600/mysql2.png "MySQL type")

Далее последует вопрос, для какой машины устанавливать. Выбираем машину разработчика:

![MySQL3](http://4.bp.blogspot.com/-5p2AqGkBbhs/T8DaINB0HfI/AAAAAAAAAoo/XLBycae4LUE/s1600/mysql3.png "MySQL mashine")

Языковая поддержка - мультиязычный:

![mysql4](http://4.bp.blogspot.com/-YwYLFpIO7mU/T8DaNqzyQDI/AAAAAAAAAow/0WY1CVK-EyM/s1600/mysql4.png "MySQL database")

Путь установки. По умолчанию, либо задайте свой:

![MySQL5](http://2.bp.blogspot.com/-mheaCYCJBWk/T8DaTHegUNI/AAAAAAAAAo4/s7QkWQbau2I/s1600/mysql5.png "MySQL path")

Количество подключений к серверу баз данных. По умолчанию предлагается 15-20, так и оставим:

![MySQL6](http://1.bp.blogspot.com/-7NhsyDlS6K4/T8DaYZ9gBiI/AAAAAAAAApA/gY6qbN61zoo/s1600/mysql6.png "MySQL approximate number")

Указание номера порта - стандартный - 3306, указание добавить исключение для брандмауэра и прочее:

![mysql7](http://4.bp.blogspot.com/-LWj8_7E0CR4/T8DaefSwxbI/AAAAAAAAApI/eKbzam4O2eg/s1600/mysql7.png "MySQL tcp")

Выбор языково поддержки. Убедитесь, что выставили кодировку utf-8 :

![mysql8](http://3.bp.blogspot.com/-LFgFUoV7qcs/T8DakR5t5RI/AAAAAAAAApQ/RvcaTSa120Y/s1600/mysql8.png "MySQL utf")

Установить как сервис Windows, запускать автоматически (впрочем, последнее решать вам):

![mysql9](http://4.bp.blogspot.com/-3Rfp5puQMDg/T8DapXrVwvI/AAAAAAAAApY/2Fs3PTKh-M0/s1600/mysql9.png "MySQL server")

Задать пароль для входа в БД:

![MySQL10](http://1.bp.blogspot.com/-I-A0-eoq67M/T8DavjC0_aI/AAAAAAAAApg/48u66lg_fqY/s1600/mysql10.png "MySQL server")

Готово. Позднее установим [phpmyadmin](phpmyadmin.html) и попробуем проделать [ручную установку СУБД MySQL](mysql-install.html) для тех, у кого зависает  инсталлятор. К несчастью, такое бывает.
