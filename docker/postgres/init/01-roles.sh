#!/usr/bin/env bash
# Crea los dos roles de Obi y deja resueltos sus permisos.
#
#   obi_owner  Propietario de la base de datos y de las tablas. Ejecuta las
#              migraciones y los tests (necesita CREATEDB para la base de test).
#   obi_app    Usuario con el que se conecta la aplicación. Recibe SELECT,
#              INSERT, UPDATE y DELETE sobre cada tabla que cree obi_owner,
#              sin poder crear ni alterar tablas.
#
# La restricción de audit_log (obi_app solo SELECT e INSERT) la aplica la
# migración de la app audit, porque la tabla todavía no existe aquí.
#
# Postgres ejecuta este script solo cuando el volumen de datos está vacío.
# Para volver a correrlo: docker compose down -v && docker compose up
set -euo pipefail

: "${OBI_OWNER_PASSWORD:?Falta OBI_OWNER_PASSWORD}"
: "${OBI_APP_PASSWORD:?Falta OBI_APP_PASSWORD}"

psql -v ON_ERROR_STOP=1 \
  --username "$POSTGRES_USER" \
  --dbname "$POSTGRES_DB" \
  -v db="$POSTGRES_DB" \
  -v owner_pw="$OBI_OWNER_PASSWORD" \
  -v app_pw="$OBI_APP_PASSWORD" <<'EOSQL'

-- Roles
CREATE ROLE obi_owner LOGIN CREATEDB PASSWORD :'owner_pw';
CREATE ROLE obi_app   LOGIN          PASSWORD :'app_pw';

-- obi_owner es dueño de la base. En PG15+ el esquema public pertenece a
-- pg_database_owner, así que obi_owner también queda como dueño de public.
ALTER DATABASE :"db" OWNER TO obi_owner;

-- Nadie más se conecta ni crea objetos por omisión.
REVOKE ALL ON DATABASE :"db" FROM PUBLIC;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

GRANT CONNECT ON DATABASE :"db" TO obi_owner, obi_app;
GRANT USAGE ON SCHEMA public TO obi_app;

-- Permisos de obi_app sobre todo lo que creen las migraciones de obi_owner.
-- Sin TRUNCATE, REFERENCES ni TRIGGER.
ALTER DEFAULT PRIVILEGES FOR ROLE obi_owner IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO obi_app;
ALTER DEFAULT PRIVILEGES FOR ROLE obi_owner IN SCHEMA public
  GRANT USAGE, SELECT ON SEQUENCES TO obi_app;

EOSQL

echo "obi: roles obi_owner y obi_app creados en la base $POSTGRES_DB"
