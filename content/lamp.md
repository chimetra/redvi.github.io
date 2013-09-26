Title: Установка LAMP в archlinux
Date: 2012-01-21 08:25
Tags: Arch, Server, Linux
Slug: lamp
Author: redVi
Summary: Apache – это самый популярный веб-сервер. Его задача как и любого другого веб-сервера – отдавать контент на запросы клиентов.

Apache &mdash; это самый популярный веб-сервер. Его задача как и любого другого
веб-сервера &mdash; отдавать контент на запросы клиентов. Apache обладает
большим функционалом за счет подключаемых модулей.


##Установка

    :::console
    $ sudo pacman -S apache php php-apache mysql

Это наиболее популярный вариант установки. Таким образом мы получим небезызвестный LAMP &mdash; Linux + Apache + MySQL + PHP

Если вы не нуждаетесь в каком-либо из компонентов, не ставьте его.

Не забудьте установить пароль для пользователя MySQL. Для этого необходимо запустить сервер командой `/etc/rc.d/httpd start`, а затем выполнить следующее:

    :::console
    $ /usr/bin/mysqladmin -u root password новый_пароль
    $ /usr/bin/mysqladmin -u root -h linux password новый_пароль

Теперь если вы попробуете зайти без пароля, у вас ничего не выйдет:

    :::console
    $ sudo mysql -u root
    ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)

Входим с паролем:

    :::console
    $sudo mysql -u root -p

В ответ на это вам предложат ввести заданный пароль.

Можете воспользоваться альтернативным методом, запустив:

    :::console
    $ /usr/bin/mysql_secure_installation

Теперь проверим, есть ли в `/etc/shadow` пользователь `http`:

    :::console
    # cat /etc/shadow :
    http:x:14871::::::

Если такой строки вами найдено не было, добавляем пользователя вручную:

    :::console
    # useradd -d /srv/http -r -s /bin/false -U http

Смотрим содержание нашего `/etc/hosts`:

    :::sh
    # /etc/hosts: static lookup table for host names
    #
    #<ip-address> <hostname.domain.org> <hostname>
    127.0.0.1 localhost.localdomain localhost linux

Примечание: здесь и далее `linux` - имя хоста, т.е. вашей машины

Так должен выглядеть `/etc/rc.conf`:


    # --------------------------------------
    # NETWORKING
    # --------------------------------------
    #
    # HOSTNAME: Hostname of machine. Should also be put in /etc/hosts
    #
    HOSTNAME="linux"

Итак, если вы ещё не запустили Apache, пришло время сделать это:

    :::console
    # /etc/rc.d/httpd start

Проверим его работоспособность, пройдя по ссылке в браузере: `http://localhost/`
Если всё нормально, вы увидите следующее изображение:

![localhost](http://3.bp.blogspot.com/-wrcyniFvt0o/TwBDrvF4tfI/AAAAAAAAAeU/jQuqE1PbVbw/s1600/apache2.png)

Если веб-сервер не запустился, тестируем настройку:

    :::console
    # apachectl configtest

##Что делать с PHP?

Добавьте  в `/etc/httpd/conf/httpd.conf`  в секцию `DefaultType text/plain`:

    LoadModule php5_module modules/libphp5.so
    Include conf/extra/php5_module.conf

Для того чтобы обрабатывались `*.php` файлы:

    AddType application/x-httpd-php .php
    AddType application/x-httpd-php-source .phps

Чтобы  php код обрабатывался в файлах `*.html`:

    AddType application/x-httpd-php .html
    AddType application/x-httpd-php .htm

После чего понадобится перезапустить веб-сервер:

    :::console
    # /etc/rc.d/httpd restart

Посмотреть корневую директорию сервера можно в этом же файле. Выглядит так:

    DocumentRoot "/srv/http"

Здесь же можно затронуть файл `/etc/php/php.ini`:

Нам важно знать путь к корневой директории. По умолчанию нужная строка выглядит так:

    open_basedir = /srv/http/:/home/:/tmp/:/usr/share/pear/

Что ж, теперь проверим отображение php-файлов. Пишем простую страничку примерно такого содержания:

    <html>
    <head>
    <title>PHP</title>
    </head>

    <body>
    My test page
    <?php
      phpinfo();
    ?>
    </p>
    </body>
    </html>

Так, в заголовке должно быть отображено название документа - PHP, в теле текст "My test page" и, если работает php, при помощи функции `phpinfo()` будет выведена его служебная информация.

Сохраните этот документ под именем `page.php` и сохраните в `/srv/http/` , то есть в корневую директорию сервера. Разумеется, у вас могут быть свои настройки. Чтобы протестировать следует зайти на страницу:

    http://localhost/page.php

Вот что вы должны увидеть:

![php](http://3.bp.blogspot.com/-vHPxeFERVbY/TwGCCASgxxI/AAAAAAAAAeg/sGxJERM4BAo/s1600/apache_php.png)

##MySQL

Для поддержки MySQL в  `/etc/php/php.ini`  раскомментируйте следующие строку:

    ;extension=mysql.so

Для настройки вашей системы выполните `/etc/rc.d/mysqld start`.

Убедитесь, что группа и пользователь `mysql` существуют. Если нет, добавьте их вручную:

    :::console
    # groupadd -g 89 mysql
    # useradd -u 89 -g mysql -d /var/lib/mysql -s /bin/false mysql

Измените владельца корневой директории MYSQL:

    :::console
    # chown -R mysql:mysql /var/lib/mysql

###Установка базы данных

Если вы хотите запускать mysql от имени суперпользователя, можете не применять опцию `--user` и не изменять владельца

    :::console
    # mysql_install_db --datadir=/var/lib/mysql --user=mysql
    # chown -R mysql:mysql /var/lib/mysql

Для запуска MySQL:

    :::console
    # /etc/rc.d/mysqld start

Тестируем mysql (как root):

    :::console
    # mysql

Задать пароль для mysql :

    :::console
    # mysqladmin -u root password 'пароль_root'

Для входа в mysql:

    :::console
    # mysql -u root -h linux -p

где linux - не забывайте! - имя вашего хоста.

##Установка phpMyAdmin (не бязательно)

Следует установить нужные пакеты:

    :::console
     $ sudo pacman -S php-mcrypt phpmyadmin

И исправить несколько файлов как указано ниже.

    :::console
    $ sudo rm -r /srv/http/phpMyAdmin - в случае, если phpmyadmin уже был установлен ранее
    $ sudo cp /etc/webapps/phpmyadmin/apache.example.conf /etc/httpd/conf/extra/httpd-phpmyadmin.conf - скопируем "образцовый" файл настроек

Отредактируем файлы `/etc/httpd/conf/httpd.conf` и `/etc/webapps/phpmyadmin/.htaccess`

    :::sh
    # httpd.conf
    #
    # phpMyAdmin configuration
    Include conf/extra/httpd-phpmyadmin.conf

    # /etc/webapps/phpmyadmin/.htaccess
    # deny from all

Теперь, перезагрузив наш `httpd`, можно войти в `phpmyadmin` по адресу `http://localhost/phpmyadmin`:

![phpmyadmin](http://4.bp.blogspot.com/-iWb_bAkGXQE/T0SrxOEJbFI/AAAAAAAAAik/N70gh7PPzhk/s1600/phpmyadmin.png)

Примечание: для запуска Apache и MySQL при старте системы, добавьте в `/etc/rc.conf` в секцию `DAMONS` соответствующие службы, вот так:

    DAEMONS=(...... httpd mysqld)

