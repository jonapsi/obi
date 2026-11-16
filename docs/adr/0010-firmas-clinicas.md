# ADR-0010: Firmas clínicas sin firma electrónica en el MVP

- **Estado:** Aceptada
- **Fecha:** 2026-11

## Contexto

La NOM-004 exige identificar al responsable de cada documento del expediente. Una firma electrónica con validez legal (por ejemplo, e.firma) está fuera del alcance del MVP.

## Decisión

- Un documento se finaliza congelándolo: se guardan los snapshots del autor y del responsable y se calcula `content_hash`, que se imprime en el pie del PDF.
- Como control compensatorio, el expediente oficial sigue en papel: Obi exporta solo documentos finalizados como PDF, y el responsable firma la impresión con tinta.

## Consecuencias

- Este control vence antes de que IJPCC deje de llevar expediente en papel y use Obi como su único expediente oficial, o antes de solicitar un dictamen de NOM-024, que exige firmas electrónicas estandarizadas. En cualquiera de esos casos, primero hay que implementar la firma electrónica.
