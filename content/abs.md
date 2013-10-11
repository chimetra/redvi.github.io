Title: Знакомимся с ABS
Date: 2012-01-11 08:25
Tags: Arch, Kernel, Linux
Slug: abs
Author: redVi
Summary: Сегодня будем доказывать, что arch linux ничем не хуже gentoo.

Сегодня будем доказывать, что arch linux ничем не хуже gentoo. Главная
особенность gentoo что? Правильно, порты, система портежей (вроде бы сделанная по образу и подобию портов FreeBSD, если нет, поправьте меня). Что ж, и мы не обделены.

Многие, вероятно, уже догадались, о чём пойдёт речь. Для тех же, кто этого ещё не понял &mdash; знакомьтесь &mdash; ABS.

ABS &mdash; Arch Building System &mdash; система построения пакетов в Arch Linux. Цель &mdash; создание автономного пакета из исходников для последующей установки при помощи пакетного менеджера pacman.

Создание пакета для Arch начинается с написания файла `PKGBUILD`. Это просто Bash-скрипт, содержащий:

- название пакета, номер версии и прочую информацию такого рода.
- инструкции для скачивания, компиляции и установки программного пакета.

Готовый файл `PKGBUILD` используется программой `makepkg`, которая следует описанным в нем инструкциям для правильного создания установочного бинарного пакета, имеющего расширение `.pkg.tar.gz`.

Получение ABS:

```console
# pacman -S abs
```
Синхронизация дерева ABS:

```console
# abs
```
Просто, не так ли? Дальше &mdash; интереснее.

Просмотрим, что находится в появившемся каталоге `abs`:

```console
$ ls /var/abs/

community
core
extra
local
multilib
multilib-staging
README
```
Здесь лежат каталоги, соответствующие группам пакетов Arch Linux. Зайдя в нужный подкаталог, мы можем скомпилировать из исходников какой-либо пакет, но об этом позже.

Что содержит конфигурационный файл abs:

```sh
# /etc/abs.conf
#

# the top-level directory of all your PKGBUILDs - корневая директория для abs
[ "$ABSROOT" = "" ] && ABSROOT="/var/abs/"

#
# Server to sync from - сервер синхронизации
#
SYNCSERVER="rsync.archlinux.org"

#
# The architecture to fetch abs for - архитектура при сборке пакета
# Either i686 or x86_64
#
ARCH="x86_64"

#
# Pacman mirror list used for syncing via tarball - список зеркал для
# синхронизации
#
MIRRORLIST="/etc/pacman.d/mirrorlist"
#
# REPOS to be parsed by abs (in this order) - удалите ! чтобы включить
#   (prefix a repo with a ! to disable it)
#
# Note: If a repo is removed, it is still fetched!
# Repos must be preceded with a ! to prevent fetching
#
REPOS=(core extra community multilib !testing !community-testing
!multilib-testing
    !staging !community-staging !gnome-unstable !kde-unstable)
```


После сборки пакета, можно очистить кеш pacman'а. Для очистки кеша существует команда `pacman -Scc`. Лучше сначала просмотреть, от чего мы собираемся избавиться:

```console
$ ls /var/cache/pacman/pkg
```
Давайте уже приступим. Например, захотелось нам установить из исходников openbox. Посмотрим, есть ли он:

```console
$ ls /var/abs/community|grep openbox
openbox
openbox-themes
$ cd /var/abs/community/openbox
$ sudo makepkg --asroot
```

Openbox найден. Далее выполнен вход в соответствующую директорию и дана команда сборки пакета. Поскольку, работая от обычного пользователя, собирать пакеты в системных директориях мы не вправе, а сборку от рута нам провести не дадут, выдав устрашающее предупреждение о том, как это небезопасно... В общем, пишем то, что написали: `--asroot`

Что будет?

Умная система проверит наличие исходников и при необходимости скачает их, проверит зависимости, соберёт пакет, да ещё и почистит за собой.

После вышеописанных действий мы получим в той же директории установочный пакет, который, собственно, и установим командой:

```console
$ sudo pacman -U имя_пакета.pkg.tar.xz
```

В названии будет указано имя пакета, версия и наша архитектура, вот так:

```
openbox-3.5.0-4-x86_64.pkg.tar.xz
```

А если мы хотим собрать ядро?

```console
$ ls /var/abs/core/linux
change-default-console-loglevel.patch  CVE-2012-0056.patch
linux.install
config                 i915-fix-ghost-tv-output.patch
linux.preset
config.x86_64          i915-gpu-finish.patch   PKGBUILD
```

Вы можете открыть редактором файл `PKGBUILD` и, например, раскомментировать строку `"make menuconfig"`, что даст возможность внести изменения перед сборкой ядра.

Что ж, принцип поиска и сборки пакетов, думаю, ясен.

Что ещё можно использовать?

```console
$ sudo vim /etc/makepkg.conf:
CFLAGS="-march=x86-64 -mtune=generic -O2 -pipe -fstack-protector
--param=ssp-buffer-size=4 -D_FORTIF    Y_SOURCE=2"
CXXFLAGS="-march=x86-64 -mtune=generic -O2 -pipe -fstack-protector
--param=ssp-buffer-size=4 -D_FORT    IFY_SOURCE=2"
LDFLAGS="-Wl,-O1,--sort-common,--as-needed,-z,relro,--hash-style=gnu"
#-- Make Flags: change this for DistCC/SMP systems
MAKEFLAGS="-j2
```

Для более быстрой сборки раскомментируйте `MAKEFLAGS` и установите подходящее вам значение. Рекомендуемое значение = число ядер процессора+1. Но никто не мешает найти оптимальное значение опытным путём.

Здесь можно заметить сходство с портежами gentoo, хотя нет главного &mdash; USE-флагов. Так что, если вам хочется настроить свои флаги, делать это придётся для каждого пакета отдельно при помощи правки build-файла пакета. Безусловно, это неудобно. Но если нужно просто собрать программу из исходников &mdash; самое оно.
Кроме того, предусмотрено создание своего порта. Для этого выделена директория `/var/abs/local/` - свои эксперименты проводим там. Коротко о том, как это будет выглядеть. Нужно скопировать `PKGBUILD` желаемого пакета в нашу локальную директорию для экспериментов и... сделать как захочется.

```console
$ cp /var/abs/community/nginx/PKGBUILD /var/abs/local/
```

Файл `PKGBUILD` в этом посте разбираться не будет, о нём вы можете найти подробную инструкцию в официальной документации. Хотя не исключаю, что данный материал когда-то будет дополнен. Когда времени будет больше. А пока у меня всё.

