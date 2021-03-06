# -*- coding: utf-8 -*-
# Django settings for Editores project.
import os
import sys


__author__ = 'Roberto Guimaraes Morati Junior <robertomorati@gmail.com@gmail.com>'
__copyright__ = 'Copyright (c) 2014 AutEnvLDG/AutoCoop/Nemo'
__version__ = '1.0.0'



if 'runserver' in sys.argv:
    DEBUG = True
else:
    DEBUG = False

#from statsd import statsd

ALLOWED_HOSTS = ['*']

#APPEND_SLASH=False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
#SESSION_EXPIRE_AT_BROWSER_CLOSE = True


TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.path.dirname(__file__)
#STATICFILES_DIRS = ( os.path.join(PROJECT_DIR,'static/'),)
#ICONES_URL = '../media/imagens/icones/'
CRISPY_TEMPLATE_PACK = 'uni_form'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, "../editores.db"),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-BR'

SITE_ID  = True

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

LANGUAGES = (
    ('pt_BR', ('pt_br')),
    ('en_US', ('en_us')),
)
DEFAULT_LANGUAGE = 1

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, '../staticfiles/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL of the login page.
#LOGIN_URL='/autenvldg/'

#datalog config
DATADOG_API_KEY = '429b85a4274f59adfeb8a438e3478d59'
DATADOG_APP_KEY = '0b3bfdd2d4adafe4b1c65fce58be58658c87fdf9'
DATADOG_APP_NAME = 'page.views'
DATADOG_APP_NAME = 'editores'
DATADOG_APP_NAME = 'editor_enredos'
DATADOG_APP_NAME = 'editor_missoes'
DATADOG_APP_NAME = 'editor_jogadores'
DATADOG_APP_NAME = 'editor_movimentos'
DATADOG_APP_NAME = 'editor_aventuras'


#STATSD_HOST = 'localhost'
#STATSD_PORT = 8125
#STATSD_PREFIX = None
#STATSD_MAXUDPSIZE = 512


#statsd.incr('page.views')



# Optionally, configure the host and port if you're running Statsd on a
# non-standard port.
#statsd.connect('localhost', 8125)

# Increment a counter.
#statsd.increment('page.views')

# Record a gauge 50% of the time.
#statsd.gauge('users.online', 123, sample_rate=0.5)



# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, "static"),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ttjzle-dgs#r!#uc*j5l&amp;(q++2%lg35$0=@b-z@ic=x%dmq*99'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

#TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(PROJECT_DIR, '../editor_objetos/templates/'),
#)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'datadog.middleware.DatadogMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',   
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

#Fix Json django 1.4 to django 1.6
SESSION_SERIALIZER = (
    'django.contrib.sessions.serializers.PickleSerializer')


CODEMIRROR_PATH = r"javascript/codemirror"

ROOT_URLCONF = 'editores.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'editores.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, "templates"),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
 
AUTH_PROFILE_MODULE = 'editores_objetos.Autor'


#instalação das aplicações
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'editores',
    'editor_objetos',
    'django.contrib.admin',
    'bootstrap_toolkit',
    'PIL',
    'imagekit',
    #'south',
    'rest_framework',
    'editor_enredos',
    'editor_missoes',
    'editor_jogadores',
    'editor_movimentos',
    'editor_aventuras',
    'bootstrap3', 
    'statsd',
    #'django_cleanup', # remove old files
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

#AUTHENTICATION_BACKENDS = (
#    'editores.auth_backends.CustomUserModelBackend',
#)

#CUSTOM_USER_MODEL = 'accounts.CustomUser'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


#rest framerwork
REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}


# Default settings
BOOTSTRAP3_DEFAULTS = {
    'jquery_url': '//code.jquery.com/jquery.min.js',
    'base_url': '//netdna.bootstrapcdn.com/bootstrap/3.1.1/',
    'css_url': None,
    'theme_url': None,
    'javascript_url': None,
    'javascript_in_head': False,
    'include_jquery': False,
    'horizontal_label_class': 'col-md-2',
    'horizontal_field_class': 'col-md-4',
    'set_required': True,
    'form_required_class': '',
    'form_error_class': '',
    'form_renderers': {
        'default': 'bootstrap3.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'bootstrap3.renderers.FieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
    },
}