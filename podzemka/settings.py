import dj_database_url
from django.core.exceptions import ImproperlyConfigured
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-podzemka-secret-key-change-me-in-production-0123456789",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

if not DEBUG and SECRET_KEY.startswith("dev-only"):
    raise ImproperlyConfigured("Задайте DJANGO_SECRET_KEY в переменных окружения")


def env_list(name, default=""):
    """Читает список из переменной окружения: "a,b,c" -> ["a", "b", "c"]."""
    return [item.strip() for item in os.environ.get(name, default).split(",") if item.strip()]


ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django_prometheus",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "venue",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "podzemka.urls"

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
                "venue.context_processors.site_info",
            ],
        },
    },
]

WSGI_APPLICATION = "podzemka.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=60,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Asia/Chita"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

if os.environ.get("DJANGO_STATIC_MANIFEST") == "1":
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"},
    }

UMAMI_WEBSITE_ID = os.environ.get("UMAMI_WEBSITE_ID", "")
UMAMI_SCRIPT_URL = os.environ.get("UMAMI_SCRIPT_URL", "http://localhost:3000/script.js")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_INFO = {
    "name": "Подземка",
    "tagline": "Банкетный зал в стиле лофт и андеграунд",
    "legal_name": "ИП Анисимов Игорь Владимирович",
    "domain": os.environ.get("SITE_DOMAIN", "podzemka.example"),
    "phone": "+7 (900) 123-45-67",
    "phone_raw": "+79001234567",
    "email": "hello@podzemka.example",
    "address": "улица Курнатовского, 17, Чита, Забайкальский край, 672027",
    "street": "улица Курнатовского, 17",
    "city": "Чита",
    "region": "Забайкальский край",
    "country": "RU",
    "postal_code": "672027",
    "hours": "Ежедневно, 12:00 — 02:00",
    "bar_secret": "Дайте ходу",
    "bar_discount": 14,
    "geo": {"lat": "52.035530", "lon": "113.493054"},
    "map_url": "https://yandex.ru/maps/?pt=113.493054,52.035530&z=17&l=map",
    "telegram": "https://t.me/podzemka_example",
    "vk": "https://vk.com/podzemka_example",
}

PROMO = {
    "title": "Выпускной в Подземке",
    "discount": 30,
    "host_name": "Гай Манукян",
    "host_photo": "img/tamada-gai-manukyan.jpg",
    "until": "2026-10-01",
    "until_human": "1 октября",
}
