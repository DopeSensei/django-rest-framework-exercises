from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent  # Proje kok dizini.


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

SECRET_KEY = 'django-insecure-%hjisw!0c0)bs&s9m#0e(#(=g54-#f+q2-d3+p%puk)0=5qrp#'  # Prod'da gizli tutulmali.
DEBUG = True  # Hata detaylarini gosterir; prod'da False olmali.
ALLOWED_HOSTS = []  # Prod ortaminda izin verilen domain/IP listesi.


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',  # gelistirme yardimci komutlari (shell_plus, graph_models)
    'api',  # senin uygulama app'in
    'rest_framework',  # DRF (API framework)
    'silk',  # profiling/performans araci
    'drf_spectacular',  # OpenAPI schema generator
    'django_filters'  # django-filter integration
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'silk.middleware.SilkyMiddleware',  # Silk icin middleware
]

ROOT_URLCONF = 'drf_course.urls'  # Proje seviyesinde URL dosyasi.

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

WSGI_APPLICATION = 'drf_course.wsgi.application'  # WSGI entrypoint.


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Lokal gelistirme icin sqlite.
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'  # Varsayilan dil.
TIME_ZONE = 'UTC'  # Varsayilan saat dilimi.
USE_I18N = True  # I18N aktif.
USE_TZ = True  # Timezone-aware datetime kullan.


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'  # Static dosyalarin URL prefix'i.

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Default PK tipi.
AUTH_USER_MODEL = 'api.User'  # Custom User modelini kullan.

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT auth
        'rest_framework.authentication.SessionAuthentication',  # Browser session auth
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # drf-spectacular schema uretimi
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],  # Query param filtreleme
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # Default pagination
    'PAGE_SIZE': 2  # Sayfa basina default kayit sayisi
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}

# Schema, API'nin kullanim kilavuzudur.
# Neden: endpoint'leri ve request/response formatlarini otomatik dokumante eder.
# drf-spectacular bu schema'yi otomatik olarak uretir.
