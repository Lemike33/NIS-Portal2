import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# Чтение SECRET_KEY из переменной окружения
# SECRET_KEY = 'django-insecure-^y!3b=14my@$3^78*d%2%l$op-h)@wk5-9-q=z)tp25ffnp80i'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-^y!3b=14my@$3^78*d%2%l$op-h)@wk5-9-q=z)tp25ffnp80i')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

DEBUG = bool(os.environ.get('DJANGO_DEBUG', True))

ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# LOGGING Settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    #  Формы записи сообщений
    'formatters': {
        'message_debug': {
            'format': 'время события:{asctime} - уровень:{levelname} - сообщение:{message}',
            'style': '{',
        },
        'time_level_path_message': {
            'format': 'время события:{asctime} - уровень:{levelname} - сообщение:{message} - путь:{pathname}',
            'style': '{',
        },
        'time_level_path_message_exc': {
            'format': 'время события:{asctime} - уровень:{levelname} - сообщение:{message} - путь:{pathname}: стэк ошибки:{exc_info}',
            'style': '{',
        },
        'general_log': {
            'format': 'время события:{asctime} - уровень:{levelname} - модуль:{module} - сообщение:{message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'message_debug',
        },
        'console_W': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'time_level_path_message',
        },
        'console_E': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'time_level_path_message_exc',
        },
        'general_log': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filters': ['require_debug_false'],
            'filename': 'general.log',
            'formatter': 'general_log',
        },
        'errors_log': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
            'formatter': 'time_level_path_message_exc',
        },
        'security_log': {
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'general_log',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'time_level_path_message',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'console_W', 'console_E', 'general_log'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['errors_log', 'mail_admins'],
            'propagate': True,
        },
        'django.server': {
            'handlers': ['errors_log', 'mail_admins'],
            'propagate': True,
        },
        'django.template': {
            'handlers': ['errors_log'],
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['errors_log'],
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security_log'],
            'propagate': True,
        },
    }
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_extensions',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'news',
    'django_filters',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.locale.LocaleMiddleware',

    'news.middlewares.TimezoneMiddleware',

    # 3 приложения кля полного кэширования сайта, в динамическом сайте так лучше не делать
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

ROOT_URLCONF = 'infoPortal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'infoPortal.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True  # Интернализация

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = '/accounts/login/'

# DEFAULT_FROM_EMAIL = 'lemikes33@yandex.ru'  # здесь указываем уже свою ПОЛНУЮ почту, с которой будут отправляться письма
SITE_ID = 1

LOGIN_REDIRECT_URL = 'articles-main'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_VERIFICATION = 'none'

# Для отправки писем email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'lemikes33'
EMAIL_HOST_PASSWORD = 'Vannistelroy+33'  # пароль приложений - доступен при подключенной двухфакторной аутентификации gmail

ACCOUNT_FORMS = {'signup': 'users.forms.BasicSignupForm'}

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER + '@yandex.ru'
SERVER_EMAIL = 'lemikes33@yandex.ru'  # это будет у нас вместо аргумента FROM в массовой рассылке

# Кэширование
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        # Указываем, куда будем сохранять кэшируемые файлы!создаем папку cache_files внутри проекта,
        # там где и manage.py!
    }
}

#  Запусти redis в power_shell: redis-server
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
