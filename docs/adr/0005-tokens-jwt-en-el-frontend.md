# ADR-0005: Almacenamiento de tokens JWT e inactividad

- **Estado:** Aceptada
- **Fecha:** 2026-11

## Contexto

El brief exige bloqueo automático de sesiones inactivas. Registrar cada clic en la base (`last_activity_at`) agrega escrituras constantes sin necesidad.

## Decisión

- Access token en memoria, con vida de 5 minutos.
- Refresh token en una cookie `httpOnly`, `Secure`, `SameSite=Strict`, limitada a la ruta del endpoint de refresh; JavaScript no puede leerla. Dura unas horas (valor exacto en settings).
- Los refresh tokens rotan en cada uso y se revocan al cerrar sesión con la app `token_blacklist` de SimpleJWT, que agrega sus propias tablas.
- SimpleJWT no maneja cookies por sí solo: las vistas de login, refresh y logout se personalizan.
- La inactividad se controla en el frontend: tras `clinics.session_timeout_minutes` (15 por omisión) sin actividad, la app se bloquea y descarta el access token.

## Consecuencias

- La única información de sesión en el servidor es la blacklist de SimpleJWT.
- En desarrollo conviene que Vite reenvíe `/api` a Django, para trabajar en el mismo origen sin configurar CORS con credenciales. El flag `Secure` de la cookie debe ser configurable por entorno.
