---
name: skill_dbt_tester
description: "Asegura la calidad de los datos creando tests genÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ricos y singulares."
---
# SKILL: GOBERNANZA Y TESTING DBT (FASE 3 - PASO 3)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Asegura la calidad de los datos creando tests genÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ricos y singulares.

## INSTRUCCIONES PARA EL AGENTE
1. Crea o actualiza los archivos `schema.yml` en cada carpeta de modelos (staging y marts).
2. Documenta cada modelo y sus columnas clave (propiedad `description`).
3. AÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ade tests obligatorios a las claves primarias (Primary Keys): `unique` y `not_null`.
4. Si el SLA menciona reglas de negocio especÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­ficas (ej. "el margen nunca puede ser negativo"), crea un test singular SQL en la carpeta `dbt_project/tests/` que falle si se incumple esa condiciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n.