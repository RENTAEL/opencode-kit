---
name: skill_write_sla_doc
description: "Esta habilidad consolida las respuestas obtenidas por el `Business_Analyst_Agent` en un documento Markdown estructurado y ejecuta el Gateway HITL para pasar a la Fase 2."
---
# SKILL: CREACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN DEL DOCUMENTO SLA Y GATEWAY (FASE 1 - PASO FINAL)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Esta habilidad consolida las respuestas obtenidas por el `Business_Analyst_Agent` en un documento Markdown estructurado y ejecuta el Gateway HITL para pasar a la Fase 2.

## INSTRUCCIONES PARA EL AGENTE
1. Toma todo el contexto de la entrevista con el Supervisor y redacta un documento llamado `SLA.md` (Service Level Agreement / Requerimientos).
2. Determina la ruta absoluta del proyecto activo buscando el nombre del proyecto en el contexto de la conversaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n o ejecutando `pwd` en la terminal. Guarda el archivo fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­sicamente en `~/projects/[NOMBRE_PROYECTO]/docs/SLA.md` usando **siempre ruta absoluta**. Nunca uses rutas relativas. El formato del documento debe ser:

```markdown
# Documento de Requerimientos y Arquitectura LÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³gica

## SecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n A ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Requerimientos de Negocio (completar en Fase 1)
* **Objetivo Principal:** [Resumen del objetivo]
* **Origen de los Datos:** [Local / API - Detalles]
* **Granularidad del Modelo Final:** [DefiniciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n aproximada de una fila]
* **Glosario de KPIs:** [FÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rmulas matemÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ticas acordadas]
* **Frecuencia de actualizaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n:** [Ej. diaria a las 08:00 AM]
* **Campos PII detectados:** [Indicar columnas conocidas o "Por confirmar en Fase 3" si no hay certeza todavÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­a.]

## SecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n B ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Arquitectura TÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cnica (completar en Fase 3, antes de marts)
* **Esquema esperado de tablas marts:**
  * Tabla de hechos (`fct_...`): [Nombre y descripciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de una fila]
  * Tablas de dimensiones (`dim_...`): [Lista de entidades descriptivas]
* **Criterio de Tie-out:** [QuÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© total o perÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­odo concreto debe cuadrar entre DuckDB y Power BI para considerar el proyecto cerrado.]
* **Campos PII confirmados:** [Confirmar o corregir lo indicado en SecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n A tras haber inspeccionado los datos reales.]
```