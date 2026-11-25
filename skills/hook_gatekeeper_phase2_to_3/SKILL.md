---
name: hook_gatekeeper_phase2_to_3
description: "Este Hook verifica que los datos realmente existen en la base de datos antes de permitir que dbt comience a transformarlos. Se dispara tras cargar datos locales (VÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­a A) o tras la ejecuciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n exitosa del script de Python (VÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­a B)."
---
# HOOK: VALIDACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN DE INGESTA Y CIERRE DE FASE (FASE 2 - PASO FINAL)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Este Hook verifica que los datos realmente existen en la base de datos antes de permitir que dbt comience a transformarlos. Se dispara tras cargar datos locales (VÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­a A) o tras la ejecuciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n exitosa del script de Python (VÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­a B).

## INSTRUCCIONES PARA EL AGENTE
1. ConÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ctate a `dwh_dev.duckdb` y lista todas las tablas cargadas en el esquema `raw` con su recuento de filas. Ejecuta un `COUNT(*)` individual por cada tabla listada en `information_schema.tables` donde `table_schema = 'raw'` y presenta los resultados en formato tabla.
2. Para cada tabla cargada, ejecuta esta query de validaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de tipos e indica los resultados en una tabla resumen:

```sql
SELECT
  column_name,
  data_type,
  COUNT(*) - COUNT(column_name) AS null_count
FROM information_schema.columns
LEFT JOIN [tabla] ON TRUE
WHERE table_schema = 'raw'
  AND table_name = '[nombre_tabla]'
GROUP BY column_name, data_type
ORDER BY column_name;
```

  Simplifica el resultado presentando ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºnicamente las columnas que cumplan alguna de estas condiciones de alerta:
  * **Tipo sospechoso:** columnas cuyo nombre contiene `date`, `fecha`, `time`, `price`, `value`, `amount`, `total` pero cuyo tipo inferido es `VARCHAR` en lugar de `DATE`, `TIMESTAMP` o `DOUBLE`.
  * **Nulos elevados:** columnas con mÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡s del 20% de valores nulos.

  Si no hay alertas en ninguna tabla, indica simplemente: *"ValidaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de tipos completada. Sin alertas."*

  Si hay alertas, muÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©stralas en este formato:

  | Tabla | Columna | Tipo inferido | Alerta |
  |---|---|---|---|
  | raw.[nombre] | [columna] | VARCHAR | Posible fecha mal tipada |
  | raw.[nombre] | [columna] | DOUBLE | 35% nulos |

  **Importante:** Las alertas son informativas, no bloqueantes. El Supervisor decide si continuar o corregir la ingesta.

3. Detente y muestra este mensaje exacto al Supervisor: *"La ingesta ha finalizado. Estas son las tablas cargadas en DuckDB:*

  | Tabla | Filas cargadas |
  |---|---|
  | raw.[nombre] | [X] |

  *[Inserta aquÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­ el resumen de validaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de tipos del paso 2]*

  *ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Apruebas este volumen de datos y me autorizas a iniciar la Fase 3 (TransformaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n dbt) invocando al Analytics_Engineer_Agent? (S/N)"*.

* **Si la respuesta es "S":** (Si estabas usando al subagente Python, apÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡galo). El Main Agent retoma el control y marca la Fase 2 como completada.

* **Si la respuesta es "N":** Si hay un problema, no intentes resolverlo inline. Invoca inmediatamente al `Debug_Agent`  transmitiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ndole: la fase actual, este skill o hook como origen, el comando exacto que fallÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ y el output completo del error. Tras haberse corregido el error, vuelve a ejecutar la ingesta y lanza este Gateway de nuevo.