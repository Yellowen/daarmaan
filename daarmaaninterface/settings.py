# -----------------------------------------------------------------------------
#    Daarmaan - Single Sign On Service for Yellowen
#    Copyright (C) 2012 Yellowen
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------

import os

ROOT = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sameer Rahmani', 'lxsameer@gnu.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'daarmaaninterface/database/db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
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
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/statics/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(ROOT, "statics/auto/")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/statics/auto/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(ROOT, "statics/").replace("\\", "/"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'miin((zb8=x7!2n$48!j+to&amp;&amp;pnj)2khye9&amp;khh=g+ik3a#j(8'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'daarmaaninterface.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'daarmaaninterface.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(ROOT, "templates/").replace("\\", "/"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    "vanda.core",
    'daarmaan.server',
    'vanda.apps.dashboard',
)

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
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'general': {
            'handlers': ['console'],
            'level': 'DEBUG',
            }
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    # Project information contexts
    "daarmaaninterface.projinfo.info",
    "vanda.apps.dashboard.context_processors.dashboard",

)

# Daarmaan Version.
VERSION = "0.5.31"

# Session will not expired with browser close
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1209600
## SESSION_COOKIE_DOMAIN =  ".yellowen.com"
## CSRF_COOKIE_DOMAIN = "yellowen.com"
## SESSION_COOKIE_NAME = "sessionticket"

LOGIN_URL = "/"
LOGOUT_URL = "/logout/"

# Vakhshour configuration
VAKHSHOUR = {
    "host": "127.0.0.1",
    "port": "8888",
}


EMAIL_VERIFICATION = False

try:
    import smtp_settings

    EMAIL_HOST = smtp_settings.EMAIL_HOST
    EMAIL_PORT = smtp_settings.EMAIL_PORT
    EMAIL_HOST_USER = smtp_settings.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = smtp_settings.EMAIL_HOST_PASSWORD
    EMAIL_USE_TLS = smtp_settings.EMAIL_USE_TLS
    EMAIL = smtp_settings.EMAIL

except ImportError:
    pass


DASHBOARD_CONFIG = {
    "blocks": {"header": {"title": "header",
                          "class": "HorizontalBar",
                          "order_matters": True,
                          "css": "/statics/css/header.css"},
               "body": {"title": "Dashboard",
                        "class": "WidgetArea",
                        "css": ["/statics/css/widgetarea.css",
                                "/statics/css/masonry.css"],
                        "js": "/statics/js/masonry.js"},
               "footer": {"title": "footer",
                          "class": "HorizontalBar",
                          "css": "/statics/css/footer.css"},
               },
    "css": ["/statics/css/dashboard.css",
            "/statics/css/fonts.css"],
}
