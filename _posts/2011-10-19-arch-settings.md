---
layout: post
title: Arch Linux. Тонкая настройка
date: 2011-10-19 08:25
tags: [arch, linux]
slug: arch-settings
author: redVi
summary: В продолжение статьи об установке лёгкого, быстрого и простого дистрибутива.
---

В продолжение статьи [об установке лёгкого, быстрого и простого дистрибутива](http://www.unix-lab.org/posts/arch-install/). В конце поста небольшой видеоролик с установкой LXDE. Не красоты ради, а удобства для. Чтобы вам не приходилось настраивать свой арч, сидя в консоли.

В общем и целом настройка arhclinux будет сведена к нескольким несложным действиям как то:

- [Настройка интернет-соединения](#inet)
- [Установка драйверов на видео + xorg](#xorg)
- [Установка окружения рабочего стола](#environ)
- [Настройка тачпада](#touchpad)
- [Переключение графики при наличии двух видеокарт](#switcheroo)
- [Энергосбережение](#powersave)
- [fn-клавиши](#fn)


### <a id="inet"></a>Настройка интернет-соединения

Примеры конфигураций можно посмотреть по адресу `/etc/network.d/examples/`

[![net](http://farm4.staticflickr.com/3718/10549379683_14bd417c23_n.jpg)](http://farm4.staticflickr.com/3718/10549379683_108ecedbf4_o.png)

 Достаточно выбрать своё подключение и скопировать соответствующий файл в `/etc/network.d/` наименование_вашего_профиля. Например:

```console
# cp /etc/network.d/examples/ethernet-static /etc/network.d/eth0
```

Открыть скопированный файл в любимом текстовом редакторе и исправить значения на свои:

[![static](http://farm3.staticflickr.com/2816/10549393903_07c261b4b6_n.jpg)](http://farm3.staticflickr.com/2816/10549393903_31fa0a31f1_o.png)

После чего запустить профиль командой:

```console
# netcfg eth0 up
```

### <a id="xorg"></a>Установка драйверов на видео + xorg

Посмотрим на свою видеокарту:

```console
$ lspci | grep VGA
```

или

```console
$ lspci | grep -i vga
```

Найдём нужный (в примере открытый для карты intel!) драйвер:

```console
# pacman -Ss xf86-video-intel | less
```

Установим необходимые пакеты:

```console
# pacman -S xf86-video-intel
# pacman -S xorg-server xorg-xinit xorg-utils xorg-server-utils mesa mesa-demos
```

Дайте команду `startx`. Если всё в порядке, вы увидите псевдографические окна. Если нет:

пробуем запустить графику с драйвером `vesa`:

```console
# pacman -S xf86-video-vesa
```

конфигурируем xorg:

```console
# Xorg -configure
```

Файл конфигурации появится в каталоге `/root` и будет носить название `xorg.conf.new`. отредактируйте его, если нужно, и скопируйте в каталог `/etc/X11`:

```console
# cp xorg.conf.new /etc/X11/xorg.conf
```

Стартуйте графику снова.

### <a id="environ"></a>Установка окружения рабочего стола:

```console
# pacman -S lxde
```

<b>Примечание:</b> lxde лишь один из возможных вариантов и приводится как пример

Стартуем:

```console
$ sudo /user/sbin/lxdm start
```

Теперь вы увидите обычный рабочий стол с окружением lxde. Чтобы запускать графику при старте системы следует дописать в `/etc/rc.conf` в секцию `DAEMONS` - lxde.

### <a id="touchpad"></a>Настройка тачпада (если есть):

```console
# pacman -S xf86-input-synaptics
```

Создаём в `/etc/X11/xorg.conf.d/` новый файл с именем `50-synaptics.conf`:

```sh
Section "InputClass"
    Identifier "touchpad"
    Driver "synaptics"
    MatchIsTouchpad "on"
    Option "SHMConfig" "on"
    Option "TapButton1" "1"
    Option "TapButton2" "2"
    Option "TapButton3" "3"
    Option "VertEdgeScroll" "on"
    Option "VertTwoFingerScroll" "on"
    Option "HorizEdgeScroll" "on"
    Option "HorizTwoFingerScroll" "on"
    Option "CircularScrolling" "on"
    Option "CircScrollTrigger" "2"
    Option "EmulateTwoFingerMinZ" "0"
EndSection
```

### <a id="switcheroo"></a>Переключение графики при наличии двух видеокарт:

Подмонтируем `gebug`:

```console
# mount -t debugfs /sys/kernel/debug
# vim /etc/fstab:
debugfs /sys/kernel/debug   debugfs defaults    0   0
# modprobe radeon
```

Перезагрузка

Проверьте поддержку `vgaswitcheroo` в ядре:

```console
$ cat /sys/kernel/debug/vgaswitcheroo/switch
```

или, если каталога и файла `vgaswitheroo/switch` ещё нет:

```console
$ gzip -cd /proc/config.gz | grep SWITCHEROO
WGASWITCHEROO=y
```

Такое выдало? Отлично, всё включено. Нет? Идите и [компилируйте ядро с поддержкой vgaswitcheroo](http://www.unix-lab.org/posts/kernel-v3/).

Активировать ATI:

```console
# echo DDIS > /sys/kernel/debug/vgaswitcheroo/switch
```

Активировать Intel:

```console
# echo DIGD > /sys/kernel/debug/vgaswitcheroo/switch
```

Отключить неиспользуемую видеокарту:

```console
# echo OFF > /sys/kernel/debug/vgaswitcheroo/switch
```

Включить неиспользуемую видеокарту:

```console
# echo ON > /sys/kernel/debug/vgaswitcheroo/switch
```

Если чувствуете, что карта не отключилась:

```console
# echo "blacklist radeon" >> /etc/modprobe.d/modprobe.conf
```

Если нужно, чтобы карта не включалась при загрузке системы, допишите в `/etc/rc.locale`:

```sh
# chown "username" /sys/kernel/debug/vgaswitcheroo/switch
# где "username" имя вашего пользователя
# echo OFF > /sys/kernel/debug/vgaswitcheroo/switch
```

[![off](http://farm6.staticflickr.com/5547/10549166836_af0c02e973_n.jpg)](http://farm6.staticflickr.com/5547/10549166836_34d5e9c23f_o.png)

### <a id="powersave"></a>Энергосбережение

Не буду повторять многократно пересказанное. Вики вам в помощь, дамы и господа:

- [acpi](http://www.unix-lab.org/posts/acpi/)
- [laptop](https://wiki.archlinux.org/index.php/Laptop_(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9))
- [lm sensors](https://wiki.archlinux.org/index.php/Lm_sensors_(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9))

Для автоматического старта `laptop-mode`:

```console
# systemctl enable laptop-mode.service
```

### <a id="fn"></a>Горячие клавиши, fn-клавиши ноутбука

В KDE изначально не было возможности регулировать яркость экрана, что, впрочем, быстро пофиксилось добавлением лишь одной строки к загрузчику. Зато Gnome 3 приятно удивил, подхватив и кнопки управления яркостью дисплея, и кнопки увеличения громкости звука, и даже включение bluetooth, так что... хотите работу "из коробки" &mdash; добро пожаловать в Gnome.

<u>KDE</u>
[![kde](http://farm3.staticflickr.com/2812/9471540916_d9ffb37430_n.jpg "KDE")](http://farm3.staticflickr.com/2812/9471540916_d9ffb37430_b.jpg)

<u>Gnome</u>
[![gnome](http://farm6.staticflickr.com/5322/9468762349_c9cfdfa125_n.jpg "Gnome")](http://farm6.staticflickr.com/5322/9468762349_c9cfdfa125_b.jpg)

Для любителей минимализма осмелюсь порекомендовать [openbox](http://www.unix-lab.org/posts/openbox/) или же [xmonad](http://www.unix-lab.org/posts/xmonad/).

<b>ВНИМАНИЕ!</b> Поскольку с недавнего времени archlinux претерпел некоторые изменения, а именно осуществился переход к `systemd`, файл `/etc/rc.conf`, скорее всего, скоро перестанет поддерживаться, хотя на данный момент такая возможность есть. Вместо этого пишутся юниты для автозапуска тех или иных сервисов. Так, юнит запуска KDM выглядит следующим образом:

[![systemd](http://farm6.staticflickr.com/5515/10549455943_d4df01c7b3_n.jpg)](http://farm6.staticflickr.com/5515/10549455943_827000a983_o.png)

Для того, чтобы KDM стартовал при загрузке системы, выполните команду:

```console
# systemctl enable kdm.service
```

Запуск `rc.local` больше не требуется. Вместо этого создадим юнит с нужной командой (в примере: отключение внешней видео карты)

```sh
# /etc/systemd/system/rc-local.service
#
[Unit]
Description=/etc/rc.local
Compatibility [Service]
Type=oneshot
ExecStart=/bin/sh -c 'echo OFF > /sys/kernel/debug/vgaswitcheroo/switch'
RemainAfterExit=yes
[Install]
WantedBy=multi-user.target
```

Для запуска iptables при старте системы

```sh
# /etc/systemd/system/iptables.service
#
[Unit]
Description=Start iptables
[Service] ExecStart=/usr/sbin/iptables
[Install] Before=network.target
```

Добавление в автозапуск осуществляется командами `systemctl enable rc-local.service`
и `systemctl enable iptables.service` соответственно.

Тема юнитов `systemd` достаточно объёмна и заслуживает отдельного рассмотрения. Подробнее [здесь](https://wiki.archlinux.org/index.php/Systemd).

Модули ядра теперь живут по адресу: `/etc/modules-load.d/`

Так, чтобы при старте системы загружались необходимые модули, мы можем создать файл с расширением `.conf` и вписать их туда. Например:

```sh
# /etc/modules-load.d/load_modules.conf
#
acpi-cpufreq cpufreq_conservative
```

Удачи!

<div class="video"><iframe width="400" height="300" src="http://www.youtube.com/embed/2EIo6-bH9DU?rel=0" frameborder="0" allowfullscreen></iframe></div>
