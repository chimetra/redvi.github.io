#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

from datetime import datetime

SITENAME = 'unix-lab.org'
SITESUBTITLE = u'блог об операционных системах, open source и программировании'
SITEURL = 'http://www.unix-lab.org'

AUTHOR = 'redVi'
AUTHOR_URL = 'author/{slug}/'
AUTHOR_SAVE_AS = 'author/{slug}/index.html'
AUTHORS_URL = 'authors/'
AUTHORS_SAVE_AS = 'authors/index.html'
ARCHIVES_URL = 'archives/'
ARCHIVES_SAVE_AS = 'archives/index.html'
ABOUT_URL = 'about/'
ABOUT_SAVE_AS = 'about/index.html'
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'
CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'
ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'

TIMEZONE = 'Asia/Novosibirsk'

LOCALE = 'ru_RU.UTF-8'
DEFAULT_LANG = 'ru'

RELATIVE_URLS = True
PDF_GENERATOR = False
REVERSE_CATEGORY_ORDER = False
THEME = 'storm'
CSS_FILE = 'screen.css'
OUTPUT_PATH = 'public/'
PATH = 'content'
WITH_PAGINATION = True
DEFAULT_PAGINATION = 6
DEFAULT_DATE_FORMAT = '%d %B %Y'
NEWEST_FIRST_ARCHIVES = False
METADATA = u'Блог об операционных системах, open source и программировании'

# Google analytics
# GOOGLE_ANALYTICS = 'UA-**'
# GOOGLE_ANALYTICS_DOMAIN = 'www.site-domain.org'

# Feeds
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
FEED_DOMAIN = 'http://www.unix-lab.org'
FEED_RSS = 'feeds/rss.xml'
FEED_ATOM = None
CATEGORY_FEED_ATOM = None
FEED_MAX_ITEMS = 3

#Pages
DISPLAY_PAGES_ON_MENU  = False
DIRECT_TEMPLATES = ('about', 'archives', 'authors', '404', 'index')

# Vars
GET_YEAR = datetime.now()
CURRENT_YEAR = GET_YEAR.year

# Plugins
PLUGIN_PATH = "plugins"
PLUGINS = ["sitemap", ]
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'weekly',
        'pages': 'monthly'
    }
}

# run pelican:
# pelican -s local_settings.py -o ./
