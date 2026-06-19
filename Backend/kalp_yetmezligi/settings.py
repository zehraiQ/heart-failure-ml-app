from pathlib import Path
import os


TEMEL_DIZIN = Path(__file__).resolve().parent.parent
PROJE_KOK = TEMEL_DIZIN.parent

GIZLI_ANAHTAR = os.getenv("GIZLI_ANAHTAR", "django-insecure-kalp-yetmezligi-ornek-gizli-anahtar")
HATA_AYIKLAMA = os.getenv("HATA_AYIKLAMA", "True").lower() == "true"
IZINLI_SUNUCULAR = os.getenv("IZINLI_SUNUCULAR", "*").split(",")
SECRET_KEY = GIZLI_ANAHTAR
DEBUG = HATA_AYIKLAMA
ALLOWED_HOSTS = IZINLI_SUNUCULAR

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "klinik",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "kalp_yetmezligi.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJE_KOK / "Frontend" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "kalp_yetmezligi.wsgi.application"
ASGI_APPLICATION = "kalp_yetmezligi.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": TEMEL_DIZIN / "veritabani.sqlite3",
    }
}

SIFRE_DOGRULAYICILARI = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
AUTH_PASSWORD_VALIDATORS = SIFRE_DOGRULAYICILARI

LANGUAGE_CODE = "tr-tr"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "statik/"
STATICFILES_DIRS = [PROJE_KOK / "Frontend" / "static"]
STATIC_ROOT = TEMEL_DIZIN / "statik_toplanmis"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Uretim ortaminda temel guvenlik basliklari otomatik devreye girer.
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_GUVENILIR_KAYNAKLAR", "").split(",") if os.getenv("CSRF_GUVENILIR_KAYNAKLAR") else []
