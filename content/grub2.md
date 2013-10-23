Title: GRUB2: основные настройки
Date: 2012-11-13 08:15
Tags: Arch, Linux
Slug: grub2
Author: redVi
Summary: Не так давно в archlinux всё же прекратили поддержку grub-legacy. Теперь выбор варьируется между двумя загрузчиками.

Не так давно в archlinux всё же прекратили поддержку grub-legacy. Теперь выбор варьируется между двумя загрузчиками: Syslinux и Grub2. Как ясно из названия поста, автор отдаёт предпочтение второму варианту. Говорят, syslinux проще, поэтому большинство пользователей может обратить внимание на него.  А вот владельцам UEFI BIOS рекомендуют второй граб.


## Установка

```console
# pacman -S grub-bios grub2-common
# grub-install /dev/sda
# grub-mkconfig -o /boot/grub/grub.cfg
```

Теперь заглянем в файл `/etc/default/grub`

```sh
# /etc/default/grub
GRUB_DEFAULT=0 # загружаемый по умолчанию пункт меню, 0 - первый пункт
GRUB_TIMEOUT=5 # тайм аут, когда можно выбрать другой пункт, 5 - 5 секунд
GRUB_DISTRIBUTOR="Arch" # "поставщик" вашей версии grub'а
GRUB_CMDLINE_LINUX_DEFAULT="quiet acpi" # параметры загрузки для обычной загрузки
GRUB_CMDLINE_LINUX=""  # параметры загрузки (обычной и в режиме восстановления)
GRUB_PRELOAD_MODULES="part_gpt part_msdos" # дополнительные модули загрузки

# Uncomment to enable Hidden Menu, and optionally hide the timeout count
#GRUB_HIDDEN_TIMEOUT=5
#GRUB_HIDDEN_TIMEOUT_QUIET=true # скрыть отсчёт таймера

# Uncomment to use basic console
GRUB_TERMINAL_INPUT=console # использование консоли

# Uncomment to disable graphical terminal
#GRUB_TERMINAL_OUTPUT=console  # отключает графический терминал
GRUB_GFXMODE=auto # разрешение графического меню (800х600, например)

# Uncomment to disable generation of recovery mode menu entries
GRUB_DISABLE_RECOVERY=true # будет ли включен режим восстановления

# Uncomment and set to the desired menu colors.  Used by normal and wallpaper
# modes only.  Entries specified as foreground/background.
#GRUB_COLOR_NORMAL="light-blue/black" # настройка цветов графического меню
#GRUB_COLOR_HIGHLIGHT="light-cyan/blue"

# Uncomment one of them for the gfx desired, a image background or a gfxtheme
#GRUB_BACKGROUND="/path/to/wallpaper" # заставка для меню из ваших изображений
#GRUB_THEME="/path/to/gfxtheme" # тема графического меню
```

Подробнее можно почитать [здесь](http://ru.wikibooks.org/wiki/Grub_2).

![archlinux_grub](http://3.bp.blogspot.com/-_zu4gaDD3Zg/UHANztmprSI/AAAAAAAABwI/IyoemkBRr4A/s1600/Archl_Grub2.png "archlinux_grub")

## Изменение параметров:

### Настройка яркости экрана:

```sh
# /etc/default/grub:
GRUB_CMDLINE_LINUX_DEFAULT="quiet acpi_backlight=vendor"
```

После чего:

```console
# grub-mkconfig -o /boot/grub/grub.cfg
```

### Загрузка двух и более операционных систем

```console
# pacman -S os-prober
# grub-mkconfig -o /boot/grub/grub.cfg
```

Распознать имеющиеся ОС должен автоматически. Если этого не произошло, придётся
добавить вручную, после чего снова переконфигурировать конфигурационный файл
grub.

### Как добавить Windows?

В файл `/etc/grub.d/40_custom` внести строки:

```sh
menuentry "Microsoft Windows 7 BIOS-MBR" {
    insmod part_msdos
    insmod ntfs
    insmod search_fs_uuid
    insmod ntldr
    search --fs-uuid --no-floppy --set=root C474B30B74B2FEEC
    ntldr /bootmgr
}
```

где `fs-uuid` - ID вашего раздела с Windows. Определить его можно с помощью команды `blkid`:

```console
# sudo blkid
/dev/sda1: UUID="C474B30B74B2FEEC" TYPE="ntfs"
```

После чего обновить конфигурацию grub2:

```console
# grub-mkconfig -o /boot/grub/grub.cfg
```

## Украшательства

Для Archlinux можно найти неплохие темы в AUR.

Чтобы поставить тему, послужившую иллюстрацией к данному посту, проделываем следующие шаги - установим тему и скопируем её в директорию с grub:

```console
$ yaourt grub2-theme-archlinux
# cp -r /usr/share/grub/themes/Archlinux /boot/grub/themes/
```

Открываем в текстовом редакторе `/etc/default/grub`:

```sh
#/etc/default/grub
GRUB_THEME="/boot/grub/themes/Archlinux/theme.txt"
```

Рекомендуется установить разрешение экрана загрузчика к данной теме:

```
GRUB_GFXMODE=1024x768
```

После чего снова:

```console
# grub-mkconfig -o /boot/grub/grub.cfg
Генерируется grub.cfg …
Найдена тема: /boot/grub/themes/Archlinux/theme.txt
Найден образ linux: /boot/vmlinuz-linux
Найден образ initrd: /boot/initramfs-linux.img
No volume groups found
Найден Windows 7 (loader) на /dev/sda1
завершено
```

Также для эстетических целей используется `plymouth` (его часто можно увидеть в user-friendly дистрибутивах, например, в ubuntu), но автор сего зверя не ставит и не рекомендует по одной простой причине: он снижает скорость загрузки.
