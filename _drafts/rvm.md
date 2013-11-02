
Вводная часть

Что такое гем?
Что такое гемсет?



### Установка RVM

```console
$ \curl -L https://get.rvm.io | bash
Downloading RVM branch master
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                              Dload  Upload   Total   Spent    Left  Speed
100   124  100   124    0     0    107      0  0:00:01  0:00:01 --:--:--   120
100 1084k  100 1084k    0     0   234k      0  0:00:04  0:00:04 --:--:--  458k
* To start using RVM you need to run `source /home/user/.rvm/scripts/rvm`
```

Перезапускаем консоль.

```console
$ rvm -v
rvm 1.23.13
```

```console
# просмотреть все доступные для установки версии Ruby
$ rvm list known
# увидеть все установленные версии Ruby
$ rvm list
rvm rubies
=* ruby-1.9.3-p448 [ x86_64 ]
# => - current
# =* - current && default
#  * - default
```

### Использование разных версий ruby

```console
# установить несколько версий ruby
$ rvm install 1.9.3
$ rvm install 2.0.0
# переключиться на ruby 2
# и использовать 2 версию по-умолчанию
$ rvm use ruby-2.0.0-p247 --default
$ rvm list
   ruby-1.9.3-p448 [ x86_64 ]
=* ruby-2.0.0-p247 [ x86_64 ]

# => - current
# =* - current && default
#  * - default
```


Новый проект

Для примера создадим гемсет `jekyll`, где будут собраны всен нужные одноимённому генератору статических страниц гемы.

```console
$ source ~/.rvm/scripts/rvm # &laquo;включаем&raquo; rvm
$ rvm use 1.9.3@jekyll --create # создать гемсет
Using /home/user/.rvm/gems/ruby-1.9.3-p448 with gemset jekyll
$ rvm use 1.9.3@jekyll --default # выбирать его по-умолчанию
Using /home/redvi/.rvm/gems/ruby-1.9.3-p448 with gemset jekyll
$ gem install jekyll jekyll-tagging i18n # установка гемов
$ gem list # просмотр установленных в выбранном гемсете гемов
i18n (0.6.5)
io-console (0.3)
jekyll (1.2.1)
jekyll-tagging (0.5.0)
json (1.5.5)
liquid (2.5.3)
maruku (0.7.0)
```

Gemset'ы создаются для определённой версии ruby. Так, при переключении с одной версии на другую вы будете всегда видеть разный набор гемсетов: отображаются они также лишь для своей версии.

```console
$ rvm gemset list

gemsets for ruby-2.0.0-p247
   (default)
=> example
   global

$ cd workspace/jekyll
$ rvm gemset list

gemsets for ruby-1.9.3-p448
   (default)
   global
=> jekyll
```

Но здесь мы забежали чуть вперёд. Дело в том, что при переходе в директорию проекта, автоматически меняется версия ruby и набор gemset'ов, о чём речь пойдёт чуть ниже.

Gemset'ы можно удалять, очищать, экспортировать и импортировать гемы из одного в gemset'a в другой.
RVM предоставляет следующие команды для работы с gemsets:
create — создание нового gemset
export — экспорт списка гемов в файл default.gems
import — установка в текущий gemset списка гемов из файла default.gems
$ rvm gemset delete example --force # удалить gemset
Removing gemset example
empty — очистить gemset

Шпаргалка по основным командам RVM
2. rvmreset — перезагрузка RVM
3. rvm uninstall — удалить одну или несколько версию Ruby, оставив исходники
4. rvm implode — полностью удалить RVM (удаляет ВСЁ)

rvm list known — получить список всех версий ruby доступных для установки
rvm install 1.9.1 – установить ruby версии 1.9.1
rvm remove 1.9.2 – удалить ruby версии 1.9.2
rvm use 1.9.2 — переключиться на ruby версии 1.9.2
rvm use 1.9.2@rails3 --default — установить версию ruby 1.9.2 c gemset rails3 по умолчанию
rvm use system — использовать системную версию ruby
rvm list – список установленных версий ruby
rvm gemset list – список gemset'ов в выбранной версии ruby
rvm use 1.9.2@rails3 --create создать gemset rails3 для ruby версии 1.9.2
rvm gemset export — экспортировать гемсет в файл default.gems
rvm gemset import default.gems — установить gem's из списка в файле defaults.gem в текущий gemset


Задание окружения под отдельный проект с помощью .ruby-gemset

Как быть если у вас несколько проектов, каждый из которых используют разную версию gemset? Можно конечно переключиться между gemset'ами вручную с помощь rvm use {rubyversion}@{gemsetname}, но и тут RVM приходит нам на помощь, делая эту часть работы за нас.


Переключение между гемсетами
$ rvm gemset use global
Using ruby-1.9.3-p448 with gemset global
$ rvm gemset use jekyll
Using ruby-1.9.3-p448 with gemset jekyll


Окружение?
$ vim ~/workspace/jekyll/.ruby-gemset
jekyll
$ vim ~/workspace/jekyll/.ruby-version
ruby-1.9.3-p448

```console
$ cd workspace/ralis_projects/jekyll
$ rvm list

=> ruby-1.9.3-p448 [ x86_64 ]
 * ruby-2.0.0-p247 [ x86_64 ]

# => - current
# =* - current && default
#  * - default
```

Мы видим, что при переходе в директорию проекта, текющая версия ruby автоматически изменилась на указанную в `.ruby-version`.


