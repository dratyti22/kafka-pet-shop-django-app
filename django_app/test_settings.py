# django_app/test_settings.py
from pathlib import Path

# Базовые пути
BASE_DIR = Path(__file__).resolve().parent

# Базовые настройки Django
SECRET_KEY = 'django-insecure-test-key-1234567890'
DEBUG = False
ALLOWED_HOSTS = ['*']

# ДОБАВЬТЕ ЭТИ НАСТРОЙКИ ↓
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "django.contrib.postgres",
    "django.contrib.sites",

    "rest_framework",
    "corsheaders",
    "mptt",

    'src.user.apps.UserConfig',
    "src.product.apps.ProductConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_app.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_db.sqlite3',
    }
}

# Настройки для тестов
AUTH_USER_MODEL = 'user.User'
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 16,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'src.services.jwt_auth.JWTAuthentication',
        "rest_framework.authentication.SessionAuthentication"
    ],
}

# Ускоряем тесты
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# ДОБАВЬТЕ ЭТУ СТРОЧКУ ↓
SITE_ID = 1
