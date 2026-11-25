---
name: hook_gatekeeper_phase1_to_2
description: "Este es un Hook de ejecuciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n obligatoria que bloquea el avance a la Fase 2 hasta que el Supervisor apruebe el documento de requerimientos. Se dispara automÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ticamente justo despuÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s de que la habilidad `skill_write_sla_doc` fina..."
---
# HOOK: VALIDACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN GATEKEEPER Y CIERRE DE FASE (FASE 1 - PASO FINAL)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Este es un Hook de ejecuciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n obligatoria que bloquea el avance a la Fase 2 hasta que el Supervisor apruebe el documento de requerimientos. Se dispara automÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ticamente justo despuÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s de que la habilidad `skill_write_sla_doc` finalice su ejecuciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n.

## INSTRUCCIONES PARA EL AGENTE
**GATEWAY HITL (CIERRE DE FASE 1)**

Tras confirmar la creaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n del archivo `docs/SLA.md`, detente inmediatamente y muestra este mensaje exacto al Supervisor: *"El documento de requerimientos ha sido generado en docs/SLA.md. Por favor, revÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­salo. ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Apruebas este documento y me autorizas a apagar el subagente para devolver el control al Main Agent e iniciar la Fase 2 (ExtracciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n e Ingesta)? (S/N)"*.

* **Si la respuesta es "S":** El `Business_Analyst_Agent` se apaga, y el Main Agent retoma el control del flujo de trabajo, marcando la Fase 1 como completada.

* **Si la respuesta es "N":** No apagues el subagente. Pregunta al Supervisor quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© correcciones de negocio o fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rmulas necesita cambiar recoge las correcciones verbalmente y vuelve a invocar `skill_write_sla_doc` para regenerar el archivo `docs/SLA.md` completo con los cambios incorporados. Una vez regenerado, vuelve a lanzar este Gateway de aprobaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n.