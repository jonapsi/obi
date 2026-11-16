# ADR-0008: Expediente personalizable con bloques tipados

- **Estado:** Aceptada
- **Fecha:** 2026-11

## Contexto

El brief pide historias clínicas personalizables y herramientas modulares para las notas (análisis ABC, registros de ánimo, planes de intervención, metas, notas libres).

## Decisión

- `content_blocks` (`jsonb`) guarda una lista ordenada de bloques tipados tomados de un catálogo fijo definido en código.
- Cada tipo de documento declara sus bloques obligatorios y opcionales; Django valida cada bloque con su propio serializer y rechaza tipos desconocidos.
- En el MVP, personalizar significa elegir qué bloques opcionales usar y en qué orden. Las plantillas definidas por cada clínica y guardadas en la base quedan fuera del MVP.
- `schema_version` aumenta cuando cambia la forma de un bloque existente; agregar un tipo nuevo no lo requiere. Los documentos finalizados nunca se migran.

## Consecuencias

- La aplicación debe poder leer e imprimir todas las versiones pasadas de cada bloque.
- Pendiente: definir el catálogo de bloques por tipo de documento y los campos de cada bloque.
