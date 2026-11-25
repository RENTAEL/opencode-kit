---
name: hook_validate_sla
description: "Este hook se dispara automÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ticamente despuÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s de que el Supervisor aprueba el SLA en `hook_gatekeeper_phase1_to_2`. Verifica programÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ticamente que la SecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n A del archivo `docs/SLA.md` contiene todos los campo..."
---
# HOOK: VALIDACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN DE INTEGRIDAD DEL SLA (FASE 1 - POST APROBACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Este hook se dispara automÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ticamente despuÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s de que el Supervisor aprueba el SLA en `hook_gatekeeper_phase1_to_2`. Verifica
programÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ticamente que la SecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n A del archivo `docs/SLA.md` contiene todos los campos obligatorios con contenido real antes de permitir el inicio de la Fase 2.

## INSTRUCCIONES PARA EL AGENTE

### Paso 1 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Leer el archivo
Lee el contenido completo de `docs/SLA.md`.

### Paso 2 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Verificar campos obligatorios
Comprueba que los siguientes campos de la SecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n A existen y tienen contenido que no sea un placeholder (es decir, que no contengan corchetes como `[` o `]` y que no estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©n vacÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­os):

| Campo | VÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡lido si... |
|---|---|
| Objetivo Principal | Tiene texto sin corchetes |
| Origen de los Datos | Tiene texto sin corchetes |
| Granularidad del Modelo Final | Tiene texto sin corchetes |
| Glosario de KPIs | Tiene al menos una fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rmula |
| Frecuencia de actualizaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n | Tiene texto sin corchetes |
| Campos PII detectados | Tiene texto (puede ser "Ninguno") |

### Paso 3 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Actuar segÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºn el resultado

* **Si todos los campos son vÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡lidos:** Muestra este mensaje al Supervisor:
  *"ValidaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n del SLA completada. Todos los campos obligatorios de la SecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n A estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡n presentes y completos. Procediendo a invocar `skill_data_source_router` para iniciar la Fase 2."* ContinÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºa inmediatamente invocando `skill_data_source_router`.

* **Si algÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºn campo estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ vacÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­o o contiene placeholders:** No avances a Fase 2. Muestra este mensaje exacto al Supervisor:
  *"La validaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n del SLA ha detectado campos incompletos en la SecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n A:*
  *ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â [lista de campos con problema]*
  *Por favor, devuelve el control al Business_Analyst_Agent para completar la informaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n faltante antes de continuar."* Reinvoca al `Business_Analyst_Agent` indicÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ndole exactamente quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© campos necesitan completarse.