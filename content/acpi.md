Title: Управление питанием и настройки acpi
Date: 2013-02-02 08:25
Tags: Linux, Gentoo
Slug: acpi
Author: redVi
Summary: Трудно приходится линуксоидам, не имеющим DE, а сидящим исключительно на WM &mdash; всё, что в полноценном Desktop Environment ( окружении рабочего стола или как это лучше обозначить на великом и могучем? ) поставляется и работает "из коробки" в WM нужно подбирать и настраивать.

Трудно приходится линуксоидам, не имеющим DE, а сидящим исключительно на WM &mdash; всё, что в полноценном Desktop Environment ( окружении рабочего стола или как это лучше обозначить на великом и могучем? ) поставляется и работает "из коробки" в WM нужно подбирать и настраивать. Вот и автором сего поста ранее были использованы элементы xfce для таких вещей как управление питанием, регулировка громкости звука и яркости экрана. Но вступило что-то в голову: ведь в моей системе всегда установлены acpi и laptop-mode-tools, так почему бы не обучить их выполнять их же непосредственные обязанности: делать всё то, для чего раньше нужны были xfce4-volumed и xfce4-power-manager?

Внимание! Для обучения нам понадобятся пакеты `laptop-mode-tools`, `acpi`, `acpid`. Acpid должен быть запущен.


## I. Уровень яркости экрана

Дописать в `/etc/default/grub` строки:

```sh
GRUB_CMDLINE_LINUX_DEFAULT="acpi_backlight=vendor resume=/dev/sda5"
```

Лезем в acpi

Создайте файлы со следующим содержанием:

Для увеличения яркости:

```sh
# /etc/acpi/actions/bl_up.sh
#
#!/bin/sh
bl_device=/sys/class/backlight/intel_backlight/brightness
echo $(($(cat $bl_device)+200)) >$bl_device
```

и для уменьшения яркости

```sh
# /etc/acpi/actions/bl_down.sh:
#
#!/bin/sh
bl_device=/sys/class/backlight/intel_backlight/brightness
echo $(($(cat $bl_device)-200)) >$bl_device
```

В `bl_device` замените `inel_backlight` на своё значение в зависимости от используемой видеокарты. Также стоит выяснить устраивающее вас значение, на основе которого будет увеличиваться или уменьшаться яркость экрана. У автора это значение = 200.

Как найти подходящее значение?
Посмотрите какая цифра стоит сейчас. Если вы ничего ещё не настраивали, она должна отражать максимально допустимое значение:

```console
# cat  /sys/class/backlight/intel_backlight/brightness
4882
```

Теперь поиграйте со значениями, чтобы выбрать нужный шаг:

```console
# echo 1000 > /sys/class/backlight/intel_backlight/brightness
# echo 1010 > /sys/class/backlight/intel_backlight/brightness
# echo 1100 > /sys/class/backlight/intel_backlight/brightness
```

Посмотрите как будет изменяться яркость экрана при разных значениях, если при добавлении 10 единиц вы практически не чувствуете разницы, добавьте ещё 50-100 единиц. Какой шаг покажется оптимальным, тот и оставьте.

Теперь укажем acpi использовать наши скрипты:

```sh
# /etc/acpi/events/bl_up
#
event=video[ /]brightnessup
action=/etc/acpi/actions/bl_up.sh


# /etc/acpi/events/bl_down
#
event=video[ /]brightnessdown
action=/etc/acpi/actions/bl_down.sh
```

и сделаем эти скрипты исполняемыми:

```console
# chmod +x /etc/acpi/actions/{bl_up.sh,bl_down.sh}
```

Чтобы автоматически подбирать яркость при работе от аккумулятора или же сети, установим laptop-mode-tools:

```console
# pacman -S laptop-mode-tools
```

и немного изменим его настройки:

```sh
# /etc/laptop-mode/conf.d/lcd-brightness.conf
#
CONTROL_BRIGHTNESS=1
# Commands to execute to set the brightness on your LCD
#
#BATT_BRIGHTNESS_COMMAND="echo [value]"
BATT_BRIGHTNESS_COMMAND="echo 700"
LM_AC_BRIGHTNESS_COMMAND="echo 2000"
NOLM_AC_BRIGHTNESS_COMMAND="echo 3000"
BRIGHTNESS_OUTPUT="/sys/class/backlight/intel_backlight/brightness"
```

Разумеется, значения `700/2000/3000` и путь `/sys/class/backlight/intel_backlight/brightness` должны быть заменены на ваши значения.

## II. Автогибернация при критическом уровне заряда батареи

Достаточно часто бывает такое, что при работе от батареи забываешь посматривать на уровень её заряда, в результате чего получаешь отключение машины при полной разрядке батареи. Внезапное - как хлопок - выключение и все несохранённые данные потеряны. Обидно, не правда ли? Поэтому неплохо было бы позаботиться о своевременных мерах предосторожности.
Для этих целей также будем использовать функционал laptop-mode.

```sh
# /etc/laptop-mode/conf.d/auto-hibernate.conf:
#
ENABLE_AUTO_HIBERNATION=1
#
# The hibernation command that is to be executed when auto-hibernation
# is triggered.
#
HIBERNATE_COMMAND=/usr/share/laptop-mode-tools/module-helpers/pm-hibernate
#
# Auto-hibernation battery level threshold, in percentage of the battery's
# total capacity.
#
AUTO_HIBERNATION_BATTERY_CHARGE_PERCENT=4
#
# Enable this to auto-hibernate if the battery reports that its level is
# "critical".
#
AUTO_HIBERNATION_ON_CRITICAL_BATTERY_LEVEL=1
```

Если вас не устраивают значения по умолчанию, вы также можете изменить их.
В случае, если до этого момента у вас не был указан раздел swap, укажите его в grub2, эти настройки уже были даны выше:

```sh
# /etc/default/grub
#
GRUB_CMDLINE_LINUX_DEFAULT="acpi_backlight=vendor resume=/dev/sda5"
```

где `/dev/sda5` - ваш swap-раздел
Кроме того, в случае с archlinux следует добавить хук suspend в  `/etc/mkinitcpio.conf`:

```sh
HOOKS="base udev autodetect modconf block filesystems usbinput fsck resume"
```

и пересобрать initrd:

```console
# mkinitcpio -p linux
```

## III. Регулировка звука

Для этого снова обратимся к скриптам acpi, как и в случае с управлением яркостью дисплея.

```sh
# /etc/acpi/actions/volume_up.sh
#
#!/bin/bash
/usr/bin/amixer set Master 5%+

# /etc/acpi/actions/volume_down.sh
#
#!/bin/bash
/usr/bin/amixer set Master 5%-

# /etc/acpi/events/volume_up
#
event=button[ /]volumeup
action=/etc/acpi/actions/volume_up.sh

# /etc/acpi/events/volume_down
#
event=button[ /]volumedown
action=/etc/acpi/actions/volume_down.sh
```

Делаем скрипты в actions исполняемыми:

```console
# chmod +x /etc/acpi/actions/{volume_up.sh,volume_down.sh}
```

Для корректного распознавания мультимедийных клавиш, лучше использовать утилиту `xmodmap`.

```console
$ xmodmap -pke > ~/.xmodmap
$ vim .xinitrc:
xmodmap ~/.xmodmap
```

## IV. Acpi и события клавиш

Честно говоря, меня устраивает поведение по-умолчанию, поэтому с пристрастием этот вопрос не рассматривался. При закрытии крышки ноутбука машина переходит в режим гибернации. При нажатии кнопки питания - корректно отключает систему. Оно и хорошо.

Похоже, управление этими событиями тоже берёт на себя laptop-mode-tools ( только пока неясно, в каком модуле/скрипте лежат эти настройки), поскольку в `/etc/acpi/handler.sh` каких-либо действий на события не назначено.

Но таки рассмотрим как настраивать то или иное событие.

Ответственен за эти шаманские действа вышеупомянутый `handler.sh` (или `default.sh` в зависимости от используемого дистрибутива), где и прописываются настройки. В случае, если вам хочется использовать не команду, а скрипт, расположите его в отдельном файле, подобно тому, как выше настраивалось управление яркостью дисплея и уровнем громкости .

Пример из дефолта:

```sh
button/lid)
        case "$3" in
            close)
                logger 'LID closed'
                ;;
            open)
                logger 'LID opened'
                ;;
            *)
                logger "ACPI action undefined: $3"
                ;;
    esac
    ;;
```

`button/lid` указывает на управление закрытием/открытием крышки ноутбука, пока здесь нет ничего интересного.

Пример с воспроизведением звукового файла при закрытии/открытии крышки ноутбука:

```sh
    button/lid)
        case "$3" in
            close)
                logger 'LID closed'
                aplay /home/redvi/.scripts/message.wav
                ;;
            open)
                logger 'LID opened'
                aplay /home/redvi/.scripts/message.wav
                ;;
            *)
                logger "ACPI action undefined: $3"
                ;;
    esac
    ;;
```

То есть для настройки события нужно добавить его команду в соответствующее поле ( здесь после `logger 'LID closed'`). Так, действие при открытии крышки нужно будет вписать после `logger 'LID opened'`.

`button/power` &mdash; события, связанные с кнопкой управления питанием

`logger 'PowerButton pressed'` &mdash; когда клавиша нажата

`button/sleep` &mdash; сон, если подобная кнопка/клавиша имеется

`ac_adapter` &mdash; события, связанные с подключением/отключением адаптера питания

`logger 'AC unpluged'` &mdash; когда адаптер отключен

`logger 'AC pluged'` &mdash; когда адаптер подключен

`battery` &mdash; батарея ноутбука

`button/lid` &mdash; крышка ноутбука

Для перевода в ждущий/спящий режимы можно использовать скрипты `laptop-mode-tools` из `/usr/share/laptop-mode-tools/module-helpers`:  `pm-hibernate` и  `pm-suspend`.

Для выключения питания при закрытии крышки достаточно добавить в `/etc/acpi/actions/lm_lid.sh` строку:

```sh
[ "$3" = "close" ] && poweroff
```

Помимо всего вышеописанного мы можем контролировать парковку головок жёсткого диска. Дабы отключить парковку совсем пропишите в `/etc/laptop-mode/laptop-mode.conf`:

```sh
BATT_HD_POWERMGMT=254
LM_AC_HD_POWERMGMT=254
NOLM_AC_HD_POWERMGMT=254
```

Пожалуй, на этом стоит остановиться и дать читателю возможность самостоятельно поэкспериментировать с настройками энергосбережения и событий acpi.
