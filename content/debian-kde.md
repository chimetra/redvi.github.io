Title: Установка KDE в Debian
Date: 2011-07-18 08:15
Tags: Debian, Decorations, Linux
Slug: debian-kde
Author: redVi
Summary: Давайте установим графическую среду KDE, зовущуюся в народе кедами.

Надоел gnome.... хочется чего-то свежего и красивого для настольной системы? Чтобы радовало глаз и была широта настроек? Давайте установим графическую среду KDE, зовущуюся в народе "кедами".

Для установки полного пакета со всеми "примочками" просто введите в консоли от рута:

    :::console
    # aptitude install kde-full

Впрочем, можете установить только базовую систему или же лишь необходимое вам из написанного ниже:

    :::console
    # aptitude install kdm kdebase-runtime kdebase-workspace kdebase kde-minimal kdeplasma-addons kdegraphics kdegames kdemultimedia kdenetwork kdepim kdeutils kdeadmin kdeartwork

Минималистам достаточно установить пакеты `kdm` и `kdebase-workspace`.

Начнётся установка необходимых компонентов. На все поступающие вопросы отвечайте `"yes"`

В конце установки вам предложат выбрать графическую среду по умолчанию. Тут уж я советовать не вправе: хотите просто ознакомиться с KDE - оставьте gnome, хотите с KDE мирно сосуществовать длительное время - оставьте его. Выбор за вами.

Перезагружаемся и выбираем в какой среде хотим работать:

![kde](http://1.bp.blogspot.com/-m6dLB3wYgqg/ToWa4uo93aI/AAAAAAAAANs/S71SSi2gBzM/s1600/kde.jpg "kde")

<b>Примечание:</b> для русификации среды поставьте пакет kde-l10n-ru
