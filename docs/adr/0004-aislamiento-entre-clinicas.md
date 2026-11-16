# ADR-0004: Aislamiento entre clínicas en la capa de servicios

- **Estado:** Aceptada
- **Fecha:** 2026-11

## Contexto

Obi es multi-clínica: una cuenta puede pertenecer a varias clínicas a través de `clinic_members`, y los datos clínicos de una clínica no deben ser visibles desde otra. PostgreSQL Row-Level Security exigiría fijar el contexto de clínica en cada conexión.

## Decisión

- Los límites entre clínicas se aplican en la capa de servicios de Django: toda consulta sobre datos clínicos filtra por la clínica de la membresía activa.
- Las llaves foráneas compuestas sobre `(clinic_id, …)` impiden que una fila mezcle datos de dos clínicas.
- Row-Level Security queda fuera del MVP.

## Consecuencias

- Una consulta que omita el filtro de clínica podría leer filas de otra clínica; las pruebas y la revisión de código deben cubrirlo.
- RLS está planeado como endurecimiento posterior al MVP.
