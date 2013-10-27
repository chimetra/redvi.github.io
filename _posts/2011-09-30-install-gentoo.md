---
layout: post
title: Установка Gentoo. По-русски
date: 2011-09-30 08:20
update: 2 января 2013
tags: [gentoo, linux]
slug: install-gentoo
author: redVi
summary: Сегодня будем развенчивать миф о сложности установки Gentoo.
---

Сегодня будем развенчивать миф о сложности установки Gentoo. Почему установка "по-русски"? Потому что настраивать станем русскую локаль, раскладку и временную зону. Статья получилась довольно объёмной, для тех, кто не знает, как скоротать долгий вечер).


### Загрузитесь с СD-диска.

Грузимся с параметрами по умолчанию.

![gentoo boot](http://1.bp.blogspot.com/-CNpKK24BMI0/ToWIXvl3XNI/AAAAAAAAAMQ/ucrOkjGKt5w/s1600/gentoo_boot.png)

### Настройка интернет-соединения:
автор использует модемное соединение, данные передаются автоматически при помощи DHCP.

```console
# /sbin/ifconfig
```

если кроме интерфейса lo больше ничего нет, значит делаем следующее:

```console
# dhcpcd eth0 (где ваш сетевой интерфейс - eth0)
```

после чего повторяем команду `/sbin/ifconfig`

теперь у нас появились данные интерфейса `eth0`.

Для настройки adsl-соединения:

```console
# pppoe-setup
# net-setup eth0 (для обычных или беспроводных сетей)
# ping ya.ru - пингуем яндекс
```

чтобы прервать пинги:

`Ctrl+C`

Интернет настроили, идём дальше

## Создание разделов диска

Для этого воспользуемся `cfdisk`:

перед тем,как создавать разделы,сядьте и подумайте какие,какого размера и с какой файловой системой.

- `/` - корневой каталог
- `/home` - директории пользователей
- `/boot` - загрузочные файлы
- `/usr` - пользовательские приложения.
- `/var` - изменяемые приложения, лучше не жадничать хотя бы потому,что там будут компилироваться наши пакеты
- `/opt` - большой размер нужен для игрового сервера

Лучше записать то, что вы себе насочиняли. Для домашнего использования можно обойтись стандартными каталогами `/boot`, `/` , `swap`.

### Непосредственно создание разделов:

```console
# cfdisk /dev/sda
```

где `sda` - SCSI-диск; `hda` - IDE-диск. Выбирайте что нужно вам.

- `news` - создание нового раздела
- `type` - выбор типа файловой системы (83 - Linux, 82 - `swap`)
- `bootable` - отметить как загрузочный (укажите для раздела,в который хотите смонтировать `/boot`!)
- `write` - записать изменения
- `delete` - удалить
- `quit` - выйти

![cfdisk](http://4.bp.blogspot.com/-DO3Qly4-DxU/ToWKYWy_xdI/AAAAAAAAAMU/MjAae-_QKKA/s1600/gentoo_cfdisk.png)

### Назначение файловой системы:

```console
# mke2fs /dev/sda1 - создание `ext2` на разделе `/dev/sda1`
# mke2fs -j /dev/sda3 - создание `ext3` на разделе `/dev/sda3`
# mkswap /dev/sda2 - создание раздела подкачки на `/dev/sda2`
# swapon /dev/sda2 - и его активация
# mkfs.ext4 - создание `ext4`, если не желаете использовать `ext3`
```

### Назначение точек монтирования:

```console
# mount /dev/sda3 /mnt/gentoo - монтируем корень
# mkdir /mnt/gentoo/boot - раздел под загрузчик
# mount /dev/sda1 /mnt/gentoo/boot - монтирование раздела загрузчика
```

## Архив стадии, дерево портежей

В качестве источника загрузки автором было использовано зеркало `mirror.yandex.ru`
Внимательно следите за тем,чтобы загрузить подходящий скачанному вами образу архив. В примере использован amd64.

```console
# cd /mnt/gentoo
# links http://mirror.yandex.ru/gentoo-distfiles/releases/amd64/current-stage3/
```

Выберите файл `stage*.tar.bz` и нажмите `enter`. Начнётся загрузка архива, это 161 Мб, так что пока можно попить кофейку.

![stage](http://2.bp.blogspot.com/-sQnGBlA-AFE/ToWKhbbfoMI/AAAAAAAAAMY/6G6peYvEpEo/s1600/gentoo2.png)

Загрузили? Распаковываем:

```console
# tar xvjpf stage3-*.tar.bz
```

Теперь сделаем снимок дерева портежей

```console
# links http://mirror.yandex.ru/gentoo-distfiles/snapshots/
```

выбираем внизу `portage-latest.tar.bz2`

Начнётся загрузка.

распаковываем (из корневого каталога):

```console
# tar xvjf /mnt/gentoo/portage-latest.tar.bz2 -C /mnt/gentoo/usr
```

## Настройка компиляции ядра

Настройки хранятся в файле `mnt/gentoo/etc/portage/make.conf`. Его и открываем любимым редактором (joe, nano, vi?)
Здесь используются переменные и значения. Пример:

переменная - `CHOST`, её значение - `x86_64-pc-linux-gnu` - указывает на архитектуру процессора
`CFLAGS="-march=k8 -pipe -O2"` - где

`"-march=k8"` - название целевой архитектуры, `k8` прописывается для amd64, `-О2` - классс оптимизации.

<b>Допустимые значения:</b>

- `-s` оптимизация по размеру
- `-0` без оптимизации
- `-1 -2 -3` - по скорости
- `CXXFLAGS="${CFLAGS}"` - не изменяйте её
- `MAKEOPTS="-j2"` - определяет сколько параллельных процессов компиляции можно запускать при установке пакета. Обычно ставят значение равное количеству ядер процессора +1. Если ваш процессор поддерживает технологию Hyper-threading, разумное значение будет: количество доступных ядер, умноженное на 2 +1.
USE-флаги. Можно пока ничего не дописывать, займётесь этим позже.

### Выбор зеркал, DNS, chroot

Действия в примере производятся из каталога `/`

Выбор зеркала загрузки

```console
# mirrorselect -i -o >> /mnt/gentoo/etc/portage/make.conf
```

Выбор зеркала rsync:

```console
# mirrorselect -i -r -o >> /mnt/gentoo/etc/portage/make.conf
```

Из предложенного списка выберите зеркала России.

![rsync](http://4.bp.blogspot.com/-IyJCfdryYVE/ToWK0dEumOI/AAAAAAAAAMc/7etuZEOxiaQ/s1600/gentoo4_rsync.png)

Нелишним будет скопировать информацию о DNS

```console
# cp -L /etc/resolv.conf /mnt/gentoo/etc/resolv.conf
```

Монтируем `/proc` & `/dev`:

```console
# mount -t proc none /mnt/gentoo/proc
# mount -o bind /dev /mnt/gentoo/dev
```

Переходим в новую среду с помощью `chroot`:

```console
# chroot /mnt/gentoo /bin/bash
# env-update
# source /etc/profile
# export PS1="(chroot) $PS1"
```

![chroot](http://4.bp.blogspot.com/-CsPH_FFvXKY/ToWK85b1e-I/AAAAAAAAAMg/VUTZVPeXNck/s1600/gentoo3_chroot1.png)

## Прочие премудрости

Обновите дерево портежей:

```console
# mkdir /usr/portage
# emerge --sync`
```

это может занять какое-то время, не пугайтесь

```console
# emerge portage - если выдаёт сообщение о новой версии портежей
```

Выбор профиля:

```console
# eselect profile list
Available profile symlink targets:
[1]   default/linux/amd64/10.0 *
[2]   default/linux/amd64/10.0/desktop
[3]   default/linux/amd64/10.0/server
# eselect profile set 3
```

Думаю, приведённые действия не нуждаются в пояснении, всё ясно из названий профилей. Нужно лишь выбрать необходимый вам, исходя из ваших задач.

### USE-флаги

Служат для включения/отключения поддержки необязательных функций при компиляции программ.
Вам не нужен X-сервер? Допишите значение `"-X"`. Не нужна поддержка qt? Значит `"-qt"`. И наоборот включите поддержку unicode: `"unicode"`.
Посмотреть допустимые значения:

```console
# less /usr/portage/profiles/use.desc
```

Значения дописываются в `/etc/portage/make.conf` в строку USE

```console
# nano -w /etc/portage/make.conf
```

Например:

![gentoo use](http://4.bp.blogspot.com/-I-dahuzNfuY/ToWLIjklZvI/AAAAAAAAAMk/lrp-gm6MKbA/s1600/gentoo_use1.png)

### Настройка кодировки:

```console
# nano -w /etc/locale.gen
```

вы увидите список закомментированных строк с кодировками, вот сверху или же ниже его впишите:

```
en_US.UTF-8 UTF-8
ru_RU.UTF-8 UTF-8
```

сохраните изменения и выйдите: `Ctrl+O`, `Ctrl+Q`

```console
# locale-gen
```

### Настройка времени:

```console
# cp /usr/share/zoneinfo/Europe/Moscow /etc/localtime
```

Теперь наше локальное время идёт по Кремлёвским курантам))
Можете скопировать любое место вашей дислокации из `/usr/share/zoneinfo`

## Ядро

Скачаем исходники ядра

```console
# USE="-doc symlink" emerge gentoo-sources
```

### Установка ядра

Способ 1 - всё и сразу

```console
# emerge genkernel
# genkernel all
```

В результате получим ядро с поддержкой разного ненужного хлама. Плюс этого способа - простота.
Примечание: можно подправить `/etc/genkernel.conf`, включив в нём параметры:

```
OLDCONFIG="yes"
MENUCONFIG="yes"
CLEAN="no"
MRPROPER="no"
```

В таком случае вы сможете собрать своё ядро, а genkernel сделает всё остальное.
После сборки можете просто проверить название созданного ядра и initrd, а затем обратиться к дальнейшему пункту о сборке программ:

```console
# ls /boot/kernel* /boot/initramfs*
```

Способ 2 - только то, что нужно

```console
# emerge pcutils (с её помощью вы сможете посмотреть аппаратную часть своего ПК)
# cd /usr/src/linux (переход в каталог с исходниками)
# make menuconfig (вызов меню с настройками)
```

![menuconfig](http://2.bp.blogspot.com/-Kp3waRhclrU/ToWLVz7j0xI/AAAAAAAAAMo/yjipyAJdiOw/s1600/gentoo_menuconfig.png)

Здесь всё строго индивидуально. Используете usb-мышь или клавиатуру? Проверьте включена ли их поддержка. Хотите, чтобы система понимала NTFS? Проверьте включена ли её поддержка. Настроек хватит на всё: тип процессора, видео, звук, поддержка файловых систем, девайсов устройств, поддерживаемых кодировок. Просто пройдитесь по пунктам меню и поразбирайтесь,что вам нужно,а что нет. Если вы испытываете затруднения с этим, можете ознакомиться со следующей заметкой, а затем продолжить.

Настроили? Теперь ядро нужно скомпилировать и установить:

```console
# make && make modules_install - для тех, кто занимался ручной сборкой
```

И скопировать ядро в `/boot`:

```console
# cp arch/x86_64/boot/bzImage /boot/
```

Пример:

```console
# cp arch/x86_64/boot/bzImage /boot/2.6.37-gentoo-r4
```

Если вы собрали ядро с initrg, следует всё же установить genkernel и скомандовать:

```console
# genkernel --install initramfs
```

Сборка программ, конфигурирование модулей, настройка загрузчика

```console
# emerge udev (автоматическое распознавание устройств) syslog-ng (служба журналирования) vixie-cron (что такое cron, думаю, знают все) dhcpcd (автоматическое получение IP-адреса, если у вас это дело статично, можете не ставить)
```

Теперь добавляем эти вещи в автозагрузку:

```console
# rc-update add udev boot
# rc-update add syslog-ng default
# rc-update add vixie-cron default
# rc-update add dhcpcd default
```

Проверяем наши устройства:

```console
# nano -w /ets/fstab
```

Должно получится примерно так:

![fstab](http://3.bp.blogspot.com/-2gM1M875onw/ToWMPewcg4I/AAAAAAAAAM4/RRNI4XwkV_0/s1600/gentoo_fstabrt1.png)

Обратите внимание: нужно убрать параметр noauto напротив `/boot` (в данном примере `/boot` расположен на `/sda1`)

Имя хоста:

```console
# nano -w /etc/conf.d/hostname
```

Укажите здесь имя своего ПК

Сеть:

```console
# nano -w /etc/conf.d/net
```

дописываем:

```sh
# /etc/conf.d/net
#
config_eth0="dhcp" # для получения динамического IP-адреса
# если адрес статичен,то впишите вместо dhcp свою информацию. Например:
config_eth0="192.168.0.2 netmask 255.255.255.0" # IP-адрес и адрес сети
routes_eth0="default via 192.168.0.1" # роутер
dns_servers_eth0="192.168.0.1 8.8.8.8" # DNS-адреса
```

Теперь следует указать gentoo на существующий интерфейс. Для этого создайте символьную ссылку на `net.eth0`:

```console
# cd /etc/init.d
# ln -s net.lo net.eth0
```

Добавление сетевого интерфейса в автозагрузку:

```console
# rc-update add net.eth0 default
```

Создание пароля для суперпользователя:

```console
# passwd
```

впишите пароль для учётной записи root

Примечание: можете также ознакомиться с настройками файла `/etc/rc.conf` (редактор по умолчанию, графическая среда и прочее)

Настройка раскладки клавиатуры:

```sh
# /etc/conf.d/keymaps
KEYMAP="ru"
```

Настройка часов:

```sh
# /etc/conf.d/clock
CLOCK="local"
TIMEZONE="Europe/Moscow"
```

Загрузчик:

- `# emerge grub`
- `# nano /boot/grub/menu.lst`
- `splashimage` - расскоментируете - будет картинка при загрузке
- `timeout` - время, после истечения которого начнётся загрузка
- `kernel` - можно дописать в конец этой строки разрешение экрана консоли, например, `vga=0x318`.

Обязательно проверьте, чтобы указанная здесь версия ядра полностью совпадала с версией собранного вами. Если это не так, исправьте на верную, иначе загрузчик просто не найдёт ядро.

Для тех у кого параллельно установлена Windows (на `/dev/sda1`):

```
title=Windows XP
rootnoverify (hd0,0)
makeactive
chainloader +1
```

Примечание: на практике информация про Windows не проверена

Установка загрузчика:

```console
# grep -v rootfs /proc/mounts > /etc/mtab
# grub install /dev/sda - где `sda` - ваш диск
```

## Финиш

```console
# exit
# cd
# umount /mnt/gentoo/boot /mnt/gentoo/proc /mnt/gentoo/dev /mnt/gentoo (в общем последовательно отмонтируйте всё, что смонтировали в `/mnt`)
# reboot
```

![gentoo grub](http://3.bp.blogspot.com/-z9UHd-dlQzU/ToWMYc2twdI/AAAAAAAAAM8/BHhdNkDdTVg/s1600/gentoo_grub4.png)

Перезагрузка, загрузка ПК с винчестера и вас встречают приглашением входа в систему.
Поздравляю, вы победили!

## Локализация системы

Перезагрузившись, мы обнаружим прескверную вещь: кириллица отображается квадратиками. Что ж, в `locale.gen` нужные настройки внесены, продолжим квест по русификации системы.

```console
# emerge terminus-font intlfonts freefonts cronyx-fonts corefonts kbd
```

В файле `/etc/env.d/02locale`:

```sh
LC_ALL=""
LANG="ru_RU.UTF-8"
```

В `/etc/conf.d/keymaps`:

```sh
keymap="ruwin_alt_sh-UTF-8"
windowkeys="NO"
extended_keymaps=""
dumpkeys_charset=""
fix_euro="NO"
```

В `/etc/conf.d/consolefont`:

```sh
consolefont="cyr-sun16"
consoletranslation=""
```

Можно также установить различные шрифты и поэкспериментировать с ними. После пересборки/установки шрифтов желательно выполнить:

```console
# fc-cache -fv
```

