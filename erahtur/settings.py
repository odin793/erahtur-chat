# Django settings for erahtur project.
# _*_ coding: utf-8 _*_;

from os import path

def rel(*args):
    return path.join(path.dirname(path.abspath(__file__)), *args)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('Stas Kotseruba', 'odin793@gmail.com')
)

MANAGERS = ADMINS
"""
DATABASES = {
    'default': {
        'ENGINE': 'sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': rel('erahtur_db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
"""
DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = rel('erahtur_db')
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru_RU'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = rel('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'f4u%-f)zbyr1@3u0ulkqr=*7ym3p$wc=ih7851=vv&lpaw6_q$'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    #'django.template.loaders.filesystem.Loader',
    #'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

#TEMPLATE_CONTEXT_PROCESSORS = (
    #"django.contrib.auth.context_processors.csrf",
    #'django.contrib.auth.context_processors.auth',
    #'village.views.login_processor',
#)

TEMPLATE_CONTEXT_PROCESSORS=(
	"django.core.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	#"work.publications.views.vacations_processor",
	#"work.publications.views.news_processor",
	"village.views.archive_processor",
	"village.views.login_processor",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
)


ROOT_URLCONF = 'erahtur.urls'

TEMPLATE_DIRS = (
    rel('templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TINYMCE_JS_URL = path.join(MEDIA_URL, 'js/tiny_mce/tiny_mce.js')
TINYMCE_JS_ROOT =  path.join(MEDIA_ROOT, 'js/tiny_mce')


TINYMCE_DEFAULT_CONFIG = {
    # 'plugins': "table,spellchecker,paste,searchreplace",
    "plugins": "safari",
    'theme': "advanced",
    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_toolbar_align': 'left', 
    'theme_advanced_buttons1' : "bold,italic,strikethrough,bullist,numlist," 
                                    "separator,undo,redo,separator,link,unlink,image," 
                                    "separator,cleanup,code,removeformat,charmap,"
                                    "fullscreen,paste",
    'theme_advanced_buttons2' : "",
    'theme_advanced_buttons3' : "",
}
TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = False

ACCOUNT_ACTIVATION_DAYS = 2

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    #'django.contrib.messages',
    'django.contrib.markup',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    #'registration',
    'tinymce',
    'village',
    'forum',
    'tagging',
)

FORCE_LOWERCASE_TAGS=True

AUTH_PROFILE_MODULE = 'village.UserProfile'

LOGIN_REDIRECT_URL='/'

AUTH_USER_EMAIL_UNIQUE = True
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'info@google.ru'

try:
    from settings_local import *
except ImportError:
    pass