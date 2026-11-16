# ADR-0007: Cifrado

- **Estado:** Aceptada
- **Fecha:** 2026-11

## Contexto

El expediente contiene datos sensibles de salud. Al mismo tiempo, la búsqueda del servidor necesita leer nombre, fecha de nacimiento y teléfono del paciente, y la validación de notas necesita leer `content_blocks`.

## Decisión

- TLS para datos en tránsito; cifrado en reposo para la base de datos y sus respaldos.
- Cifrado a nivel de campo solo para `account_credentials.mfa_totp_secret_encrypted`, en la aplicación, con una llave de KMS.
- Los adjuntos se cifran en el servicio de almacenamiento con una llave administrada por KMS (por ejemplo, S3 SSE-KMS).
- `content_blocks` queda como `jsonb` protegido por el cifrado en reposo. Nombre, fecha de nacimiento y teléfono del paciente no se cifran, porque la búsqueda depende de ellos; la búsqueda nunca lee el contenido de las notas.
- Adjuntos: solo los ve, sube o descarga el terapeuta con asignación activa al paciente, o el supervisor con supervisión vigente sobre el trainee asignado. Lo que sube el supervisor se guarda como `supervision_feedback`, separado del expediente. Cada descarga se registra en `audit_log`.

## Consecuencias

- La validación por bloques, su orden y el `content_hash` canónico siguen siendo simples.
- Si una institución exige protección contra acceso directo a la base, el cifrado de `content_blocks` a nivel de campo queda como mejora: la columna pasaría a `bytea` y `content_hash` se calcularía antes de cifrar.
