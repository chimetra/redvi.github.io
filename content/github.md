Title: GitHub и pastebin: что и зачем?
Date: 2012-11-27 1:15
Tags: Git
Slug: github
Author: redVi
Summary: Зачем и кому могут пригодиться сервисы GitHub и Pastebin

Сегодня поговорим о сотрудничестве и личной выгоде. В жизни бывает немало ситуаций, когда нужно выложить плоды своих ночных бдений в место, где они уже не смогут потеряться. Например, хранили вы свои наработки на жёстком диске, долго и с интересом записывали нестандартные решения, но однажды - бывает и так - ноутбук ваш упал в бассейн и восстановлению не подлежит, а вместе  с ним и все важные данные, и резервной копии нет к тому же. Что бывает гораздо чаще, вам стало нужно делиться своими скриптами, а может, даже проектами с другими людьми. Ясно, что в нашей повседневной жизни люди эти могут быть от вас за много километров. Собственно, поэтому нам и пригодятся сервисы, о которых пойдёт речь.

Автором выбраны всего два сервиса. Оба хороши по-своему, и по-своему нужны.

## Pasetebin

<u>Что?</u>

Сервис, позволяющий загружать куски кода. Имеется подстветка синтаксиса самых разных языков программирования.

<u>Зачем?</u>

Часто требуется выложить вывод терминала или же исходный код какого-либо скрипта, дабы другие пользователи ( на форумах, IRC, IM ) могли оценить ваш труд или же помогли вам решить какую-то проблему.

![pastebin](http://1.bp.blogspot.com/-6Djgk994zKw/UJIkYv4NJTI/AAAAAAAACSU/QFvmgKLb2DU/s1600/pastebin.png)

<b>Пример:</b>

У вас возникли трудности с настройкой графики под linux. Вы выкладываете лог Xorg'а, дабы вам помогли решить проблему. Или же вы захотели поделиться вашими настройками conky. Если код достаточно большой, лучше использовать pastebin.

- Очень удобно:
    * не нужно специально регистрироваться для того, чтобы пользоваться сервисом. Достаточно иметь аккаунт в социальной сети, с помощью которого можно осуществить вход.
    * можно указать время, по истечении которого, файл будет удалён

## GitHub

<u>Что?</u>

Популярный веб-сервис для хостинга проектов и их совместной разработки. В последнее время обогнал по популярности даже sourceforge.

<u>Зачем?</u>

Тут уже может быть много мотивов. Вообще, как указано выше, используется для совместной разработки проектов. Но очень часто и одиночки хранят на github свои файлы: конфигурации `.vim`, `.bahsrc`, `wmii` ;) автора к использованию данного сервиса подтолкнуло простое любопытство.
Регистрация обязательна. После первого входа нам предложат создать репозитарий и объяснят как это сделать.

![git init](http://2.bp.blogspot.com/--KE9OT61Wgc/UIY0wO64bLI/AAAAAAAAB_w/8szrtcrhSp0/s1600/github.png)

Заходить на github можно как по http, так и с помощью ssh. Рассмотрим второй вариант подробнее.
Установим openssh:

```console
$ pacman -S openssh
```

Сгенерировать ключи:

```console
$ ssh-keygen -t rsa -C "user@host.com" # для github это будет ваша электронная почта
```

После чего вам нужно будет ответить на несколько вопросов по созданию директорий. Passphrase оставим открытым.

![ssh](http://3.bp.blogspot.com/-9TzD6mi3ehQ/UIY0jHHELnI/AAAAAAAAB_o/t4XwLRrg6vY/s1600/ssh.png)

Создаст директорию `~./ssh/id_rsa & ~/.ssh/id_rsa.pub`

Открываем github, логинимся - Настройки аккаунта - SSH - вводим содержимое своего паблика, подтвержаем запрос.

![ssh github](http://3.bp.blogspot.com/-EWedxNNAuc0/UIY03kO9UmI/AAAAAAAAB_4/VuMk0hpbl6Q/s1600/ssh-key.png)

```console
$ ssh git@github.com
Hi redVi! You've successfully authenticated, but GitHub does not provide shell access.
Connection to github.com closed
```

Что ещё:

```console
$ git clone git@github.com:redVi/bash.github # скачиваем каталог в свою \ домашнюю директорию
$ cd bash/                                   # переходим в каталог
$ cp /home/arch/.bashrc /home/arch/bash/`    # копируем нужный файл (или создаём его)
$ git add .bahsrc                            # добавляем файл на github
$ git commit -m "my general bash config" .bashrc # вносим комментарии
$ git push -u origin master                  # обновляем (в последующем просто git push -u)
```

![repo](http://2.bp.blogspot.com/-DxxN2zljafg/UIY1ALoyTtI/AAAAAAAACAA/1Fbum3I1kOE/s1600/github-files.png)

Если вы хотите выложить проект, рекомендую ознакомиться [с дополнительными материалами](http://githowto.com/ru).

### Как удалить файл или директорию из индекса

```console
$ git reset file - отменить коммиты
$ git rm file - удалить сам файл
$ git commit -a -m "delete some files" - закоммитить изменение
$ git push - отправить изменения
```

### Список часто используемых команд git

```console
# снимок всех файлов перед глобальными изменениями
git init
git add .
git commit -m "commit"
# восстановить предыдущую версию
git reset --hard
# и сохранить её состояние
git commit -a -m "commit"
# добавить новый файл
git add file
# забыть о файлах
git rm file
git rm -r directory/
# удалить старое имя файла и добавить новое
git mv file1 file2
# список последних коммитов
git log
# восстановление состояния до указанного коммита
git reset --hard 3456
# где 3456 - хеш нужного коммита
# восстановить файлы и каталоги
git checkout 3456 file1 file2
# создать список изменений
git log > ChangeLog
# получить копию проекта
git clone git://path/to/project.git
# обновить до последней версии
git pull
# последние изменения
git diff
# отправить изменения
git push git://path/to/project.git
# создание форка проекта
git clone git://path/to/project.git
# просмотр всех веток
git branch
# исправить введенный коммит
git commit --amend
# добавить изменения в коммит
git commit --amend -a
# изменить последние 10 коммитов
git rebase -i HEAD~10
# теперь если коммит отмечен для исправлений
git commit --amend
# если нет
git rebase --continue
# удалить файл из всех ревизий
git filter-branch --three-filter 'rm file' HEAD
# кто редактировал файл
git blame file
# указать данные для репозитария --global - для всего, полностью
git config --global user.name "John Johnson"
git config --global user.email "john@example.com"
# создать пакет из репозитария
git bundle create file HEAD
# восстановить коммиты из репозитария
git pull file
# применить патч
git apply < your.patch
# обновить адрес перенесенного репозитария
git config remote.origin.url git://new.url/project.git
# создание tarball с исходниками
git archive --format=tar --prefix=project/ HEAD
# указать все каталоги проекта сразу
git add .
git add -u
git commit -a
# внести несколько коммитов для новых участко кода
git add -p
git commit
# автоматически сделать коммиты
git commit --interactive
```
