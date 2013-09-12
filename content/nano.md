Title: Подсветка в nano
Date: 2013-01-12 21:15
Tags: Editors
Slug: nano
Author: redVi
Summary: Включаем подсветку синтаксиса в редакторе nano

Всем известен простой текстовый редактор nano. Он поставляется как редактор по умолчанию в большинстве дистрибутивов linux и имеет огромное количество пользователей, пожалуй, больше, чем какой-либо другой редактор. Но зачастую в нём не хватает одной приятной мелочи &mdash; подсветки синтаксиса. Впрочем, это можно легко и быстро исправить.


Шаблоны с различной подсветкой находятся по пути `/usr/share/nano`. Что там удастся найти?

    :::console
    $ tree /usr/share/nano
    /usr/share/nano
    |-- asm.nanorc
    |-- awk.nanorc
    |-- cmake.nanorc
    |-- c.nanorc
    |-- css.nanorc
    |-- debian.nanorc
    |-- fortran.nanorc
    |-- gentoo.nanorc
    |-- groff.nanorc
    |-- html.nanorc
    |-- java.nanorc

Итак, в нашем распоряжении подсветка языков программирования c, python, php и java. Можно раскрасить html и css файлы и кое-что ещё. Не так уж много, но для дел насущных должно хватить.

Дело за малым: создать файл `.nanorc` в домашней директории и включить в него необходимые стили. Это может выглядеть так:

    :::console
    $ cat .nanorc
    include /usr/share/nano/makefile.nanorc
    include /usr/share/nano/python.nanorc
    include /usr/share/nano/xml.nanorc
    include /usr/share/nano/sh.nanorc
    include /usr/share/nano/cmake.nanorc
    include /usr/share/nano/css.nanorc
    include /usr/share/nano/html.nanorc
    include /usr/share/nano/patch.nanorc
    include /usr/share/nano/php.nanorc


Теперь посмотрим как отображается файл с одним из влюченных шаблонов.


![nano](http://4.bp.blogspot.com/-a3JjN___Tu8/UNqbqwdUHPI/AAAAAAAADKs/2qpwA559400/s1600/nano.png)


Не так уж плохо. По крайней мере, это гораздо удобнее, чем отсутствие подсветки как таковой. И &mdash; да &mdash; это всё, пользуемся.

