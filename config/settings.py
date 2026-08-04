import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    'mdeditor',

    'apps.users.apps.UsersConfig',
    'apps.courses.apps.CoursesConfig',
    'apps.projects.apps.ProjectsConfig',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.users.middleware.ActiveUserMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

MDEDITOR_CONFIGS = {
    'default': {
        'width': '100%',  # Redaktor kengligi
        'height': 500,    # Redaktor balandligi
        'language': 'en',
        'toolbar': [
            "undo", "redo", "|",
            "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
            "h1", "h2", "h3", "h4", "h5", "h6", "|",
            "list-ul", "list-ol", "hr", "|",
            "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime",
            "emoji", "html-entities", "pagebreak", "goto-line", "|",
            "help", "info", "||", "preview", "watch", "fullscreen"
        ],
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
        'image_folder': 'editor',  # media/editor/ papkasiga rasmlarni yuklaydi
        'theme': 'default',        # muharrir mavzusi
        'preview_theme': 'default', # ko'rish rejimi mavzusi
        'editor_theme': 'default',
        'toolbar_autofixed': True,
        'search_replace': True,
        'emoji': True,
        'tex': True,               # LaTeX (Matematik formulalar)ni yoqish
        'flow_chart': True,        # Sxemalar (Flowchart)
        'sequence_diagram': True,  # Ketma-ketlik diagrammalari
        'watch': True,             # Real-vaqt rejimida o'ng tomonda ko'rsatish
        'line_numbers': True,      # Kod qatorlari raqami
    }
}

LOGIN_URL = 'login'

LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')