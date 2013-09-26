Title: Настройка DSL в Debian/Ubuntu Linux
Date: 2011-10-30 08:25
Tags: Debian, Linux
Slug: debian-dsl
Author: redVi
Summary: После установки linux первое, что обычно делает счастливый пользователь - настройка интернет-соединения.

 После установки linux первое, что обычно делает счастливый пользователь - настройка интернет-соединения. Но не у всех получается произвести её корректно. Поэтому сегодня рассмотрим простейший способ настройки ADSL под Debian Squeeze. Итак, поехали.

##I. Используем конфигуратор

###1. Введите в терминале:

    :::console
    # ifconfig -a

Это позволит просмотреть список найденных сетевых интерфейсов

Примечание: `lo` – интерфейс вашего локального хоста, на нём внимание не заостряем. Нас интересует `eth0` или же `ppp0`. В случае, если у вас одна сетевая карта, обычно так оно и есть.

###2. Установим и запустим pppoeconf:

    :::console
    # apt-get install pppoeconf
    # pppoeconf

На DVD-диске debian pppoeconf точно есть, ставим с диска.

Перед вами появится окно настройки интернет-соединения. Тут всё просто: следуйте подсказкам. В большинстве случаев просто соглашайтесь со всем, что вам будет предложено. Здесь введите свой логин:

![login](http://1.bp.blogspot.com/-uzF5nkVaaz4/Tp-ixjdmy2I/AAAAAAAAAUI/zfZ5J02YQA0/s1600/username.jpg)

и пароль:

![password](http://1.bp.blogspot.com/-6RLRqSWPU48/Tp-i5WlaqJI/AAAAAAAAAUQ/PNFE1s4aVmA/s1600/passwd.jpg)

После сканирования сети вы получите готовый к употреблению, рабочий интернет.

![pppoe](http://3.bp.blogspot.com/-24QD9Nof_ng/Tp-i_vEPGzI/AAAAAAAAAUY/SdZ0fOC9foE/s1600/ok.jpg)

Для того, чтобы убедиться в его работоспособности, попингуем гугл, например:

    :::console
    $ ping google.com

<b>Примечание:</b>

`$ pon dsl-provider` – подключаемся

`$ poff dsl-provider` - отключаемся

`$ plog` – отобразит текущее стостояние подключения

`$ ifconfig ppp0` – отобразит сетевой интерфейс `ppp0`


##II. Network Manager

Легче всего настроить подключение при помощи стандартного Network Manager (как в Windows). Проблема в том, что он не всегда корректно работает. Её рассматривать не будем - всё легко, сами разберётесь.


##III. Ручная конфигурация ( рекомендую )

Создаём конфигурационный файл `/etc/ppp/peers/pppoe`:

    # /etc/ppp/peers/pppoe

    plugin rp-pppoe.so
    # rp_pppoe_ac 'your ac name'
    # rp_pppoe_service 'your service name'

    # network interface
    eth0
    # login name
    name "someloginname"
    usepeerdns
    persist
    # Uncomment this if you want to enable dial on demand
    #demand
    #idle 180
    defaultroute
    hide-password
    noauth


Вы используете тип аутентификации PAP или CHAP. В зависимости от типа правим конфиги `/etc/ppp/pap-secrets` или же `/etc/ppp/chap-secrets`. Там нужно прописать ваш логин и пароль.
Формат:

    "login" * "password"

Соединяемся:

    :::console
    $ sudo pon pppoe

Отключаемся:

    :::console
    $ sudo poff pppoe

Можете сделать это соединение используемым по умолчанию. Для этого создайте ссылку вида:

    :::console
    $ ln -s pppoe /etc/ppp/peers/provider

И можете управлять соединением командами pon и poff.
Можете также ознакомиться с настройками файла `/etc/ppp/options`, если знаете, что делаете.


Настройка Ethernet со статическим IP-адресом

Предположим, что Вы хотите назначить IP-адрес 192.168.0.2 на устройство `eth1`, с маской 255.255.255.0.
Ваш IP- адрес шлюза по умолчанию 192.168.0.1.
Введите в файл `/etc/network/interfaces`:

    iface eth1 inet static
    address 192.168.0.2
    netmask 255.255.255.0
    gateway 192.168.0.1
    В этом случае, нужно будет вписать DNS-серверы в файл /etc/resolv.conf
    search domain.example
    nameserver 192.168.0.1
    nameserver 4.2.2.2

Директива `search` добавит строку `domain.example` к имени хоста, и попытается найти название в вашей сети. Например, домен сети - `domain.example`, и вы пытаетесь вызвать хост `“myhost”`, запрос доменной системы имен будет изменен на `“myhost.domain.example”` для возможности поиска в домене.
Если Вы используете свой собственный сервер имен, пропишите его в данном файле. В ином случае информацию вам должен предоставить Провайдер.


Теперь немного о конфигурационных файлах.

`/etc/ppp/resolv.conf` - здесь прописываются DNS-адреса

В `/etc/network/interfaces`  хранится большинство сетевых настроек

`/etc/iftab` - содержит таблицу интерфейсов (соответствие имён и интерфейсов их MAC-адресов)

`/etc/servises` - база данных сервисов, задающая соответствие имени сервиса и номера порта.
`/etc/hosts.deny` - содержит IP-адреса узлов, которым запрещён доступ к сервисам данного узла.
`/etc/hosts.allow` - содержит IP-адреса узлов, доступ которым разрешён.

