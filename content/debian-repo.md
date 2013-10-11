Title: Репозитории Debian Squeeze
Date: 2011-08-05 08:25
Tags: Debian, Linux
Slug: debian-repo
Author: redVi
Summary: Как известно, изначально в Debian Squeeze задействованы только репозитории security и main. Для домашнего использования маловато.

Как известно, изначально в Debian Squeeze задействованы только репозитории `security` и `main`. Для домашнего использования маловато. Хочется и к мультимедия иметь доступ, и любимые программы устанавливать, а они зачастую non-free. Добавим несколько интересных вещей для Squeeze, тем более, что для следюущего стабильного релиза - Wheezy - они, скорее всего тоже подойдут. Надо будет лишь вместо squeeze wheezy поставить. Конечно, пока это недоказанная гипотеза, но так было с lenny,поживём - увидим.


Добавляем репозитории:

```sh
# /etc/apt/sources.list
# /etc/apt/sources.list
#
# Main repo's
deb http://ftp.ru.debian.org/debian/ squeeze main contrib non-free
deb-src http://ftp.ru.debian.org/debian/ squeeze main
deb http://volatile.debian.org/debian-volatile squeeze/volatile main contrib non-free
deb-src http://volatile.debian.org/debian-volatile squeeze/volatile main contrib

# Multimedia
deb http://www.debian-multimedia.org stable main
deb ftp://ftp.debian-multimedia.org stable main
deb http://www.debian-multimedia.org testing main
deb ftp://ftp.debian-multimedia.org testing main

#Yandex
deb http://mirror.yandex.ru/debian squeeze main contrib non-free
deb http://mirror.yandex.ru/debian-multimedia/ squeeze main
deb http://ftp.debian.org/debian/ squeeze main

#Opera
deb http://deb.opera.com/opera/ squeeze non-free

#Wine
deb http://www.lamaresh.net/apt squeeze main

#VirtualBox
deb http://download.virtualbox.org/virtualbox/debian squeeze non-free

# Программы от Google
deb http://dl.google.com/linux/deb/ stable non-free

#Emacs
deb http://emacs.naquadah.org/ unstable/
#deb-src http://emacs.naquadah.org/ unstable/

#KDE 4 backports для Debian Lenny
#deb http://www.debian-desktop.org/pub/linux/debian/kde43 lenny-backports main contrib non.free
#deb-src http://www.debian-desktop.org/pub/linux/debian/kde43 lenny-backports main contrib non.free
#Testing!
#deb http://ftp.ru.debian.org/debian/dists/ testing contrib main non-free

#skype
deb http://download.skype.com/linux/repos/debian/ stable non-free
```

Сохраняем список нажатием клавиш `Ctrl+O`, выходим - `Ctrl+X`.
Обновляем наши записи:

```console
$ sudo aptitude update
```

Примечание для новоприбывших: закомментированные (#)строки игнорируются.
Данная статья, скорее всего, не будет обновляться, т.к. репозитории неизменны. Но могут измениться ключи. Список репозиториев может быть расширен. Поэтому обратите внимание на сайт [linuxoid](http://linuxoid.in/Полезные_репозитории_для_Debian).
