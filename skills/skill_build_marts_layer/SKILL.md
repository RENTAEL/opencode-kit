---
name: skill_build_marts_layer
description: "Crea el modelo dimensional (Kimball) aplicando la lÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³gica de negocio acordada."
---
# SKILL: CONSTRUCCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN DE CAPA MARTS (FASE 3 - PASO 2)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Crea el modelo dimensional (Kimball) aplicando la lÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³gica de negocio acordada.

## INSTRUCCIONES PARA EL AGENTE
1. Lee el archivo `docs/DESIGN_RULES.md` y evalÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºa quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© reglas de las secciones **Modelado Dimensional** y **Seguridad y PII** aplican al modelo que vas a construir. No todas las reglas serÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡n relevantes ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â aplica ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºnicamente las que correspondan al contexto de este proyecto.
2. Revisa el glosario de KPIs en `docs/SLA.md`. Si el SLA incluye KPIs de Time Intelligence (MoM, YTD, comparativas de perÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­odos, tendencias temporales), genera una tabla `dim_date` antes de construir los demÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡s marts siguiendo este proceso:

  **2a.** Infiere el rango de fechas ejecutando esta query en `dwh_dev.duckdb`:

  ```sql
  SELECT
    MIN(fecha_columna) AS fecha_min,
    MAX(fecha_columna) AS fecha_max
  FROM raw.[tabla_de_hechos_principal];
  ```

  Sustituye `fecha_columna` y `tabla_de_hechos_principal` por los valores reales del proyecto.

  **2b.** Crea el archivo `dbt_project/models/marts/dim_date.sql` con esta estructura base, ajustando el rango inferido:

  ```sql
  WITH date_spine AS (
    SELECT UNNEST(
      generate_series(
        DATE '[fecha_min]',
        DATE '[fecha_max]',
        INTERVAL '1 day'
      )
    ) AS date_day
  )
  SELECT
    date_day                                    AS date_id,
    EXTRACT(YEAR FROM date_day)::INT            AS year,
    EXTRACT(MONTH FROM date_day)::INT           AS month,
    EXTRACT(DAY FROM date_day)::INT             AS day,
    EXTRACT(QUARTER FROM date_day)::INT         AS quarter,
    EXTRACT(DOW FROM date_day)::INT             AS day_of_week,
    TO_CHAR(date_day, 'YYYY-MM')                AS year_month,
    TO_CHAR(date_day, 'Month YYYY')             AS month_name,
    CASE WHEN EXTRACT(DOW FROM date_day) IN (0,6)
      THEN FALSE ELSE TRUE END                  AS is_weekday
  FROM date_spine
  ```

  **2c.** Declara `dim_date` en el `schema.yml` con test `unique` + `not_null` sobre `date_id`.

  Si el SLA no incluye KPIs de Time Intelligence, omite este paso por completo.

3. Crea los archivos `.sql` en `dbt_project/models/marts/`.
4. Utiliza la funciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n `{{ ref('nombre_modelo_staging') }}` para leer de la capa anterior. ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡Nunca leas directamente de `raw`!
5. Construye **Tablas de Dimensiones** (`dim_...`): Entidades descriptivas (usuarios, productos, tiempo) con claves subrogadas ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºnicas.
6. Construye **Tablas de Hechos** (`fct_...`): Tablas transaccionales o de eventos que contengan las mÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tricas numÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ricas y las claves forÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡neas hacia las dimensiones.
7. AsegÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºrate de implementar las fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rmulas matemÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ticas exactas definidas en `docs/SLA.md`.