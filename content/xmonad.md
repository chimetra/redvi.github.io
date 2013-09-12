Title: Знакомьтесь, xmonad
Date: 2012-10-23 11:15
Tags: Decorations
Slug: xmonad
Author: redVi
Summary: Установка, настройка и сипользование оконного менеджера Xmonad

##I. Вступление

Xmonad &mdash; фреймовый оконный менеджер, написанный на языке Haskell. Для приведения его к рабочему состоянию знать haskell совсем не обязательно, хотя уж точно не помешает. Об этом менеджере окон можно говорить очень долго, но пост предназначен по большей части для опытных пользователей и не ставит в круг своих задач объяснение простых истин.

Возгласы "я не новичок, но всё равно ничего не понял!" без рассмотрения отправляются в `/dev/null`. Тема достаточно объёмная и содержит несколько новых понятий, лучше объяснить не смогу.

##II. Начали:

###1. Как запустить?

Мы не сможем найти то, что ищем либо в репозитории community, либо в Arch User Repository. Пример того, как ставятся пакеты из AUR:

    :::console
    $ sudo yaourt -S xmonad xmonad-contirb

Вооружаемся каким-либо текстовым редактором (желательно с подсветкой синтаксиса) и приступаем к созданию xmonad.desktop: дело в том, что xmonad не добавится автоматически к вашему DM - прописываем вручную.

    :::sh
    # /usr/share/xsessions/xmonad.desktop:

    [Desktop Entry]
    Encoding=UTF-8
    Name=xmonad/>
    Comment=This session starts xmonad
    Exec=/usr/bin/xmonad
    Type=Application

Теперь при запуске с *DM (KDM, GDM, etc) появится выбор нашего рабочего окружения
Пока оно представляет собой... да, чистый рабочий стол. Минимализм во все поля.
Если для запуска вы используете `.xinitrc`, пропишите туда и xmonad.

    myStartupHook = do
        spawn "~/.xmonad/startup.sh"

Кстати-----------------------------------------------

Дефолтный файл конфигурации входит в состав xmonad. Можно скопировать его и отредактировать под свои нужды.

    :::console
    $ cp /usr/share/xmonad-0.10/man/xmonad.hs ~/.xmonad/

Если вдруг у вас не будет привилегий на редактирование файла, смените владельца и группу на свои:

    :::console
    $ sudo chown your_user xmonad.hs
    $ sudo chown :users xmonad.hs

---------------------------------------------------------


###2. Автозапуск программ

Что ж, давайте хотя бы прозрачность настроим. Для этого нужно стартовать при запуске графической среды compton, а как настроить этот самый запуск?

    :::console
    $ vim .xmonad/xmonad.hs:
    $ mkdir .xmonad
    $ vim .xmonad/startup.sh

    export LANG=ru_RU.UTF-8
    export MM_CHARSET=UTF-8
    setxkbmap -layout 'us,ru' -option 'grp:alt_shift_toggle, grp_led:caps'
    xsetroot -cursor_name left_ptr
    nitrogen --restore
    xfce4-power-manager &
    xfce4-volumed &
    xfce4-notifyd &
    xxkb &
    trayer -c &
    compton &

Как вы, должно быть, заметили в автозапуск добавлены элементы xfce. Они весят совсем немного, весь xfce ставить не требуют, зато значительно повышают комфортабельность работы. Например, notifyd будет оповещать нас о различных событиях:

![xfce-notyfyd](http://4.bp.blogspot.com/-lp6MTNSzwts/UIOWbjm2tnI/AAAAAAAAB8s/ziCGIMDonlQ/s1600/xfce4-notifyd.png)

Внимание! После любого изменения `xmonad.hs` нужно его скомпилировать, чтобы увидеть изменения:

    :::console
    $ xmonad --recompile
    $ xmonad --restart

Так уже лучше, верно? Мы указали, что являемся русскоязычными пользователями (`LANG=ru.RU`), включили переключение раскладок клавиатуры (`setxkbmap -layout`) и запустили несколько иных программ. Это по желанию. Подразумевается, что соответствующие программы у вас установлены. Если нет, просмотрите заметку о настройке openbox, где объясняется, какая программа за что отвечает.

Неплохо было бы сразу заставить работать мультимедийные клавиши. Здесь нам пригодится уже упомянутая [в заметке про openbox](openbox.html) программка xmodmap.

###3. Расположение окон

В файле `.xmonad.hs`

    :::haskell
    import XMonad.Layout.Circle
    import XMonad.Layout.Spacing
    myWorkspaces = ["1:main","2:net","3:work","4:media"]  ++ map show [5..9]
    myLayout = tiled ||| Mirror tiled ||| Full ||| Circle
        where
            -- default tiling algorithm partitions the screen into two panes
            tiled = spacing 5 $ Tall nmaster delta ratio
           -- The default number of windows in the master pane
           nmaster = 1
           -- Default proportion of screen occupied by master pane
           ratio = 2/3
           -- Percent of screen to increment by when resizing panes
           delta = 5/100


Full - в полный экран
Tall - экран делится на две части горизонтально
Mirror Tall - экран делится на две части вертикально
Circle - небольшие плавающие окна

Вот так выглядит компоновка Tall

<a href="http://farm8.staticflickr.com/7341/9260866503_17a1b961c2_b.jpg" data-lighter><img src="http://farm8.staticflickr.com/7341/9260866503_17a1b961c2_b.jpg"/></a>

Как привязать рабочий стол к определённой компоновке?

    :::haskell
    defaultLayouts = tiled ||| Mirror tiled ||| Full (и прочее, и так далее)
    myLayout = onWorkspace "1:main" Circle  $ onWorkspace "2:net" Full $ onWorkspace "3:work" simpleTabbed $ defaultLayouts
    myWorkspaces  = ["1:main","2:net","3:work","4:media"]  ++ map show [5..9]
    main = do
         xmproc <- spawnPipe "/usr/bin/xmobar /home/arch/.xmobarrc"
         xmonad $ defaultConfig{
         workspaces  = myWorkspaces
         , layoutHook =  avoidStruts $ myLayout
         }

Теперь при входе наши компоновки уже назначены:

- рабочий стол 1:main  -  компоновка Circle

- рабочий стол 2:net - компоновка Full

и так далее

###4. Горячие клавиши

Поскольку у автора сочетания завязаны на клавишу `win` (которую теперь можно смело заменить наклейкой с надписью "xmonad") - `modMask = mod4Mask` в `xmonad.sh`, то и сочетания клавиш соответствующие.

По умолчанию стоит другая комбинация `modMask = mod1Mask` - это левый alt.

Сочетание клавиш:

- `win + 1, win + 2, win + 3` - переход на рабочие столы.
- `win + space` - переключение компоновки рабочего стола (то есть то, как располагаются окна: Full, Circle...)
- `win + Tab` - переключение между окнами
- `win + левый клик` - перемещение окна
- `win + shift + c` - закрыть окно
- `win + shift + k` - поменять местами окно в фокусе и мастер-окно
- `win + shift + p` - запустить то или иное приложение
- `win + shift + q` - выйти из xmonad

Далее те горячие клавиши, которые настроит пользователь.

В полном конфигурационном файле, представленном ниже, это секция

    :::haskell
    additionalKeys,
        [, ((mod4Mask, xK_Return), spawn "konsole")
        , ((mod4Mask, xK_b), spawn "chromium")]


То есть `win + Return`, `win + b` и так далее. Формат записи: ((кнопка маскировки, xK_клавиша), spawn "приложение")

###5. Прикручиваем xmobar

    :::console
    $ vim .xmobarrc:

    Config { font = "-*-terminus-bold-r-*-*-14-*-*-*-*-*-*-*"
        , bgColor = "black"
        , fgColor = "grey"
        , position = TopW L 100
        , commands = [ Run Cpu ["-L","3","-H","50","--normal","green","--high","red"] 10
            , Run Memory ["-t","Mem: <usedratio>%"] 10
            , Run Swap [] 10
            , Run Date "%a %b %_d %l:%M" "date" 10
            , Run StdinReader
              ]
        , sepChar = "%"
        , alignSep = "}{"
        , template = "%StdinReader% }{ %cpu% | %memory% * %swap%  <fc=#ee9a00>%date%</fc>"
        }

xmobar будет иметь чёрный цвет, располагаться вверху, показывать нам заголовок открытого на данный момент окна и используемую компоновку рабочего стола, а также наименование рабочего стола.

В файле `.xmonad.hs` это строки:

    :::haskell
    import XMonad.Hooks.ManageDocks
    import XMonad.Util.Run(spawnPipe)
    main = do
        xmproc <- spawnPipe "/usr/bin/xmobar ~/.xmobarrc"
    { manageHook = manageDocks <+> manageHook defaultConfig
    , layoutHook =  avoidStruts $ myLayout -- avoidStruts чтобы окна --не загораживали xmobar
    { ppOutput = hPutStrLn xmproc
                         , ppTitle = xmobarColor "green" "" . shorten 50
                            }
    }


###6. Trayer

Небольшой симпатичный трей. В примере имеет ширину 60% экрана, расположен внизу по центру.
В файл `.xmonad/startup.sh` добавьте строки:

    trayer --edge bottom --align center --SetDockType true --SetPartialStrut true --expand true --width 60 --height 10 --transparent true --tint 0x000000 &

##В заключение:

Для нетерпеливых. Файл `.xmonad.hs`  (или стянуть [отсюда](https://github.com/redVi/dotfiles/blob/master/xmonad/xmonad.hs))

    :::haskell
    import XMonad
    import XMonad.Hooks.DynamicLog
    import XMonad.Hooks.ManageDocks
    import XMonad.Util.Run(spawnPipe)
    import XMonad.Util.EZConfig(additionalKeys)
    import System.IO
    import XMonad.Layout.PerWorkspace (onWorkspace)
    import XMonad.Layout.SimplestFloat
    import XMonad.Layout.Circle
    import XMonad.Layout.ThreeColumns
    import XMonad.Layout.Tabbed
    import XMonad.Layout.Accordion
    import XMonad.Layout.Grid
    import XMonad.Layout.IM
    import Data.Ratio ((%))
    import XMonad.Hooks.EwmhDesktops
    import qualified XMonad.StackSet as W
    import qualified Data.Map as M
    import Data.Monoid
    import System.Exit
    import XMonad.Layout.Spacing

    myWorkspaces = ["1:main","2:net","3:work","4:media", "5:chat" ] ++ map show [6..9]
    myLayout = onWorkspace "5:chat" pidginLayout $ onWorkspace "1:main" Circle $ onWorkspace "2:net" Full $ onWorkspace "3:work" simpleTabbed $ defaultLayouts
    --myNormalBorderColor = "#808080"
    --myFocusedBorderColor = "#414141"
    myFocusedBorderColor = "#395573"
    myNormalBorderColor = "#0080ff"
    myTerm = "konsole"
    myBorderWidth = 2
    myStartupHook = spawn "~/.xmonad/startup.sh"
    myManageHook = composeAll
         [ className =? "MPlayer" --> doFloat
         , className =? "Eclipse" --> doFloat
         , className =? "Eidete" --> doFloat
         , className =? "Gimp" --> doFloat
         , className =? "Pidgin" --> doShift "5:chat"
         , className =? "Pidgin" --> doFloat
         , className =? "arch - Skype™ (Beta)" --> doFloat
         , className =? "arch - Skype™ (Beta)" --> doShift "5:chat"
    , className =? "Ktorrent" --> doShift "1:main"]

    defaultLayouts = tiled ||| Mirror tiled ||| Full ||| Circle ||| simpleTabbed ||| ThreeCol 1 (3/100) (1/2) ||| ThreeColMid 1 (3/100) (1/2) ||| Accordion ||| Grid
    where
          -- default tiling algorithm partitions the screen into two panes
          tiled = spacing 5 $ Tall nmaster delta ratio

          -- The default number of windows in the master pane
          nmaster = 1
          nmaster2 = 2

          -- Default proportion of screen occupied by master pane
          ratio = 2/3

          -- Percent of screen to increment by when resizing panes
          delta = 3/100
    gridLayout = spacing 8 $ Grid
    pidginLayout = withIM (1%7)(Role "buddy_list") gridLayout

    main = do
        xmproc <- spawnPipe "/usr/bin/xmobar /home/arch/.xmobarrc"
        xmonad $ defaultConfig
            { manageHook = manageDocks <+> myManageHook <+> manageHook defaultConfig
    , borderWidth = myBorderWidth
    , normalBorderColor = myNormalBorderColor
    , startupHook = myStartupHook
    , focusedBorderColor = myFocusedBorderColor
            , terminal = myTerm
       , workspaces = myWorkspaces
    , layoutHook = avoidStruts $ myLayout -- avoidStruts чтобы окна не загораживали xmobar
       , logHook = dynamicLogWithPP $ xmobarPP
                            { ppOutput = hPutStrLn xmproc
                         , ppTitle = xmobarColor "green" "" . shorten 50
                            }
            , modMask = mod4Mask
            } `additionalKeys`
            [((mod4Mask, xK_Print), spawn "xfce4-screenshooter")
    , ((mod4Mask, xK_Return), spawn "terminal")
    , ((mod4Mask, xK_b), spawn "chromium")
    , ((mod4Mask, xK_f), spawn "firefox")
    , ((mod4Mask, xK_w), spawn "geany")
    , ((mod4Mask, xK_r), spawn "okular")
    , ((mod4Mask, xK_h), spawn "spacefm")
    , ((mod4Mask, xK_e), spawn "eclipse")
    , ((mod4Mask, xK_x), spawn "deadbeef")
            , ((mod4Mask, xK_i), spawn "pidgin")
            , ((mod4Mask, xK_c), spawn "cheese")
            ]

И, пожалуй, ссылки на хорошие статьи по теме: [№1](http://ro-che.info/docs/xmonad/), [№2](http://www.linuxandlife.com/2011/11/how-to-configure-xmonad-arch-linux.html#xmonad-layout-and-workspaces).

А так располагаются окна с компоновкой Circle

<a href="http://farm4.staticflickr.com/3822/9263651078_17ce45c263_b.jpg" data-lighter><img src="http://farm4.staticflickr.com/3822/9263651078_17ce45c263_b.jpg"/></a>

