import os
from pathlib import Path

import dj_database_url
from decouple import config
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(os.path.join(BASE_DIR, ".env"))
ENVIRONMENT = os.environ.get("ENVIRONMENT", "").strip().lower()

if ENVIRONMENT == "local":
    load_dotenv(os.path.join(BASE_DIR, ".env.local"), override=True)
elif ENVIRONMENT == "prod":
    load_dotenv(os.path.join(BASE_DIR, ".env.docker"), override=True)

# Security
SECRET_KEY = "django-insecure-1k0rswl8wlff&ov#7n@7kbk(+0453tpsre-gj(w!_+n2ye+8ey"
DEBUG = True
ALLOWED_HOSTS = []

# Installed Apps
DJANGO_APPS = [
    "daphne",  # for ASGI
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.postgres",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",
    "channels",
]

THIRD_PARTY_APPS = [
    "django_extensions",
    "tailwind",
    "theme",
    "django_browser_reload",
    "widget_tweaks",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "anymail",
]

PROJECT_APPS = [
    "app.apps.MyAppConfig",  # Update if named differently
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "192.168.65.1"]

# URLs / ASGI / WSGI
ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"), conn_max_age=600
    )
}

# Custom User
AUTH_USER_MODEL = "app.UserProfile"

# Authentication
AUTHENTICATION_BACKENDS = ["allauth.account.auth_backends.AuthenticationBackend"]

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "account_login"

ACCOUNT_LOGIN_METHODS = {"email", "username"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
SITE_ID = 1

# Email
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
ANYMAIL = {
    "SENDGRID_API_KEY": config("SENDGRID_API_KEY"),
}
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Tailwind
TAILWIND_APP_NAME = "theme"

# Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "theme/static",
    BASE_DIR / "theme/static_src/src",
]

# Auto field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
