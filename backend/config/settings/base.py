"""Settings comunes a todos los entornos.

La base de datos se lee del archivo .env en la raíz del repositorio
(el mismo que usa docker compose).

Hay dos conexiones a la MISMA base de datos, cada una con un usuario:

  default  -> obi_app    La usa la app (runserver, producción).
                         Lee y escribe datos; no puede crear ni alterar tablas.
  owner    -> obi_owner  Solo para cambiar la estructura:
                         python manage.py migrate --database=owner
"""

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # backend/
REPO_DIR = BASE_DIR.parent

env = environ.Env()
environ.Env.read_env(REPO_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])


def _database(user_var: str, password_var: str) -> dict:
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", default="obi"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
        "USER": env(user_var),
        "PASSWORD": env(password_var),
    }


DATABASES = {
    "default": _database("DB_APP_USER", "DB_APP_PASSWORD"),
    "owner": _database("DB_OWNER_USER", "DB_OWNER_PASSWORD"),
}

# Sin admin, sessions ni messages (ver ADR-0002).
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "core",
    "accounts",
    "clinics",
    "patients",
    "scheduling",
    "clinical",
    "attachments",
    "audit",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

AUTH_USER_MODEL = "accounts.Account"
AUTHENTICATION_BACKENDS = ["accounts.backends.CredentialBackend"]
PASSWORD_HASHERS = ["django.contrib.auth.hashers.Argon2PasswordHasher"]
# La unicidad del email está en un índice funcional (Lower) que este chequeo no ve.
SILENCED_SYSTEM_CHECKS = ["auth.W004"]

LANGUAGE_CODE = "es-mx"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
