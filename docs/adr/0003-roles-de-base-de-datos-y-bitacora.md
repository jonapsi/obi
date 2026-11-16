# ADR-0003: Roles de base de datos y bitácora de solo inserción

- **Estado:** Aceptada
- **Fecha:** 2026-11

## Contexto

La normativa exige trazabilidad de los accesos y cambios al expediente. Implementar triggers criptográficos por fila en el MVP es complejo y pondría en riesgo el calendario del piloto.

## Decisión

- La bitácora (`audit_log`) se escribe en la capa de aplicación, desde middleware de Django y la capa de servicios (`audit.services.log_event`). `audit` es una app hoja: las demás apps llaman a su servicio y nunca a sus modelos.
- Dos roles de PostgreSQL:
  - `obi_owner`: dueño de la base y de las tablas; ejecuta migraciones y tests.
  - `obi_app`: usuario de la aplicación; `SELECT`, `INSERT`, `UPDATE` y `DELETE` sobre las tablas, sin poder crear ni alterar tablas.
- En `audit_log`, `obi_app` solo tiene `SELECT` e `INSERT`. Lo aplica la migración `audit/0002_restrict_obi_app`.

## Consecuencias

- El script `docker/postgres/init/01-roles.sh` crea los roles y usa `ALTER DEFAULT PRIVILEGES` para que cada tabla nueva de `obi_owner` quede disponible para `obi_app`.
- Django necesita dos juegos de credenciales: `migrate` y los tests con `obi_owner`; `runserver` con `obi_app`.
- Queda como mejora posterior: filas encadenadas con hash y triggers para una inmutabilidad más fuerte.
