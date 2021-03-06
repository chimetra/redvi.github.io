---
layout: post
title: Скринкасты в Linux
date: 2012-12-11 08:10
tags: [arch, linux]
slug: screencast
author: redVi
summary: В этом посте затронем тему записи скринкастов под linux. Будет рассмотрено несколько наиболее популярных утилит для захвата видео с монитора компьютера, также обратим внимание на их функционал, для одних детально, для других - поверхностно.
---

В этом посте затронем тему записи скринкастов под linux. Будет рассмотрено несколько наиболее популярных утилит для захвата видео с монитора компьютера, также обратим внимание на их функционал, для одних детально, для других &mdash; поверхностно.

Вообще, в linux не так много кандидатов, которые могут устроить нас по всем показателям. Как оказалось, найти адекватную программу для указанных целей достаточно проблематично. Выбраны несколько: старый добрый ffmpeg, небезызвестные XVidCap и recordMyDesktop, а также подающий надежды новичок &mdash; eidete.


## Начнём с ffmpeg.

Что он умеет и как это использовать в посведневной жизни:

"Склеивание" музыки и видео:

```console
$ ffmpeg -i son.wav -i video_origine.avi video_finale.avi
```

Замена одной звуковой дорожки на другую (например, более качественную):

```console
$ ffmpeg -i new.wav -i video.avi out.avi
```

Запись скринкаста (запись с монитора компьютера):

```console
$ ffmpeg -f x11grab -s 1366x768 -r 25 -b 1500 -bt 500 -aspect 1,3333 -sameq -i :0.0+0,0 -f alsa -async 1 -ac 2 -i hw:0,0 -acodec libmp3lame ~/MyVideo.avi
```

В этом примере будет записан также звук.

Перекодирование из одного формата в другой:

```console
$ ffmpeg -i video.avi -f webm video.webm
```

Извлечение аудиодорожки из видеозаписи:

```console
$ ffmpeg -i video.avi -f mp3 audio.mp3
```

Запись звука с микрофона:

```console
$ ffmpeg -f alsa -async 1 -ac 2 -i hw:0,0 -acodec libmp3lame sound.mp3
```

Создание gif-анимации из видео:

```console
$ ffmpeg -i video.avi animation.gif
```

Получить сведения о видео:

```console
$ ffmpeg -i video.avi
```

- Основные ключи:
    * i - входной файл
    * s - разрешение экрана для нашей записи
    * r - количество кадров в секунду
    * ac - количество каналов (для аудио)
    * qscale - регулировка уровня сжатия
    * bt - битрейт

Остальное можно найти в мануале - `man ffmpeg`. Там до вас даже постараются донести, как всё это работает:

![2](http://2.bp.blogspot.com/-B-a-5VgHZ08/UJE_alZqgEI/AAAAAAAACOI/5eqGThoy38s/s1600/ffmpeg-man.jpg)

<b>Кстати:</b>

Проверить поддерживаемые форматы файлов можно командой `ffmpeg -formats`


## Следующий кандидат - XVidCap

Кодирует на лету и имеет множество разных форматов. Автору не подошёл. Это тот редкий случай, когда всё вроде нормально, но субъективно что-то не нравится.

![1](http://4.bp.blogspot.com/-8nse0GdN634/UJEuVmbwfaI/AAAAAAAACMs/FAPlIKW0CUo/s1600/xvidcap.png)

## recordMyDesktop

Используют многие. Автору он не подошёл по причине непонятных фризов при записи ролика. Возможно, так отвратно он работает на отнюдь не топовом ноутбуке - нужно больше мощности?

Кроме того, recodrMyDesktop записывает файл в непотребном формате, который всё равно придётся перекодировать.

![3](http://1.bp.blogspot.com/-cLB_VdCYUUs/UJEuy146rxI/AAAAAAAACM0/2Pjw2AglwMs/s1600/recordmydesktop.png)

## eidete

Новая звезда. Запись сразу в формат `webm` - новый видеоформат для веба - весит мало, качество хорошее, взят под крыло компанией Google. Минималистичный, понятный интерфейс с достаточным количеством настроек. Увы, пока он находится в стадии глубокого альфа-тестирования и на archlinux автора корректно не заработал. Но пользователи ubuntu ликуют и разносят благую весть "наконец-то есть нормальная программа для захвата видео" по просторам Всемирной Паутины. Да, у eidete определённо есть будущее.

![4](http://4.bp.blogspot.com/-VXfGn9I7ktQ/UJExFs4LdlI/AAAAAAAACM8/oM7R2HmzEMo/s1600/eidete.png)

##  Как создать анимированный gif

Для этого отлично подходит программка `byzanz`. В официальных репозиториях её может и не быть. Пользователи Archlinux могут найти обсуждаемую деву в AUR.

Сам процесс записи выглядит примерно так:

```console
$ byzanz-record --duration=5 --delay=5 --x=500 --y=500 --width=800 --height=600 myGifFile.gif
```

где

```
--x/--y - точки координат
--width/ --height - ширина и высота экрана соответственно
--duration - задержка перед началом записи
--delay - продолжительность
```

![5](http://2.bp.blogspot.com/-PbkorsaKIPo/UM7NoUF5-5I/AAAAAAAADF8/kihDan3tTns/s1600/output.gif)

## Итог

Ну, что сказать, ffmpeg пока был и остаётся лучшим, хотя если вам нужно добавить звук в записанный ролик, лучше записать звуковую дорожку отдельно - в Audacity, а затем склеить с видео в другой программке - Avidemux. Не забывайте, Avidemux может многое.

Пример скринкаста, снятого в ffmpeg, в формате `webm`. Замечу, что один и тот же ролик в `.avi` и `.webm` имеет абсолютно разный вес. Рекорд автора: `.avi` - 70 MB, `.webm` - 12 MB. Впечатляет, не правда ли?

Увы, наш славный youtube тоже не любит больших файлов и кодирует их, но уже по-своему, их сжатие просто делает картинку размытой - никакой чёткости. Если вы знаете, как бороться с этой youtub'овской чертой - напишите мне.

<div class="video"><iframe width="560" height="315" src="http://www.youtube.com/embed/gXPwFHKkncI" frameborder="0" allowfullscreen></iframe></div>
