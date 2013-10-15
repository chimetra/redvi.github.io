Title: Nginx как самостоятельный веб-сервер
Date: 2012-11-06 08:15
Tags: Arch, Server, Linux
Slug: nginx
Author: redVi
Summary: В этот раз будет затронут вопрос установки и настройки сервера nginx не как дополнение к apache, а абсолютно отдельно от последнего.

Пост в продолжение цикла о веб-серверах. В этот раз будет затронут вопрос установки и настройки сервера nginx не как дополнение к apache, а абсолютно отдельно от последнего.
Если вас также интересует настройка apache под различными операционными системами, возможно, вам пригодятся данные ниже ссылки:

- [Apache + Archlinux](http://www.unix-lab.org/posts/lamp/)
- [Apache + Windows](http://www.unix-lab.org/posts/apache-php-mysql/)


<b>Немного предыстории:</b>

Nginx (энджин-экс) был разработан нашим соотечественником Игорем Сысоевым, первый релиз увидел свет осенью 2004 года. Nginx - это HTTP-сервер и обратный прокси-сервер, а также почтовый прокси-сервер. Чаще всего используется в дополнение к apache для снижения нагрузки на веб-серверах. Хотя вполне может использоваться и без "индейца" в случаях с высоконагруженными либо ресурсодефицитными серверами, куда поставить Apache не является возможным.

<b>Начнём:</b>

## Установка необходимых компонентов

```
:::console
$ sudo pacman -S php mysql nginx php-fpm
```

Управление запуском веб-сервера производится следующими командами:

```console
# rc.d start nginx
# rc.d stop nginx
# rc.d restart nginx
```

Старт, останов и перезапуск соответственно.

Директория по умолчанию для файлов сайта - `/usr/share/nginx/http/`

Мы же будем использовать стандартную директорию archlinux - `/srv/http`.

<b>Примечание:</b> в других дистрибутивах пути к файлам и директориям могут отличаться. Например в Debian/ubuntu стандартный каталог веб-сервера - `/var/www`.

Для запуска при загрузке системы следует добавить nginx как демон в `rc.conf`:

```
DAEMONS=( ... nginx...)
```

![welcome](http://1.bp.blogspot.com/-S7bhIrt0__E/UGbNvUV81fI/AAAAAAAABpI/mbbjE8xg9ZE/s1600/nginx.png)

## Главный конфигурационный файл

Находится по пути `/etc/nginx/nginx.conf`

Открываем любимым текстовым редактором и правим в соответствии с нуждами:

    #user html;
    # количество запускаемых рабочих процессов Nginx:
    worker_processes  1;

    # местоположение файла протокола ошибок работы сервера и уровень их важности
    # уровень серьёзности в порядке увеличения:
    # debug, info, notice, warn, error, crit
    #error_log  logs/error.log;
    #error_log  logs/error.log  notice;
    #error_log  logs/error.log  info;

    # местоположение файла, содержащего идентификатор процесса запущенного
    # сервера
    #pid        logs/nginx.pid;


    # подведение Nginx относительно сетевых соединений
    # значение worker_connections, помноженное на значение worker_processes,
    # определяет максимально возможное количество одновременных соединений к
    # серверу
    events {
        worker_connections  1024;
    }


    # default_type - MIME-тип по умолчанию, коорый будет передавать сервер клиенту,
    # если этот тип не удалось определить
    http {
        include       mime.types;
        default_type  application/octet-stream;

        #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
        #                  '$status $body_bytes_sent "$http_referer" '
        #                  '"$http_user_agent" "$http_x_forwarded_for"';

    # accsess_log определяет местоположение и формат лог-файла
        #access_log  logs/access.log  main;

    # включает или отключает использование сервером sendfile,
    # увеличивает производительность
        sendfile        on;
        #tcp_nopush     on;

    # время, в течение которого Nginx будет держать открытым постоянное соединение
        #keepalive_timeout  0;
        keepalive_timeout  65;

    # управление gzip-сжатием
        #gzip  on;

    # Начало блока SERVER!
    # слушать 80 порт, имя сервера - localhost
        server {
            listen       80;
            server_name  localhost;
            root    /srv/http;

    # управление кодировкой
            # charset koi8-r;

    # логи доступа, скажем так
            #access_log  logs/host.access.log  main;

    # определение формата файлов
    # определение корня сайта
            location / {
                root   /srv/http;
                index index.php index.html index.htm ;
            }

    # расположение 404 страницы (not found)
    # создать её придётся самим
            error_page  404              /404.html;

    # настройка сраниц ошибок 50x (ошибки сервера)
    # в примере они лежат в директории errors
            # redirect server error pages to the static page /50x.html
            #
            error_page   500 502 503 504  /50x.html;
            location = /50x.html {
                root   /srv/http/errors;
            }

            # proxy the PHP scripts to Apache listening on 127.0.0.1:80
            #
            #location ~ \.php$ {
            #    proxy_pass   http://127.0.0.1;
            #}

    # Для обработки php-файлов посредством FastCGI
            # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
            #
            location ~ \.(php|html)$ {
                root           /srv/http;
                #fastcgi_pass   127.0.0.1:9000;
                fastcgi_index  index.php;
                fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
                include        fastcgi_params; fastcgi_param QUERY_STRING $query_string;

            }

    # настройка доступа к файлу .htaccess
            # deny access to .htaccess files, if Apache's document root
            # concurs with nginx's one
            #
            #location ~ /\.ht {
            #    deny  all;
            #}
        }


    # Настройка виртуального сервера
        # another virtual host using mix of IP-, name-, and port-based configuration
        #
        #server {
        #    listen       8000;
        #    listen       somename:8080;
        #    server_name  somename  alias  another.alias;

        #    location / {
        #        root   html;
        #        index  index.html index.htm;
        #    }
        #}


        # HTTPS server
        #
        #server {
        #    listen       443;
        #    server_name  localhost;

        #    ssl                  on;
        #    ssl_certificate      cert.pem;
        #    ssl_certificate_key  cert.key;

        #    ssl_session_timeout  5m;

        #    ssl_protocols  SSLv2 SSLv3 TLSv1;
        #    ssl_ciphers  HIGH:!aNULL:!MD5;
        #    ssl_prefer_server_ciphers   on;

        #    location / {
        #        root   html;
        #        index  index.html index.htm;
        #    }
        #}

    }


## Что ещё?

Для корректной обработки php-файлов также может понадобиться внести изменения в `php.ini`:

```
# /etc/php/php.ini
cgi.fix_pathinfo = 1
```

И обязательно в конфигурационный файл `/etc/php/php-fpm.conf` добавить строку:

```
security.limit_extensions = .php .html
```

Это для того, чтобы .php-код обрабатывался в файлах `*.html`

После внесённых изменений перезапустить `nginx` и `php-fpm` и проверить на работоспособность, закинув в корневую директорию сайта файл `phpinfo.php` подобного содержания:

```
<?php
    phpinfo();
?>
```

Смотрим:

![cgi](http://2.bp.blogspot.com/-Q9s7HKDkWn8/UGZ5ByJXZSI/AAAAAAAABmY/8dVYqTfzu4s/s1600/php-fpm.png)

Возможно, в следующих постах будет рассмотрена настройка django в nginx, а также настройка виртуальных хостов. Но это позже, а пока прощаюсь.
