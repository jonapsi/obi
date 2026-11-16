# ADR-0001: Esquema de referencia: el documento SQL manda

- **Estado:** Aceptada
- **Fecha:** 2026-11

## Contexto

El esquema de Obi pasó por un borrador DBML (schema v2) y por OBI.sql antes de la decisión de usar Django. Ese borrador no incluía el stack de Django, los roles trainee y supervisor, los adjuntos de pacientes ni los tokens de un solo uso. Hace falta una sola fuente de verdad para la base de datos.

## Decisión

- El esquema definitivo es `docs/schema.sql` (exportado del documento SQL del proyecto): DDL de PostgreSQL con restricciones, índices, permisos y comentarios de columna.
- Todo cambio de esquema se hace primero en ese archivo; los modelos y migraciones de Django lo siguen.
- La base que generan las migraciones debe ser equivalente al SQL. Diferencias aceptadas: `CHECK` en lugar de `ENUM` (TextChoices), índice funcional sobre `Lower(email)` en lugar de citext, índices extra que Django crea por cada ForeignKey, y llaves foráneas compuestas `(clinic_id, …)` agregadas con `RunSQL`.

## Consecuencias

- Para verificar: aplicar las migraciones en una base vacía, exportar con `pg_dump --schema-only` y comparar con `docs/schema.sql`.
- El borrador DBML v2 y el documento "MVP Trade-Offs and Future Roadmap" (diseño NestJS) quedan obsoletos y no se incluyen en el repositorio.
