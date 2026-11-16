# ADR-0009: Alertas de notas pendientes

- **Estado:** Aceptada
- **Fecha:** 2026-11

## Contexto

El brief pide alertas dentro de la app para notas de sesión pendientes y revisiones pendientes del supervisor. El envío automático por correo o push se planea como la primera función después del MVP.

## Decisión

- Las alertas se calculan con una consulta al abrir la app; ninguna tabla las guarda.
- Toda cita con estado `attended` requiere nota de sesión. La alerta aparece cuando pasan `ends_at` + `clinics.note_due_hours` sin una nota enviada o finalizada. Las citas canceladas o de inasistencia aceptan una nota opcional, pero nunca generan alerta.
- Para un trainee, la obligación se cumple al enviar la nota (`submitted_at`). El supervisor recibe una alerta aparte cuando pasan `submitted_at` + `clinics.review_due_hours` sin aprobación.
- En el MVP las alertas son solo dentro de la app: un contador y una lista.
- La definición de nota pendiente vive en un solo queryset de Django, en la app `clinical`, para que la usen la vista y el futuro proceso programado.

## Consecuencias

- El envío automático agregará un ejecutor de tareas (Celery Beat o cron), una app `notifications` y una tabla de envíos para evitar duplicados.
- Los mensajes a pacientes requerirán su consentimiento para ser contactados.
