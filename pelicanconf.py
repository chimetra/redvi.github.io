# -*- coding: utf-8 -*-
from datetime import datetime

AUTHOR = 'redVi'
AUTHOR_URL = 'author/{slug}.html'
AUTHOR_SAVE_AS = 'author/{slug}.html'
ARCHIVES_SAVE_AS = 'archives.html'
REVERSE_ARCHIVE_ORDER = True
TAG_URL = 'tag/{slug}.html'
TAG_SAVE_AS = 'tag/{slug}.html'
CATEGORY_URL = 'category/{slug}.html'
CATEGORY_SAVE_AS = 'category/{slug}.html'
PAGE_URL = 'pages/{slug}.html'
PAGE_SAVE_AS = 'pages/{slug}.html'
ARTICLE_URL = 'articles/{slug}.html'
ARTICLE_SAVE_AS = 'articles/{slug}.html'
SITENAME = 'unix-lab.org'
SITESUBTITLE = u'блог об операционных системах, open source и программировании'
SITEURL = 'http://www.unix-lab.org'

TIMEZONE = 'Asia/Novosibirsk'

LOCALE = 'ru_RU.UTF-8'
DEFAULT_LANG = 'ru'

RELATIVE_URLS = False
GITHUB_URL = 'http://github.com/redVi'
DISQUS_SITENAME = 'redvinotes'
PDF_GENERATOR = False
REVERSE_CATEGORY_ORDER = False
THEME = 'storm'
CSS_FILE = 'screen.css'
OUTPUT_PATH = 'articles/'
PATH = 'content'
WITH_PAGINATION = True
DEFAULT_PAGINATION = 8
DEFAULT_DATE_FORMAT = '%d %B %Y'
ARTICLE_URL = 'articles/{slug}.html'
ARTICLE_SAVE_AS = 'articles/{slug}.html'
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

# Social Links
SOCIAL = (('rss', 'http://www.unix-lab.org/feeds/rss.xml'),
        ('github', 'http://github.com/redVi'),
        ('twitter', 'http://twitter.com/_redVi'),
        ('gplus', 'https://plus.google.com/105455094513485049642/about'),
        ('read to email', 'http://feedburner.google.com/fb/a/mailverify?uri=unix-lab&loc=ru_RU'),)

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
