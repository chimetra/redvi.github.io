---
layout: post
title: Установка СУБД MySQL. Вручную
date: 2012-06-03 08:25
tags: [server, windows]
slug: mysql-install
author: redVi
summary: Пост о настройке MySQL вручную для тех, у кого по каким-то причинам корректно не сработал инсталлятор.
---

Как было обещано ранее в статье [о настройке веб-сервера](http://www.unix-lab.org/posts/apache-php-mysql/), выкладываю пост о настройке MySQL вручную для тех, у кого по каким-то причинам корректно не сработал инсталлятор.

Как всегда начнём с того, что достанм необходимую программу. На этот раз будем качать архив вместо установщика: <http://www.mysql.com/downloads/mysql/>

Займёмся созданием необходимых папок. Как правило по пути `C:\Program Files\MySQL\MySQL Server 5.5`. То есть папку MySQL и вложенную MySQL Server 5.5. Распаковываем в нее содержимое архива.

![mysql-unzip](http://3.bp.blogspot.com/-9pzii_egztA/T8EE8exZSrI/AAAAAAAAAps/uPmJ4PWHgaI/s1600/mysql-unzip.png "MySQL unzip")

Далее нам понадобится файл конфигурации. Что брать за образец, решать вам.

· `my-small.ini` — MySQL используется нечасто, сервер БД не потребляет много ресурсов.

· `my-medium.ini` — MySQL используется на постоянной основе, например, как в нашем случае, для работы с домашним веб-сервером

· `my-large.ini` и `my-huge.ini` — для систем, использующихся как выделенный MySQL сервер. `My-large.ini` можно использовать и для домашнего сервера, если нужна дополнительная производительность.

· `my-innodb-heavy-4G` — для выделенных серверов, имеющих от 4 Гб оперативной памяти и использующих только таблицы типа InnoDB.

Берём какой-то из этих файлов конфигурации,  переименовываем его в `my.ini`.

Открываем в текстовом редакторе и дописываем после `[mysqld]` строки:

```
basedir=C:/Program Files/MySQL/MySQL Server 5.5
datadir=C:/Program Files/MySQL/MySQL Server 5.5/data
```

Добавляем путь `C:\Program Files\MySQL\MySQL Server 5.5\bin` в переменную среды `PATH`.

Для этого Правой кнопкой на Мой компьютер - Свойства - Дополнительные параметры системы - Переменные среды. Ищем `Path`, жмём изменить, дописываем в самый конец, не забыв поставить `;` в самом начале, то есть примерно так:

`C:\Program Files\WIDCOMM\Bluetooth Software\syswow64;C:\Program Files\MySQL\MySQL Server 5.5\bin`

![path](http://3.bp.blogspot.com/-6q49izdhLnU/T8EFU6p_aqI/AAAAAAAAAp0/25mbr4sHAXQ/s1600/path.png "path")

<b>ВНИМАНИЕ!</b> Входящий порт TCP 3306 должен быть открыт. Либо разрешён в брандмауэре Windows, либо в используемой вами антивирусной программе (как правило эти полномочия сейчас берёт на себя именно такое ПО).

![TCP](http://4.bp.blogspot.com/-syJI8ByzFhk/T8EFdAKjJjI/AAAAAAAAAp8/WFcQk3PbcZ8/s1600/mysqld-3306.png "TCP")

Открываем командную строку от имени администратора, пишем `mysqld --console`

При успешном запуске службы в конце вы увидите:

```
Version: '5.5.9-log'  socket: ''  port: 3306  MySQL Community Server (GPL)
```

![run server](http://2.bp.blogspot.com/-yqydVKOa1P8/T8EFmPYUAhI/AAAAAAAAAqE/iAUjw-4inyQ/s1600/mysqld-run.png "run server")

Открываем ещё одну копию командной строки, не закрывая существующую, пишем:

```
mysql -u root
```

Видим приглашение командной строки MySQL.

Смотрим, какие имеются базы данных на текущий момент, пишем:

```
show databases;
```

![databases](http://4.bp.blogspot.com/-pD7Lw38A9PE/T8EFxH5yH1I/AAAAAAAAAqM/dEBS0ZYLQrU/s1600/mysqld-databases.png "databases")

Теперь установим пароль root'а для доступа к БД.

```
use mysql
UPDATE user SET password = PASSWORD('ваш_пароль') WHERE user = 'root';
```

Проверяем, всё ли в порядке:

```
SELECT user, host, password FROM user;
```

Выходим:

```
FLUSH PRIVILEGES;
exit;
```

Мы добились того, что вход осуществляется только с паролем:

```
mysql -u root -p
```

Отключим службу:

```
mysqladmin -u root -p shutdown
```

И, наконец, сделаем так, чтобы MySQL была в службах Windows, в командной строке пишем:

```
"C:\Program Files\MySQL\MySQL Server 5.5\bin\mysqld" --install
```

Идём с лужбы: панель управления - Система и безопасность - Администрирование - Службы. Находим MySQL. Можно запускать, в службах всё появилось.

![MySQL services](http://2.bp.blogspot.com/-Fvk1ZIMG2zs/T8EGPoveVtI/AAAAAAAAAqU/QCYGg2BY8vU/s1600/mysql-services.png "MySQL services")

Удобнее запускать и останавливать MySQL посредством командной строки:

```
net start mysql - старт
net stop mysql - останов
```

Для удаления службы, если это будет нужно:

```
"C:\Program Files\MySQL\MySQL Server 5.5\bin\mysqld" --remove
```
