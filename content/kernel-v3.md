Title: Ядерная физика для домохозяек v.3
Date: 2013-04-19 1:15
Tags: Gentoo, Kernel, Linux
Slug: kernel-v3
Author: redVi
Summary: Автору захотелось немного обновить информацию о сборке ядра, за которым уже давно закреплена циферка три.

Достаточно давно была написана отличная статья, послужившая верой и правдой многим линуксоидам, кто самостоятельно собирал  своё ядро. Называлась она &laquo;Ядерная физика для домохозяек, версия 2&raquo;. Ранее, когда деревья были выше, небо голубее, а настольные компьютеры не столь производительны, сборка ядра под своё железо могла внести весомый вклад в увеличение производительности железного друга. Теперь это уже не столь важно и в большинстве случаев даже не нужно, ибо прирост будет незначительным. Да и среднестатистический линуксоид как-то обмельчал, &laquo;скуксился&raquo; что ли.

Тем не менее, автору захотелось немного обновить информацию о сборке ядра, за которым уже давно закреплена циферка три.

## Оглавление:

- [Вступление или подготовка к сборке ядра](#begin)
- [General setup](#general)
- [Enable loadable module support](#modules)
- [Enable the block layer](#block_layer)
- [Processor type and features](#processor)
- [Power management and ACPI options](#power)
- [Bus options (PCI etc.)](#bus)
- [Executable file formats / Emulations](#emulations)
- [Networking support](#networking)
- [Device Drivers](#device)
- [Firmware Drivers](#firmware)
- [File systems](#filesystem)
- [Kernel hacking](#kernel_hack)
- [Security options](#security)
- [Cryptographic API](#crypto)
- [Virtualization](#virtu)
- [Library routines](#library)
- [Послесловие](#end)


##Вступление или подготовка к сборке ядра {#begin}


Для сборки можно использовать ядро с [kernel.org](http://kernel.org/). Если вам удобнее собрать ядро, поставляемое с вашим дистрибутивом, вы можете смело пропустить этот шаг.

Пройдите по указанной выше ссылке и скачайте ядро `Latest Stable Kernel`. Должен скачаться файл примерно с таким наименованием: `linux-3.6.11.tar.bz2`.

Помимо этого, иногда вам может понадобиться поставить заплатки для ядра. Если вы не знаете, что это, значит оно вам и не нужно. Хотя мы рассмотрим процесс наложения заплаток для полноты картины. Получить их можно всё на том же сайте.

Рекомендация по собственно сборке ядра одна на все дистрибутивы, что естественно. А вот инструмент для сборки вполне возможно, что придётся доустановить. Для gentoo это пакет `gentoo-sources` (если предполагается сборка дистрибутивного ядра). Для дебиана понадобится установить [целую пачку пакетов](debian-kernel.html), для арча  понадобится пакет `base-devel` и [эта инструкция](abs.html).

Перед сборкой неплохо сесть и подумать какое же ядро собрать. Ядро может быть:

<b>- монолитным</b>

такое ядро полностью грузится при старте системы и остаётся в оперативной памяти до выключения машины. Его компоненты нельзя изменить, невозможно подгружать и выгружать модули благодаря чему ядро становится нечувствительным к различным троянским программам, направленным на подмену оригинальных модулей своими - это просто невозможно. Но с другой стороны монолитность ядра привносит и некоторые минусы, такие как невозможность установить стороннюю прошивку или проприетарный драйвер для видеокарты (ведь его модуль нельзя будет подгрузить!). То есть для домашних машин лучше не использовать монолитные ядра, а вот для серверов - самое оно.

<b>- модульным</b>

это ядро напротив позволит включать многие компоненты не жёстко, а модульно (соответственно своему названию), что уменьшит размер ядра и сделает возможным... да, загрузку и выгрузку нужных модулей. В готовых дистрибутивах для создания такого ядра используется initramfs (раньше - initrd). Но при сборке под себя можно обойтись и без него, достаточно лишь жёстко встроить поддержку файловой системы и контроллёра HD корневого раздела для того, чтобы система смогла определить их и загрузиться.
<b>Считаю небезынтересным:</b> [в чём разница между initrd и initramfs](http://teleology.mobi/ru/news_ru/15032006-01_ru).

Обычно предлагается включить в ядро жёстко те компоненты, которые нужны вам постоянно,  а те, что предполагается использовать время от времени, включить модулями.

Итак, вы скачали ядро и заплатки. Переместите их в каталог `/usr/src/` и сами перейдите в него.
Теперь следует распаковать исходники ядра и архивы с заплатками, наложить заплатки:

    :::console
    # tar xvf linux-3.6.11.tar.bz2
    # cp patch-3.6.11.bz2 linux-3.6.11/
    # bzip2 -d patch-3.6.11.bz2
    # patch -p1 -i patch-3.6.11.bz2

При наложении заплаток есть лишь один нюанс: сначала накладывается заплатка для обновления версии ядра (`patch-$VERSION.bz2` как дано выше) и уже затем все остальные.

Обратите внимание на вывод команды `patch`. Если заплатка идеально подходит к ядру, то в выводе должны быть только строчки `patching file ...` . Строка `Hunk #1 succeeded at...` означает что заплатка наложена успешно, но место наложения сдвинуто на несколько строк. Если же вы увидите слово `Failed` -  заплатка не подходит. Лучше удалить каталог `linux-3.6.11/` и начать все сначала уже без этой заплатки.

Далее могут выполнены следующие команды:

`make mrproper` - очистит каталог от мусора предыдущей сборки

`make menuconfig` - запустит окно настроек ядра

`[ * ]` - опция включена жёстко

`[M]` - опция включена модульно

`[   ]` - опция отключена

Вы можете воспользоваться поиском по параметрам ядра, для этого нажмите `"/"` (слеш) и введите искомое. Также не забывайте о справке: остановитесь на параметре, подробное описание которого вам хотелось бы видеть, и выбирайте `"Help"` внизу экрана.


##General setup {#general}

Содержит общие настройки

![gen](http://2.bp.blogspot.com/-7mAvCkWeVM8/URjy9WQGCpI/AAAAAAAAD6o/3EliCC8WGl4/s1600/general.jpg)

    [*] Prompt for development and/or incomplete code/drivers

Некоторые вещи, которые поддерживает Linux (таких, как сетевые драйверы, файловые системы, сетевые протоколы и т.д.) могут находиться в состоянии  разработки, где функциональность, стабильность или уровень тестирование еще не достаточно высоки для общего использования. То есть данная опция включает дополнительные экспериментальные настройки. Рекомендуется включить, чтобы отображались все доступные опции.

    ()  Local version - append to kernel release

Сюда можно внести наименование, которым дополнится название вашего ядра. Бывает полезно, когда вы собираете несколько ядер одной и той же версии. Обычно не нужно.

    Kernel compression mode (Gzip)  --->
              (X) Gzip
              ( ) Bzip2
              ( ) LZMA
              ( ) XZ
              ( ) LZO

Доступные алгоритмы сжатия, отличающиеся по скорости, эффективности, компрессии и декомпрессии. Скорость сжатия имеет значение только при сборке ядра.

    [*] Support for paging of anonymous memory (swap)

Поддержка ядром своп-файла. Включаем.

    [*] System V IPC
               [*] POSIX Message Queues
               [*] BSD Process Accounting
               [ ] BSD Process Accounting version 3 file format

`System V IPC` - механизм связи между процессами. Набор библиотечных функций и вызовов ядра, позволяющий процессам обмениваться информацией. Некоторые программы требуют этого механизма.

`POSIX Message Queues` - очередь для сообщений формата POSIX с использованием приоритетов. Часть механизма связи между процессами. Нужно, если запускать программы написанные под этот формат, например с ОС Solaris.

`BSD Process Accounting` - поддержка дополнительных сведений о процессах (время запуска, владелец, командная строка запуска, использование памяти). Полезно для контроля процессов.


    [*] Auditing support
                 [*] Enable system-call auditing support
                 [ ] Make audit loginuid immutable

`Auditing support` - включение механизма проверки ядра. Например используется системой SELinux (система расширенной безопасности для Linux).

`Enable system-call auditing support` - включение системных вызовов для механизма проверки ядра.

    <*> Kernel .config support
Сохранять настройки ядра в нем самом. Это полезно, если у Вы удалите папку с исходниками ядра, а потом захотите немного изменить ядро.

    [*] Enable access to .config through /proc/config.gz

Если эта опция включена, вы сможете получать параметры текущего ядра из `/proc/config.gz`

Рекомендуется включить. Пригодится.


    [*] Control Group support  --->

               [ ] Example debug cgroup subsystem
               [*] Freezer cgroup subsystem
               [ ] Device controller for cgroups
               [*] Cpuset support
               [*] Include legacy /proc/<pid>/cpuset file
               [*] Simple CPU accounting cgroup subsystem
               [*] Resource counters
               [ ] Memory Resource Controller for Control Groups
               [ ] HugeTLB Resource Controller for Control Groups
               [ ] Enable perf_event per-cpu per-container group
               [*] Group CPU scheduler  --->
                     [*] Group scheduling for SCHED_OTHER
                     [ ] Group scheduling for SCHED_RR/FIFO
               [ ] Block IO controller

Поддержка группирования процессов. Используется такими подсистемами как CPUSETS, CFS, контроль памяти или устройства изоляции.

    -*- Namespaces support  --->

Позволяет двум процессам в разных виртуальных средах иметь один и тот же `pid`. Эта возможность делает реальными такие сценарии, как апгрейд сервера без необходимости его перезагрузки.

    -*- Kernel->user space relay support (formerly relayfs)

Включает поддержку интерфейса некоторых файловых систем (таких как debugfs). Предназначена для эффективного механизма передачи больших объёмов данных из пространства ядра в пользовательское пространство.

    [*] Initial RAM filesystem and RAM disk (initramfs/initrd) support

Поддержка initrd/initramfs.

Если собирается ядро без оных, следует отключить опцию.

    [ ] Optimize for size

Оптимизация кода ядра по размеру. Может быть полезно для создания загрузочных дискет. В обычных случаях не требуется.

    [ ] Profiling support

Включение расширенной поддержки профилирования (например, OProfile). Обычно не нужно.

##Enable loadable module support {#modules}

![loadable](http://3.bp.blogspot.com/-0nYTc8R2UEg/URjzyeN4GkI/AAAAAAAAD6w/MSQG9xGKxmA/s1600/module-support.jpg)

    [ ] Forced module loading
    [*] Module unloading
    [*] Forced module unloading
    [ ] Module versioning support
    [ ] Source checksum for all modules

Создание модульного ядра. `Module unloading` - возможность выгрузки модулей.

`Forced module unloading` - возможность принудительной выгрузки модуля, даже если оно еще нужно ядру


##Enable the block layer {#block_layer}

![block](http://2.bp.blogspot.com/-JYbKPuIuiUY/URkV2DrabvI/AAAAAAAAD9s/CJTpjqyt8p0/s1600/block.png)

Поддержка блочных устройств. Если эта опция отключена, некоторые файловые системы станут недоступны (например, ext3), SCSI и USB устройства не смогут распознаться.

    [*] Block layer SG support v4
    Partition Types  --->
              [*] Advanced partition selection
              [ ] Macintosh partition map support
              [*] PC BIOS (MSDOS partition tables) support
              [ ] BSD disklabel (FreeBSD partition tables) support
              [ ] SGI partition support
              [ ] EFI GUID Partition support

Следует выбрать из списка типы разделов, поддержка которых вам необходима. PC BIOS для машин с обычным BIOS (на разделах MBR), EFI GUID - EFI BIOS (на разделах GPT). В общем, ясно из названий.


##Processor type and features {#processors}

![processors](http://4.bp.blogspot.com/-acxZBgZhDrM/URjz-aUPpxI/AAAAAAAAD64/f2ycGH2KWxI/s1600/processor.jpg)

    [*] Symmetric multi-processing support

Поддержка симметричной мультипроцессорности. Включается в случае, если у вас многопроцессорный компьютер или многоядерный процессор.

    [*] Enable MPS table

Для старых систем SMP, которые не имеют надлежащей поддержки ACPI.

    [ ] Support for extended (non-PC) x86 platforms

Поддержка платформ, отличных от PC.

    [ ] Paravirtualized guest support  --->

Поддержка паравиртуализации (например, для Xen).

    Processor family (Core 2/newer Xeon)  --->

                   ( ) Opteron/Athlon64/Hammer/K8
                   ( ) Intel P4 / older Netburst based Xeon
                   (X) Core 2/newer Xeon
                   ( ) Intel Atom
                   ( ) Generic-x86-64

Следует выбрать тип своего процессора. Если не знаете или рассчитываете использовать созданную конфигурацию ядра на разных машинах, отмечайте Generic.

    [*] SMT (Hyperthreading) scheduler support

Включение технологии Hyperthreading.

    [*] Multi-core scheduler support

Для процессоров Intel Core, AMD Athlon64/Phenom.

    [ ] EFI runtime service support
    [ ] EFI stub support

Для поддержки UEFI. В данном примере она отключена.


##Power management and ACPI options {#power}

![power](http://2.bp.blogspot.com/-CP-A0xP_xYw/URj0FO2XwFI/AAAAAAAAD7A/IxYaxnx5UOE/s1600/power.jpg)

    [*] Suspend to RAM and standby

Поддержка Suspend to RAM - сохранение состояния операционной системы в оперативной памяти.

    [*] Hibernation (aka 'suspend to disk')
    ()  Default resume partition

Поддержка Suspend to Disk - иначе говоря, режим гибернации. Потребуется включение swap-раздела. В `Default resume partition` можно прописать путь к swap. Или оставить пустым с последующим внесением параметра resume в строку загрузчика. Лучше прописать к загрузчику.

    [*] ACPI(Advanced Configuration and Power Interface)Support --->
              <M> EC read/write access through /sys/kernel/debug/ec
              [ ] Deprecated /proc/acpi/event support
              <M> AC Adapter
              <M> Battery
              {M} Button
              {M} Video
              <M> Fan
              [*] Dock
              <M> Processor
              <M> Thermal Zone

Поддержка интерфейса управления конфигурацией и питанием (ACPI).

    CPU Frequency scaling  --->
              [*] CPU Frequency scaling
              < > CPU frequency translation statistics
              Default CPUFreq governor (ondemand)  --->
              -*- 'performance' governor
              < > 'powersave' governor
              < > 'userspace' governor
              -*- 'ondemand' cpufreq policy governor
              < > 'conservative' cpufreq governor

Управление настройками частоты процессора: `'performance'` governor обеспечивает наибольшую производительность, `'powersave'` governor будет стараться снижать частоту процессора, чем увеличит работу от батареи, `'ondemand'` - нечто среднее. Рекомендуется выбрать `'ondemand'` в качестве "умолчательного" в  `Default CPUFreq governor`.

##Bus options (PCI etc.) {#bus}

![bus](http://2.bp.blogspot.com/-i2YQe9Ga0iA/URj0I7HFtzI/AAAAAAAAD7I/Y-ZCDexB374/s1600/bus.jpg)

    [*] PCI support
    [*] Support mmconfig PCI config space access
    [*] PCI Express support
    < > PCI Express Hotplug driver
    [*] Root Port Advanced Error Reporting support

PCI support обеспечивает поддержку шины PCI.

    <*> PCCard (PCMCIA/CardBus) support  --->

Поддержка карт PCMCIA. Чаще всего встречаются на ноутбуках.

    <*> Support for PCI Hotplug  --->

"Горячее" (на лету) подключение PCI-устройств. Позволяет добавлять и удалять PCI-устройства, даже когда машина включена и работает. В принципе, можно и отключить, поскольку чаще всего эта возможность не используется.

##Executable file formats / Emulations {#emulations}

![exec](http://2.bp.blogspot.com/-9uhqcPjNg9k/URj0NwRzOxI/AAAAAAAAD7Q/yqIMRFiTgrc/s1600/emulations.jpg)

    [*] Kernel support for ELF binaries
    [*] Write ELF core dumps with partial segments
    <*> Kernel support for MISC binaries
    [*] IA32 Emulation


Поддержка формата исполняемых файлов ELF. Обязательна к включению.

##Networking support {#networking}

![net](http://4.bp.blogspot.com/-TEHPgDhBZ4g/USiyiph-I1I/AAAAAAAAEB0/IcFmfNEkRDA/s1600/network.png)

    Networking options  --->

В подпунктах включается поддержка протокола TCP/IP, в частности возможность включения/отключения IPv6. Поскольку автор не является специалистом в данной области, детально раздел не рассматривается. Сетевые администраторы, безусловно, найдут для себя множество полезных опций. Для домашнего же использования рекомендуется оставить опции по-умолчанию.

    < >   IrDA (infrared) subsystem support  --->

Скорее всего включать не понадобится. Обеспечивает поддержку инфракрасного модуля.

    < >   Bluetooth subsystem support  --->
                           Bluetooth device drivers  --->

Для тех, у кого встроен модуль беспроводной передачи данных bluetooth. Как правило, сейчас это ноутбуки. Хотя ранее bluetooth был достаточно популярен и соответствующие устройства покупались и использовались на настольных ПК.

Bluetooth device drivers позволит выбрать из списка поддержку определённого устройства.

    <M>   RF switch subsystem support  --->

Для ноутбуков, где, как правило, радиопередатчик wifi-чипа включается нажатием клавиши  "Kill Switch". Если эта клавиша не нажата и передатчик не включен, wi-fi не заведётся. Кстати, если параллельно у вас установлена Windows, обязательно оставьте под ней включенной кнопку wi-fi. В противном случае в linux при попытке включить интерфейс wlan вам будут объяснять, что Kill Switch отключен и включать его будет бесполезно.

    -*-   Wireless  --->
        <M> cfg80211 - wireless configuration API
            [*] cfg80211 wireless extensions compatibility

Поддержка стандарта 802.11 для беспроводных сетей.


##Device Drivers {#device}

![device](http://3.bp.blogspot.com/-pVZoCFTdLCE/URj0VtIET6I/AAAAAAAAD7g/UOTlDdAxh0A/s1600/device.jpg)

    Generic Driver Options  --->
                (/sbin/hotplug) path to uevent helper
                [*] Maintain a devtmpfs filesystem to mount at /dev
                [*] Automount devtmpfs at /dev, after the kernel mounted the ro
                [*] Select only drivers that don't need compile-time external fir
                [*] Prevent firmware from being built
                -*- Userspace firmware loading support
                [*] Include in-kernel firmware blobs in kernel binary
                () External firmware blobs to build into the kernel binary
                [ ] Driver Core verbose debug messages
                [*] Managed device resources verbose debug messages

`Maintain a devtmpfs filesystem to mount at /dev` - Монтировать файловую систему tmpfs.

`Select only drivers that don't need compile-time external fir` - выбирать лишь те драйверы, которые не требуют прошивки. В зависимости от вашего оборудования эту опцию, возможно, придётся отключить.

`Include in-kernel firmware blobs in kernel binary` - включить прошивку в ядро.

`External firmware blobs to build into the kernel binary` - требуется для указания пути к блобам.

Например:

    radeon/BTC_rls.bin radeon/CAICOS_mc.bin radeon/CAICOS_me.bin radeon/CAICOS_pfp.bin

Но в таком случае требуется включить в конфигурационный файл ядра строку с указанием директории, в которой находятся эти блобы:

    CONFIG_EXTRA_FIRMWARE_DIR="/lib/firmware"

Идём далее:

    < > Parallel port support  --->
     -*- Plug and Play support  --->

Первое уже вряд ли нужно. Но если у вас есть устройства ( раньше это были все принтеры ), требующие подключения по параллельному порту - включите опцию.

Plug and Play включаем.


    [*] Block devices  --->
                    <*> Loopback device support
                    <*> RAM block device support

Блочные устройства. `Loopback device support` включить обязательно.

`RAM block device support` нужен при сборке ядра с initrd, в противном случае - отключить: "выбирайте Y, если хотите использовать часть оперативной памяти как блочное устройство. В этом устройстве вы сможете создавать файловую систему, и использовать ее как обыкновенное блочное устройство (такое как жесткий диск). Обычно его используют для загрузки и сохранения минимальной копии корневой файловой системы при загрузке с флоппи диска, CD-ROM при установке дистрибутива, или на бездисковых рабочих станциях."

    Misc devices  --->

Просмотреть и принять решение включать или не включать то или иное устройство. У автора данный раздел вообще пуст.

    SCSI device support  --->
         -*- SCSI device support
        [*] legacy /proc/scsi/ support
        *** SCSI support type (disk, tape, CD-ROM) ***
        <*> SCSI disk support
        <*> SCSI CDROM support
        [*]   Enable vendor-specific extensions (for SCSI CDROM)
        <*> SCSI generic support
        [*] Verbose SCSI error reporting (kernel size +=12K)

Поддержка устройств SCSI. В современных машинах без включения этих опций могут быть не найдены такие устройства как жёсткий диск и CD-привод.

    <*> Serial ATA and Parallel ATA drivers  --->
                 [*] Verbose ATA error reporting
                 [*] ATA ACPI Support
                 [*] SATA Port Multiplier support
                 *** Controllers with non-SFF native interface ***
                 <*> AHCI SATA support

Поддержка устройств SATA. AHCI (Advanced Host Controller Interface) - механизм, позволяющий устройствам SATA пользоваться расширенными функциями.

    [ ] Multiple devices driver support (RAID and LVM)  --->

Опции, обеспечивающие использование логических томов и программных RAID-массивов.


    [*] Network device support  --->
                [*]   Ethernet driver support  --->
                <*>   PPP (point-to-point protocol) support
                USB Network Adapters  --->
                [*]   Wireless LAN  --->


В `Ethernet driver support` следует выбрать поддержку устройства вашей сетевой карты Ethernet. PPP может понадобиться тем, кто подключается к интернету с использованием соответствующего протокола. USB Adapters - при наличии у вас поднобного адаптера для выхода в сеть. Wireless LAN - для использования беспроводных сетей стандарта IEEE 802.11. Здесь нужно выбрать соответствующий вашему оборудованию драйвер.

    Input device support  --->

Нужен для определения различных устройств ввода как то: мыши, тачпады, тачскрины, джойстики, клавиатура и иные устройства. Предлагается немного побродить по списку и выбрать нужные опции.

    {*} I2C support  --->

Поддержка видео в Linux.

    <*> Multimedia support  --->
                [*]   Cameras/video grabbers support
                [*]   Media USB Adapters  --->
                       <*> USB Video Class (UVC)
                       [*] UVC input events device support

Поддержка веб-камер и захвата видео.  Нужно включить, если имеется встроенная камера или предполагается подключать камеру внешнюю.

    Graphics support  --->
        <*> /dev/agpgart (AGP Support)  --->
                <*>   AMD Opteron/Athlon64 on-CPU GART support
                <*>   Intel 440LX/BX/GX, I8xx and E7x05 chipset support

Включение поддержки AGP. В примере для видеокарт Intel и Radeon.

    [*] Laptop Hybrid Graphics - GPU switching support

Включается, если на машине более одной видеокарты.

    <M> Direct Rendering Manager

Включить DRM - Direct Rendering Manager. Современная вещь, рекомендуется.

    {*} Support for frame buffer devices  --->
               [*] Enable Video Mode Handling Helpers
               [*] Enable Tile Blitting Support
               [*] EFI-based Framebuffer Support

Управление поддержкой фреймбуфера. EFI-based Framebuffer Support нужен для систем с UEFI.

    Console display driver support  --->
               {*} Framebuffer Console support

Поддержка кадрового буфера в консоли. Включаем.

   [*] Bootup logo  --->
               [*]   Standard 224-color Linux logo

Включаем пингвинов при загрузке системы ;)

   <*> Sound card support  --->
               <*>   Advanced Linux Sound Architecture  --->

Включение поддержки звуковых устройств. Выбор своего железа из списка.

   [*] USB support  --->

Аналогично, только для USB-устройств.

   [*] X86 Platform Specific Device Drivers  --->

Имеет смысл посмотреть владельцам ноутбуков. Особенно тем, у кого не работает контроль яркости экрана или горячие клавиши. Для владельцев MXM видеокарт там же включить:

    <*> WMI Support for MXM Laptop Graphics


##Firmware Drivers {#firmware}

![firmware](http://1.bp.blogspot.com/-3Ils4rVfERs/URj0aMbsLUI/AAAAAAAAD7o/6uomYCkeb-4/s1600/firmware.jpg)

Для включения в ядро сторонних прошивок. Если вы не уверены, что вам нужны какие-либо опции, рекомендуется оставить вариант по-умолчанию.

##File systems {#filesystem}

![filesys](http://4.bp.blogspot.com/--w14rX6P998/URj0fdZaJOI/AAAAAAAAD7w/q3VRKtSfMHo/s1600/file_systems.jpg)

Осуществляет поддержку тех или иных файловых систем, поддержку квотирования, а также выбор нативных языков (вернее того, как будут отображаться символы). В целом, в комментариях не нуждается. Единственное замечание: если вы собираете ядро без initrd нужно включить используемые при загрузке файловые системы жёстко, а не модулями.


##Kernel hacking {#kernel_hack}

![kern_hack](http://4.bp.blogspot.com/-J7yzSpH6pwo/URj0kIAAWdI/AAAAAAAAD74/n7EhSw4roUA/s1600/kernel_hacking.jpg)

    [*] Magic SysRq key

Если компьютер завис и не реагирует на команды переключения консоли. Вы можете нажать `Alt-PrintScreen-s` для записи кеша дисков или `Alt-PrintScreen-i` (Убить все процессы за исключением init). Механизм нажатия такой: - Нажать `Alt` - Нажать `PrintScreen` - Отпустить `Alt` - Нажать нужную кнопку - Отпустить все.

    -*- Debug Filesystem

Когда эта опция включена, можно монтировать debugfs в `/etc/fstab`. Таким образом мы получим директорию `/sys/kernel/debug`, что очень небесполезно в частности для обладателей двух видеокарт.


##Security options {#security}

![secur](http://4.bp.blogspot.com/-uAfdUZl_GXY/URj0oFWuBLI/AAAAAAAAD8A/t-l_cw-uc3A/s1600/security.jpg)

Позволяет увеличить защищенность системы. Можно, например, запретить запуск программ с привилегиями root без специального ключа или с помощью системы SELinux ограничить возможности доступа к файлам самого root. Изменяйте эти опции только если вы знаете что делаете.


##Cryptographic API {#crypto}

![cryp](http://2.bp.blogspot.com/-6GG_ndYOcrs/URj0tE8KRuI/AAAAAAAAD8I/qwdxqJrLm94/s1600/crypto.jpg)

Опции шифрования. Пригодятся, если у вас имеются закодированные файловые системы. Так же как и с предыдущим пунктом: изменяйте эти опции только если вы знаете что делаете.


##Virtualization {#virtu}

![virt](http://3.bp.blogspot.com/-_heNGKvMZkM/URj0w0T1I1I/AAAAAAAAD8Q/Axf270kguus/s1600/virtualization.jpg)

    <M>  Kernel-based Virtual Machine (KVM) support
    <M>  KVM for Intel processors support
    < >  KVM for AMD processors support

Нужно включить, если планируется использовать виртуализацию (конкретно: VirtualBox или QEMU). В противном случае не отмечайте ничего.


##Library routines {#library}

![lib](http://3.bp.blogspot.com/-6RbJBv52P6Q/URj00UmIdMI/AAAAAAAAD8Y/UscvOhZbCac/s1600/library.jpg)

Используется для предоставления модулям функций CRC32 CRC32c. Можете включить


##Послесловие {#end}

Итак, настройка ядра закончена. Теперь коснёмся вопроса о сборке. Процесс сборки и установки ядра можно выполнить одной командой:

    :::console
    # make bzImage modules modules_install install

Когда ядро будет собрано, у Вас должны появиться следующие файлы:

    /boot/vmlinuz-3.6.11
    /boot/System.map-3.6.11
    /boot/initrd-3.6.11.img

и каталог модулей

    /lib/modules/3.6.11

И последним шагом подправим строки загрузчика, чтобы можно было загрузиться с новым ядром (пример для grub-legacy):

    :::sh
    # /boot/grub/menu.lst
    #
    default 0
    timeout 30
    splashimage=(hd0,1)/boot/grub/splash.xpm.gz
    title Linux 3.6.11
    root (hd0,1)
    kernel /boot/vmlinuz-3.6.11 root=/dev/ram0 real_root=/dev/sda3
    initrd /boot/initrd-3.6.11

Для тех, кому любопытно собрать ядро без initrd, милости прошу: [лишнему в ядре не место](http://alv.me/?p=58). Хотя и следуя представленным выше указаниям также можно собрать такое ядро. Но статья, приведённая по ссылке, позволит лучше понять зачем это нужно и нужно ли оно вообще.

Единственное, что там не указано: как в этом случае будут выглядеть настройки загрузчика. В них больше не будет указания на initrd - последней строки - и ram0:

    :::sh
    # /boot/grub/menu.lst
    #
    title Linux 3.6.11
    root (hd0,1)
    kernel /boot/vmlinuz-3.6.11 root=/dev/sda3


Если сборка не первая, вы увидите в `/boot` старое ядро, оно будет выглядеть как `vmlinuz-$KERNEL-VERSION.old`. В случае неудачной сборки, вы всегда можете загрузиться со старым ядром.

<b>P.S:</b> при указанном способе сборки в gentoo автоматически не появится initrd. Если он вам нужен, наиболее простой способ: после сборки ядра использовать для его создания `genkernel`:

    :::console
    # genkernel --install initramfs

<b>P.S2:</b> не забудьте добавить своего пользователя в соответствующие группы. Если нет звука, прежде всего проверьте, добавлен ли пользователь в группу `audio`, если не заводится камера - в группу `video`.

Да, надо бы ещё отметить, что при необходимости можно обратиться к документации ядра.
Располагаются эти файлы в каталоге `/usr/src/linux/Documentation`. Вот, вроде бы, и всё.
