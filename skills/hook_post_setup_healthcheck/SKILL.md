---
name: hook_post_setup_healthcheck
description: "Este es un Hook de ejecuciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n obligatoria al finalizar las tres skills previas de la Fase 0. Su funciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n es auditar que dbt tiene conexiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n nativa con DuckDB."
---
# HOOK: VALIDACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN POST-SETUP Y CIERRE DE FASE (FASE 0 - PASO 4)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Este es un Hook de ejecuciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n obligatoria al finalizar las tres skills previas de la Fase 0. Su funciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n es auditar que dbt tiene conexiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n nativa con DuckDB.

## INSTRUCCIONES PARA EL AGENTE
1. Ejecuta de forma automÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡tica el test de conexiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n en la terminal:

```bash
source .venv/bin/activate
cd dbt_project
dbt debug
```

2. GATEWAY HITL (CIERRE DE FASE 0):

* Si dbt debug es EXITOSO (All checks passed): Muestra un reporte limpio en consola confirmando que la Fase 0 se ha completado con ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©xito. Pregunta obligatoriamente al usuario: "ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Aprobado el Setup tÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cnico? ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Deseas invocar al subagente Business_Analyst_Agent para iniciar la Fase 1 (Entendimiento de Negocio)? (S/N)".
* Si dbt debug FALLA: No permitas avanzar y no intentes resolverlo inline. Invoca inmediatamente al `Debug_Agent` transmitiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ndole: la fase actual, este skill o hook como origen, el comando exacto que fallÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ y el output completo del error.