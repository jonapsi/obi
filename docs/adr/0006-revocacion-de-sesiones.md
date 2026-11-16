# ADR-0006: Revocación de sesiones

- **Estado:** Aceptada
- **Fecha:** 2026-11

## Contexto

Un administrador debe poder forzar el cierre de sesión de alguien, pero el MVP no tiene una tabla de sesiones.

## Decisión

- Los refresh tokens se revocan en el servidor con la blacklist de SimpleJWT. Un cierre de sesión forzado surte efecto cuando expira el access token vigente, en 5 minutos como máximo.
- Fuera del MVP: lista de sesiones por dispositivo, límite de sesiones simultáneas e historial de accesos fuera de `audit_log`.

## Consecuencias

- Esas funciones requerirán una tabla `auth_sessions` después del MVP.
