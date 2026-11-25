---
name: skill_config_dbt
description: "Esta habilidad inicializa el proyecto dbt y configura de forma dinÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡mica el archivo de credenciales del sistema para conectar dbt con el Data Warehouse de DuckDB."
---
# SKILL: INICIALIZACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN Y CONFIGURACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN DE DBT CORE (FASE 0 - PASO 3)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Esta habilidad inicializa el proyecto dbt y configura de forma dinÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡mica el archivo de credenciales del sistema para conectar dbt con el Data Warehouse de DuckDB.

## INSTRUCCIONES PARA EL AGENTE
1. Lanza la pregunta de confirmaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n: **"ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Deseas inicializar el proyecto dbt y configurar el archivo profiles.yml? (S/N)"**.
2. Si la respuesta es "S", ejecuta en la terminal raÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­z:

```bash
source .venv/bin/activate

# Guard: verificar si dbt_project/ ya existe antes de inicializar
if [ -d "dbt_project" ]; then
  echo "dbt_project/ ya existe. Saltando dbt init y continuando con la configuraciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de profiles.yml y dbt_project.yml."
else
  echo "1" | dbt init dbt_project
fi
```

**Nota:** El guard evita que dbt init falle si el proyecto ya fue inicializado en un intento anterior. El `echo "1" |` responde automÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ticamente al wizard interactivo seleccionando la primera opciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n (duckdb). Este mecanismo asume que `dbt-duckdb` fue instalado en el paso anterior (skill_setup_environment) y que por tanto aparece como opciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n 1. Como salvaguarda, tras ejecutar init, verifica que el archivo `dbt_project/dbt_project.yml` contiene la lÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­nea `profile: 'dbt_project'` antes de continuar.

3. ObtÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©n la ruta absoluta del directorio actual:

```bash
pwd
```

4. Modifica el archivo global de configuraciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n del usuario en `~/.dbt/profiles.yml`. Reemplaza `[RUTA_PROYECTO]` con la ruta absoluta obtenida en el paso anterior:

```yaml
dbt_project:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: "[RUTA_PROYECTO]/data/dwh_dev.duckdb"
    prod:
      type: duckdb
      path: "[RUTA_PROYECTO]/data/dwh_prod.duckdb"
```

5. Abre el archivo `dbt_project/dbt_project.yml` y aÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ade la configuraciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de materializaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n por capa. Localiza la secciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n `models:` y reemplÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡zala con esta configuraciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n:

```yaml
models:
  dbt_project:
    staging:
      +materialized: view
    intermediate:
      +materialized: view
    marts:
      +materialized: table
```

Nota: Esto garantiza que las tablas de marts se persisten fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­sicamente en DuckDB, optimizando el rendimiento de las consultas desde Power BI, mientras que staging e intermediate permanecen como vistas ligeras.