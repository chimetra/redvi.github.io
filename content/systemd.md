Title: Systemd: загрузись по-новому
Date: 2012-09-22 08:15
Tags: Arch
Slug: systemd
Author: redVi
Summary: Systemd и как с ним управляться

##Предыстория

Поскольку всех арчеводов облетела благая весть о переходе на более современную систему инициализации, на которую, собственно, переходить немногие торопились, случилось и автору сего поста опробовать её в действии. Надо заметить, в archlinux имеется интеграция этой весёлой вещи со стандартными конфигурационными файлами системы. Но мы, конечно, не стали пользоваться такими благами цивилизации и решили опробовать "чистый" systemd в действии. После этого благого намерения был установлен systemd, перезагружена система и... началось! Интернет, конечно, работать отказался. Любимый `rc.local` не загрузил своё содержимое, а запускающиеся раньше из `rc.d/` сервисы вроде `network, httpd` и им подобных вываливались с ошибками. Так что сегодня на повестке обзор systemd и правила его использования.

Решение проблем с сетью и `rc.local` - [archlinux systemd](arch-settings.html)

##Основная часть

Systemd предлагает ряд удобств по сравнению с прошлой системой инициализации. займёмся рассмотрением основных возможностей и команд.

Просмотр информации о запуске служб, в том числе и тех, что стартовали при загрузке системы. То есть необязательно смотреть логи системы, можно увидеть неудачный запуск того или иного демона прямо в выводе командной строки:

    :::console
    # systemctl

![systemctl](http://4.bp.blogspot.com/-YnJckgoRAa8/UEd8zu46M0I/AAAAAAAABZk/jbVeiOBIQaM/s1600/systemctl.png)

Также имеется возможность наблюдать за поведением сервиса при помощи команды `status`, например:

    :::console
    # systemctl status httpd.service
    httpd.service - Apache start
              Loaded: loaded (/etc/systemd/system/httpd.service; static)
              Active: activating (start) since Wed, 05 Sep 2012 22:32:12 +0700; 56min ago
            Main PID: 10366 ((httpd))
              CGroup: name=systemd:/system/httpd.service
                      └ 10366 (httpd)

Так мы узнаем, что искомый сервис был запущен  с PID процесса 10366 5 сентября 2012 года в 22:32, его uptime составляет 56 минут.

Если сервис остановлен:

    httpd.service - Apache start
              Loaded: loaded (/etc/systemd/system/httpd.service; static)
              Active: inactive (dead) since Wed, 05 Sep 2012 23:54:24 +0700; 2s ago
             Process: 10366 ExecStart=/etc/rc.d/httpd (code=killed, signal=TERM)
              CGroup: name=systemd:/system/httpd.service

Нам доброжелательно укажут, что состояние его неактивно уже целых 2 секунды.

При ошибке `systemd` должен выдать такое же детальное её описание. Кроме того, ходит слух, что в последующих версиях при ошибках разработчикам будет отправляться автоматический багрепорт. Что ж, это впечатляет.

##Запуск, останов, reload

    :::console
    Для запуска сервиса:
    # systemctl start your_service_name.service
    Останов:
    # systemctl stop your_service_name.service
    Перезапуск:
    # systemctl restart your_service_name.service
    Перезагрузка настроек:
    # systemctl reload your_service_name.service

    Добавление в автозагрузку, удаление из автозагрузки:
    # systemctl enable your_service_name.service
    # systemctl disable your_service_name.service
    соответственно.

    Завершить процесс
    # systemctl kill your_service_name.service

    Грубый останов (если ничто его больше не берёт)
    # systemctl kill -s SIGKILL your_service_name.service

##Разбор юнитов

Пример юнита для запуска KDM:

    :::sh
    [Unit]
    Description=K Display Manager
    After=systemd-user-sessions.service
    [Service]
    ExecStart=/usr/bin/kdm -nodaemon
    [Install]
    Alias=display-manager.service

- Unit - общая информация
- Description - описание сервиса
- After - после какого события рекомендуется запуск. В данном случае после старта сессии пользователя. Иными словами мы задаём порядок загрузки
- Service - содержит информацию о службе
- ExecStart - что запускать. Иными словами указание расположения бинарного файла службы. Возможно вписать и аргументы, с которыми он должен быть запущен ( -noademon )
- Install - в каких ситуациях юнит должен быть активирован. Чаще всего при нормальной загрузке системы. Тогда необходимо вписать "WantedBy=multi-user.target". В данном юните прописан алиас сервиса.

Ещё пример. Запуск файрволла при активации сети:

    :::sh
    [Unit]
    Description=Start iptables
    [Service]
    ExecStart=/usr/sbin/iptables
    [Install]
    Before=network.target



##Уровни выключения

###Останов

Возможность просто остановить службу. В последующем можно также легко запустить её

    :::console
    # systemctl stop your_service_name.service

###Полное выключение службы

В том числе убрать из автозапуска. Остаётся лишь возможность ручной загрузки

    :::console
    # systemctl disable your_service_name.service

### Замаскировать службу

Иначе - заблокировать. В этом случае служба не будет находиться в автозапуске, но и запустить вручную вы её больше не сможете. Для этого создаётся символьная ссылка на /dev.null с последующей командой:

    :::console
    # ln -s /dev/null /etc/systemd/system/your_service_name.service
    # systemctl daemon-reload

Ещё способ:

    :::console
    # systemctl mask your_service_name.service
    # systemctl unmask your_service_name.service

##Вместо заключения

А что вы думаете по поводу перехода многих дистрибутивов на systemd, нравится ли новая система инициализации или она приносит лишь разочарование? Ведь на systemd, похоже, скоро переедет весь мир linux: arch, openSUSE, Fedora... за ними потянутся и остальные.

