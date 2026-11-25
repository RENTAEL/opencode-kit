---
name: skill_build_staging_layer
description: "Crea los modelos base de dbt. La regla de oro es: 1 modelo staging = 1 tabla raw."
---
# SKILL: CONSTRUCCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN DE CAPA STAGING (FASE 3 - PASO 1)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Crea los modelos base de dbt. La regla de oro es: 1 modelo staging = 1 tabla raw.

## INSTRUCCIONES PARA EL AGENTE

1. Antes de crear ningÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºn modelo, crea el archivo
   `dbt_project/models/staging/sources.yml` declarando las tablas
   raw que vas a consumir. Usa esta estructura como plantilla:

```yaml
version: 2

sources:
  - name: raw
    schema: raw
    tables:
      - name: [nombre_tabla_raw]
        description: "Datos crudos tal como fueron ingestados."
```

   El nombre de la tabla debe coincidir exactamente con el nombre
   de la tabla creada en `dwh_dev.duckdb` durante la Fase 2.

2. Crea los archivos `.sql` correspondientes en
   `dbt_project/models/staging/`. En la clÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡usula FROM usa SIEMPRE
   `{{ source('raw', 'nombre_tabla') }}` para leer las tablas raw.

3. Aplica estrictamente estas transformaciones:
   * **Tipado de datos explÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­cito:** Haz `CAST` a los tipos de datos
     correctos (ej. `CAST(fecha AS DATE)`).
   * **Nomenclatura:** Convierte todas las columnas a `snake_case`
     en inglÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s.
   * **Seguridad (PII):** Si el SLA.md documenta columnas con datos
     personales (emails, telÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©fonos, nombres reales), aplica `md5()`
     para enmascararlos en este paso.
   * **Cero lÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³gicas de negocio:** No hagas `JOIN`s ni agregaciones
     (`GROUP BY`) en esta capa.