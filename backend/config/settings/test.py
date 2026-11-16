"""Settings para los tests.

Django crea una base de datos temporal (test_obi) para los tests, y obi_app
no tiene permiso para crear bases de datos. Por eso aquí la única conexión
usa obi_owner.
"""

from .base import *  # noqa: F403
from .base import DATABASES

DATABASES = {"default": DATABASES["owner"]}
