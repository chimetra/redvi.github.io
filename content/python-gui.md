Title: Сохранение файлов с python
Date: 2013-04-06 01:15
Tags: Python
Slug: python-gui
Author: redVi
Summary: В данном посте хотелось бы предложить написать небольшое приложение, использующее графический интерфейс.

В данном посте хотелось бы предложить написать небольшое приложение, использующее графический интерфейс. Задача выбора подходящего инструмента для осуществления этой задумки может оказаться достаточно нетривиальной. Python поддерживает несколько графических библиотек:

<b>- wxWidgest</b> и интерфейс к этой библиотеке &mdash; <b>wxPython</b>. Наилучший выбор, если вы хотите, чтобы ваши приложения выглядели в любой ОС с любым графическим интерфейсом как родные. Самый большой минус на момент написания поста &mdash; недостаточно широкая документация. Впрочем, кто-то может с этим не согласиться.

<b>- tkinter</b> &mdash; Tk &mdash; самая простая и распространённая библиотека. Используется очень широко. Документация подробна и содержит всё необходимое для быстрого начала работы.

<b>-PyQt</b> &mdash; интерфейс к библиотеке `Qt`. Эта библиотека также переносима на Linux, Windows и MacOS. Хотя стоит отметить, что интерфейс программы, естественно, будет отличаться от "родных" приложений и только в случае со связкой Linux+KDE будет выглядеть как влитой. Тем не менее используется очень широко. Документация отличная. В написании кода, пожалуй, наиболее сложен.

<b>PyGTK</b> &mdash; как и предыдущий привязан к своей оконной системе. Не так распространён как три библиотеки, данные выше.

Разумеется, графических библиотек намного больше. Указанные здесь &mdash; основные. Автором рекомендуется выбирать между `wxPython` и `Tkinter`. Дабы использовать какую-либо библиотеку, нужно её установить (исключением является разве что OS Windows, где python, похоже, поставляется в чуть ли не полной комплектации). Разбираемый сегодня пример будет задействовать библиотеку tkinter и потребует установки модуля `tk`. Пользователи Linux могут найти его с помощью своего пакетного менеджера или собрать python с ключом `tk` (для gentoo).

##Как это работает?

tkinter  &mdash; программный слой поверх `Tk`, позволяющий сценариям на языке Python обращаться к библиотеке `Tk`, конструирующей и настраивающей интерфейсы и возвращающей управление обратно в сценарии Python, которые обрабатывают события, генерируемые пользователем (например, щелчки мышью). Таким образом, обращения к  графическому интерфейсу из сценария Python направляются в tkinter, а затем в Tk; события, возникающие в графическом интерфейсе, направляются из Tk в  tkinter, а  затем обратно в  сценарий Python. <small>~Марк Лутц - программирование на Python 4 изд. I том~</small>


##Начали импорт

    :::python
    # pybackup.py
    #
    #! /usr/bin/env python
    # -*- coding: utf-8 -*-
    import os
    import shutil
    from tkinter.messagebox import *
    from tkinter.filedialog import *

модуль `os` представляет переносимый интерфейс к часто используемым службам операционной системы. Нами будет использован для указания пути (`os.path`);

`shutil` используется для таких операций над файлами как копирование, переименование, удаление;

импортирование модулей из `tkinter.filedialog` даст нам возможность вызывать диалоговые окна, из `messagebox`  &mdash; создавать сообщения, уведомления для пользователя

Функция выбора директории для копирования, получение доступа к описанию функции.


    :::python
    def savefiles():
        '''Ask where save your files'''
        global dst
        dst = askdirectory()
        print(type(dst))
        print(dst)


Прежде всего, никогда не стоит забывать документировать ваш код хотя бы для того, чтобы спустя некоторое время вы сами могли в нём разобраться. В примере сразу ниже функции даётся её краткое описание.

При импорте модуля можно будет обратиться к ней, вызвав команду `backup.savefiles.__doc__`  &mdash;  то есть `имя_модуля.имя_функции.__описание__` :

    >>> backup.savefiles.__doc__
    'Ask where save your files'

Полученный нами в итоге модуль не предназначен для расширения или импортирования, тем не менее строки документации создавать всё же нужно.

Далее используется переменная dst, которая впоследствии примет значение указанной пользователем директории. Значение будет строковым. Здесь переменная сделана глобальной поскольку должна быть доступна и другим функциям.

`dst = askdirectory()` - запросит у пользователя выбор директории для сохранения файлов

`print (type(dst))` и `print(dst)` будут выводить в консоли информацию для нас, дабы мы могли увидеть какой тип получился у переменной, когда пользователь выбрал директорию. Можно удалить строки с `print`.


Функция выбора файлов для бекапа и вложенная функция копирования выбранных файлов

    :::python
    def _selectfile():
        '''Select your files for backup'''
        src = askopenfilenames()
        src = list(src)
        print(type(src))
        print(src)
        def save():
            '''Save files'''
            for listcopy in src:
                listname = os.path.join(listcopy)
                shutil.copy(listname, dst)
            print("Backup file is OK")
        save()



`askopenfilenames` - выбрать файлы для копирования. Поскольку в итоге мы получим кортеж, а кортежи неизменяемы, сразу же конвертируем его в список: `list(src)`.

После выбора файлов вызывается функция для немедленного их копирования в указанную пользователем директорию. Для этого используется обход по списку и копирование с модулем `shutil`:


`shutil.copy` - скопировать

`listname` - файлы из списка

`dst` - куда копируем


Функция выбора директории и вложенная функция рекурсивного копирования

    :::python
    def _selectdirectory():
        '''Select your directory for backup'''
        src2 = askdirectory()
        print(type(src2))
        print(src2)
        def save2():
            '''Save directories and files'''
            print ("make backup " + src2)
            names = os.listdir(src2)
            if not os.path.exists(dst):
                 os.mkdir(dst)
            for name in names:
                srcname = os.path.join(src2, name)
                dstname = os.path.join(dst, name)
                if os.path.isdir(srcname):
                    shutil.copytree(srcname, dstname)
                if os.path.isfile(srcname):
                    shutil.copy(srcname, dstname)
            print("Backup is OK")
        save2()


`askdirectory` &mdash; выбрать директорию для копирования. В функцию включена проверка для рекурсивного копирования поддиректорий. Если `srcname` &mdash; поддиректория (`os.path.isdir`), будет выполнено рекурсивное копирование (`copytree`). Если в выбранная директория помимо поддиректорий содержит обычные файлы (`os.path.isfile`), копирование этих файлов (`copy`).

`os.listdir` - возвращает список, содержащий имя директории. Выбрать несколько директорий за раз нельзя (это ограничение связано с `askdirectory`, не с самим питоном), но можно повторно вызвать функцию копирования файлов и поддиректорий для следующей директории.

`os.path.join` - "склеивает" пути

Функция, закрывающая программу

    :::python
    def close_win():
         '''Close window and exit programm'''
         if askyesno("Exit", "Do you want to quit?"):
              root.destroy()


Функция, показывающая информационное окно

    :::python
    def about():
         showinfo("Backup", "This is simple backup programm.\n(test version)")


Tkinter

    :::python
    root = Tk()
    m = Menu(root)
    root.config(menu=m)

    fm = Menu(m)
    m.add_cascade(label="File",menu=fm)
    fm.add_command(label="Select directory for save", command = savefiles)
    fm.add_command(label="Select files for copy.",command=_selectfile)
    fm.add_command(label="Select directories for copy", command=_selectdirectory)
    fm.add_command(label="Exit",command=close_win)

    hm = Menu(m)
    m.add_cascade(label="Help",menu=hm)
    hm.add_command(label="About",command=about)
    txt = Text(root,width=40,height=25,font="22")
    txt.pack()

    root.mainloop()


`root = Tk()` &mdash; создать главное окно

`m = Menu(root)` &mdash; создать меню, привязанное к главному окну

`root.config(menu=m)` - для создания списка в меню (add_cascade)

`fm = Menu(m)` &mdash; создание пунктов в списке

Всё дальнейшее просто: `fm.add_command` &mdash; вызовет указанное действие; `label` &mdash; метка, то, как будет называться пункт меню; `command` &mdash; указание на функцию, которая должна быть выполнена при нажатии пунтка меню; `pack()` &mdash; менеджер расположения. Он отвечает за то, как виджеты будут располагаться на главном окне.

`root.mainloop()` &mdash; специальный обязательный метод. Без него главное окно не появится.

<p align="center"><iframe width="420" height="315" src="http://www.youtube.com/embed/1dgeYI7HvmY" frameborder="0" allowfullscreen></iframe></p>

##Что не так?

Если вам понятен приведённый пример, вы уже можете сказать, чего в нём не хватает. Например, вы можете обнаружить, что при повторном копировании объектов одной и той же директории, замена файлов происходит, а замена поддиректорий &mdash; нет. Вам лишь укажут на тот факт, что такая поддиректория уже существует и выполнение программы прекратится. В качестве самостоятельной работы предлагается изучить конструкцию `try-except` или модуль `errno` и проработать этот момент. Например:

    :::python
    def save2():
            '''Save directories'''
            try:
                print ("make backup " + src2)
                names = os.listdir(src2)
                if not os.path.exists(dst):
                     os.mkdir(dst)
                for name in names:
                    srcname = os.path.join(src2, name)
                    dstname = os.path.join(dst, name)
                    if os.path.isdir(srcname):
                        shutil.copytree(srcname, dstname)
                    if os.path.isfile(srcname):
                        shutil.copy(srcname, dstname)
                print("Backup is OK")
            except OSError:
                shutil.rmtree(dstname)
                print("Try again")
                if os.path.isdir(srcname):
                    shutil.copytree(srcname,dstname)
                if os.path.isfile(srcname):
                    shutil.copy(srcname,dstname)
                print("Backup is OK")
        save2()



В Windows копирование файла/файлов работать не будет: сие есть последствие  использования этой ОС не православных путей к файлам (обратный слэш). Возможно, пользователям Windows будет интересно изменить код таким образом, чтобы данная функция работала.

<b>Кстати:</b> чтобы программа в Windows запускалась при двойном клике, измените расширение на `.pyw`
Кроме того, предлагается поупражняться с tkinter и выводить всплывающее окно "Wait, please!" во время копирования (наподобие того, как это сделано при закрытии программы).

Для удобства файл целиком: [backup.py](https://gist.github.com/redVi/5029005)
