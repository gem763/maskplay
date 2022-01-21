"""
Django settings for home project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from decouple import config
# https://stackoverflow.com/questions/64208678/hiding-secret-key-in-django-project-on-github-after-uploading-project
# https://hwan-hobby.tistory.com/181


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'l9naapdhlj2wfi5e26u+urm_1sn28umx!0f3@v60hn_(33%)j+'
SECRET_KEY = config("SECRET_KEY")
KAKAO_JS_KEY = config('KAKAO_JS_KEY')
SLACK_BOT_TOKEN = config('SLACK_BOT_TOKEN')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']
APP = 'getch'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'imagekit',
    'django_json_widget',
    'getch',
    'moiberlab',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.naver',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.kakao',
    'custom_user',
    'rest_framework',
    'django_extensions',
    'debug_toolbar',
    # 'corsheaders',

    # 'vote',
    'siteflags',
    'notifications',
    'ordered_model',
    # 'friendship',
]

# 주피터노트북에서 장고 연결하려면 다음줄이 반드시 필요: 2020.08.07
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # https://pypi.org/project/django-currentuser
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


INTERNAL_IPS = ('127.0.0.1')

# CORS_ORIGIN_ALLOW_ALL = True

# 소셜로그인 기능 사용하기
# https://django-allauth.readthedocs.io/en/latest/installation.html#django
# https://ldgeao99.tistory.com/117

#486275532242770:2eb3cd8566851c0df80286f64e801edaf
#1331691227003429:eedf26d0e0df7b15784591d5eeabf513f:test
#Q60jbPX1POJFmqb0dgGl:5RnWiWQnmln
#671339125678-c9in180buoiu79t797tppifmm8qk24ja.apps.googleusercontent.com:JPgwwfpI5lnlC4M7IgqFaUpTg
#126234b4fe871fa3cd5ecabe9cce6001:k

SITEFLAGS_FLAG_MODEL = APP + '.Flager' #'getch.Flager'
AUTH_USER_MODEL = APP + '.User' #'getch.User'

# 소셜로그인시 request.session.session_key가 바뀌는걸 방지하기 위해
# 아래를 쓴다. 2021.02.15
# https://stackoverflow.com/questions/13978828/django-session-key-changing-upon-authentication
SESSION_ENGINE = APP + '.session_backend' #'getch.session_backend'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # Django 기본 유저모델
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email','public_profile'],
        # 'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'kr_KR',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.9' #'v.2.4'
    },

    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
LOGIN_REDIRECT_URL = 'discover'
# SIGNUP_REDIRECT_URL = 'profiler'
# ACCOUNT_LOGOUT_REDIRECT_URL = 'play'
ACCOUNT_LOGOUT_ON_GET = True

SITE_ID = 1
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
# ACCOUNT_UNIQUE_EMAIL = False


# ACCOUNT_FORMS = {'login': 'getch.forms.CustomLoginForm'}



# NOTIFICATIONS_NOTIFICATION_MODEL = 'getch.Notification'

ROOT_URLCONF = 'home.urls'

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

WSGI_APPLICATION = 'home.wsgi.application'


# Storage
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'sideb-proejct.appspot.com'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(BASE_DIR, 'data', 'sideb-proejct-0e33d8c0b0a9.json')


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


if os.getenv('GAE_APPLICATION', None):
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': '/cloudsql/sideb-proejct:us-central1:sideb-db',
            'USER': 'postgres',
            'PASSWORD': 'kkangse1',
            'NAME': 'postgres-sideb',
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': '127.0.0.1',
            'PORT': '5432',
            'NAME': 'postgres-sideb',      # sql 인스턴스에서 실제로 생성된 db 명칭 (인스턴스명 아님)
                                           # https://console.cloud.google.com/sql/instances/getchdb-001/databases?project=getch-245810
            'USER': 'postgres',            # sql 사용자계정 (IAM 서비스계정 아님)
                                           # https://console.cloud.google.com/sql/instances/getchdb-001/users?project=getch-245810
            'PASSWORD': 'kkangse1',
        }
    }



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_L10N = True
# USE_TZ = True

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
