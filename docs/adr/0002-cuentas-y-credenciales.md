# ADR-0002: Cuentas sin contraseña y credenciales separadas

- **Estado:** Aceptada
- **Fecha:** 2026-11

## Contexto

Los datos de perfil (`accounts`) y los secretos de autenticación deben vivir separados, para que un `SELECT` o un serializer sobre perfiles nunca pueda exponer el hash de la contraseña ni el secreto MFA. Django, por su parte, espera un modelo de usuario con campo `password`.

## Decisión

- `AUTH_USER_MODEL = "accounts.Account"`, configurado antes de la primera migración. `Account` se crea en `accounts/0001_initial`, como exige Django.
- `Account` hereda de `AbstractBaseUser`, elimina el campo heredado (`password = None`) y mapea `last_login` a la columna `last_login_at`.
- El hash (Argon2id) y el secreto MFA viven en `account_credentials`. Un backend propio, `accounts.backends.CredentialBackend`, verifica contra esa tabla.
- `PASSWORD_HASHERS` solo con `Argon2PasswordHasher`.
- No se usan `PermissionsMixin`, el Django Admin ni las sesiones de Django. Los permisos vienen de los flags de `ClinicMember` y la autenticación es solo por JWT.

## Consecuencias

- `INSTALLED_APPS` no incluye `admin`, `sessions` ni `messages`.
- Se silencia `auth.W004`, porque la unicidad del email está en un índice funcional que el chequeo de Django no detecta. El login usa `email__iexact`.
- Las tareas de administración de datos se hacen con comandos de gestión o la API, no con el Admin.
