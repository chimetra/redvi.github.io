Title: Оформление глав TeX/LaTeX
Date: 2013-07-06 08:15
Tags: LaTeX
Slug: title-latex
Author: redVi
Summary: Пара способов оформления глав в LaTeX

Достаточно любопытная вещь, которой просто невозможно не поделиться: [довелось наткнуться](http://texblog.org/tag/title-format/) на пару способов оформления главы в `TeX`. Здесь имеется ввиду то, как будет отображаться стиль названия главы, но не её содержимое. Можно использовать указанные ниже методы как в «голом» `TeX`, так и в `LaTeX`. Первый способ требует подключение пакета `fncychap`, второй — `titlesec` и ручного переопределения внешнего вида главы. Начнём с самого простого.

`Fncychar` позволит выбрать несколько различных стилей, красиво оформляющих наименование глав.

`~title.tex~`

    \documentclass[12pt]{report} % шрифт 12pt, тип документа report
    \usepackage[english, russian]{babel} % кодировка шрифтов
    \usepackage[utf8]{inputenc} % кодировка входного файла
    \usepackage[Glenn]{fncychap} % выбираем стиль Glenn
    \begin{document} % начало документа
    \chapter{Название главы}
    какой-то текст...
    \end{document} % конец документа

Для сборки документа в pdf вводим в консоли: `$ pdflatex title.tex`
На выходе получим:
При выбранном стиле `Glenn`

![glenn style](http://3.bp.blogspot.com/-7-QeZdH67fo/Uaxokosbm2I/AAAAAAAAE_E/Js8myZC9Ur0/s1600/Glenn.png 'glenn style')

Или при выбранном стиле `Rejine`

![rejine style](http://4.bp.blogspot.com/-AR3jMx17qLI/UaxowFugs5I/AAAAAAAAE_M/uvjfAAGvfkI/s1600/Rejne.png 'rejine style')

Всего имеется семь возможных стилей: `Sonny, Lenny, Glenn, Conny, Rejne, Bjarne, Bjornstrup`.

Пакет `titlesec` позволяет вносить изменения в стандартный стиль главы, то есть переопределять его.

`~title.tex~`

    \documentclass[12pt]{report}
    \usepackage[english, russian]{babel}
    \usepackage[utf8]{inputenc}
    \pagestyle{plain}
    \pagenumbering{roman}
    % Titlesec
    \usepackage{titlesec, blindtext, color} % подключаем нужные пакеты
    \definecolor{gray75}{gray}{0.75} % определяем цвет
    \newcommand{\hsp}{\hspace{20pt}} % длина линии в 20pt
    % titleformat определяет стиль
    \titleformat{\chapter}[hang]{\Huge\bfseries}{\thechapter\hsp\textcolor{gray75}{|}\hsp}{0pt}{\Huge\bfseries}
    \begin{document} % начало документа
    \chapter{Название главы}
    какой-то текст...
    \end{document} % конец документа

В итоге получим следующий стиль:

![titlesec](http://3.bp.blogspot.com/-g2JaRG1VXx8/Uax2pA4niEI/AAAAAAAAE_c/Zs6WM7iePjo/s1600/titlesec.png 'titlesec')

Теперь немного подробнее поговорим о том, что нами было использовано выше.
`pagestyle` поможет выбрать стиль оформления страниц документа, имеет несколько опций:

`empty` — не нумеровать страницы

`plain` — обычный номер страницы посередине

`headings` — присутствуют колонтитулы, включающие в себя и номера страниц

`myheadings` — то же, что и выше, но текст в колонтитулах не генерируется `LaTeX`, а задаются пользовательсике значения

`pagenumeric` задаёт стиль нумерации страниц, имеет несколько опций:

`arabic` — арабские цифры

`roman` — римские цифры

 `Roman` — римские большие цифры

`alph` — строчные буквы

`Alph` — прописные буквы

`\hspace[*]{length}` указание длины линии

`definecolor` позволяет использовать цвет в `LaTeX`, стандартные цвета:

* blue
* cyan
* green
* magenta
* red
* yellow

Помимо этого есть несколько вариаций для указания цвета. В заключение этой небольшой заметки даётся таблица, призванная помочь выбрать подходящий вариант.

<table border="1" cellpadding="0" cellspacing="0">
<tbody>
<tr>
 <td><b>TYPE</b></td>
 <td><b>VALUES</b></td>
 <td><b>EXAMPLE</b></td>
</tr>
<tr>
 <td>rgb</td>
 <td>red, green and blue values between 0 and 1</td>
 <td>\definecolor{dark_purple}{rgb}{0.4, 0.0, 0.4}</td>
</tr>
<tr>
 <td>RGB</td>
 <td>red, green and blue values between 0 and 255</td>
 <td>\definecolor{dark_purple}{RGB}{102, 0, 102}</td>
</tr>
<tr>
 <td>cmyk</td>
 <td>cyan, magenta, yellow and black values between 0 and 1</td>
 <td>\definecolor{dark_purple}{cmyk}{0.0, 1.0, 0.0, 0.6}</td>
</tr>
<tr>
 <td>HTML</td>
 <td>red, green and blue values in hex between 00 and FF</td>
 <td>\definecolor{dark_purple}{HTML}{660066}</td>
</tr>
<tr>
 <td>gray</td>
 <td>shades of gray between 0 and 1</td>
 <td>\definecolor{dark_grey}{gray}{0.3}</td>
</tr>
</tbody></table>

И — да — сегодня это всё.
