# Obi

Plataforma para que profesionales de salud mental gestionen citas y expedientes clínicos.

Monorepo:

- `backend/`: Django 5.2 + Django REST Framework 3.16 (Python 3.13)
- `frontend/`: React + TypeScript con Vite
- `docs/`: esquema SQL de referencia, brief y decisiones de arquitectura (ADR)

## Requisitos

- Git
- Docker Desktop (o Docker Engine con Compose)
- Python 3.13
- Node.js 22 LTS o más reciente

## Instalación

### 1. Clonar y configurar variables

```bash
git clone <url-del-repositorio> obi
cd obi
cp .env.example .env        # Windows: copy .env.example .env
```

Cambia las tres contraseñas de `.env`.

### 2. Levantar Postgres

```bash
docker compose up -d
```

La primera vez, el script `docker/postgres/init/01-roles.sh` crea dos usuarios:

| Usuario     | Para qué                                                                |
| ----------- | ----------------------------------------------------------------------- |
| `obi_owner` | Dueño de las tablas. Ejecuta migraciones y tests.                       |
| `obi_app`   | Usuario de la aplicación. Lee y escribe datos, no cambia la estructura. |

El script solo corre con el volumen vacío. Para empezar de cero: `docker compose down -v`.

### 3. Backend

```bash
cd backend
python3.13 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pre-commit install
python manage.py migrate --database=owner
python manage.py runserver
```

> **Importante:** las migraciones siempre llevan `--database=owner`.
> Sin esa opción, Django usa `obi_app`, que no puede crear tablas, y verás
> `permission denied for schema public`.

Tests:

```bash
python manage.py test --settings=config.settings.test
```

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

Abre http://localhost:5173. Las peticiones a `/api` se reenvían a Django en el puerto 8000.

## Calidad de código

`pre-commit` corre `ruff` (lint y formato) en cada commit. Para revisar todo el repositorio:

```bash
pre-commit run --all-files
```

## Documentación

- `docs/schema.sql`: esquema de referencia. Los cambios de esquema se hacen ahí primero.
- `docs/adr/`: decisiones de arquitectura.
