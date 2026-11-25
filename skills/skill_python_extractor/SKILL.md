---
name: skill_python_extractor
description: "Habilidad del `Data_Engineer_Agent` para generar scripts modulares de extracciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n que guarden los datos en local y los inserten en DuckDB."
---
# SKILL: CREACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN DE SCRIPT DE EXTRACCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN (FASE 2 - PYTHON)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Habilidad del `Data_Engineer_Agent` para generar scripts modulares de extracciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n que guarden los datos en local y los inserten en DuckDB.

## INSTRUCCIONES PARA EL AGENTE
1. Crea un script en la carpeta `src/` (ej. `src/extract_api_data.py`).
2. El script debe cumplir estrictamente estas reglas:
   * **Credenciales:** Lee SIEMPRE las API keys y tokens desde variables de entorno usando `python-dotenv`. Nunca hardcodees credenciales en el cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo. El patrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n obligatorio es:

```python
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("NOMBRE_DE_LA_VARIABLE")
if not API_KEY:
    raise ValueError("NOMBRE_DE_LA_VARIABLE no estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ definida en .env")
```

     Las variables deben estar declaradas en el archivo `.env` de la raÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­z del proyecto.

   * **Peticiones HTTP:** Maneja errores en cada llamada (ej. `response.raise_for_status()`).
   * **Backup local:** Guarda una copia fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­sica de seguridad de los datos crudos descargados en la carpeta `data/raw/` en formato `.csv` o `.parquet`.
   * **Guardado incremental obligatorio para APIs paginadas:** Si el script pagina sobre una API (mÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡s de 10 pÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ginas esperadas), NUNCA acumules todos los registros en memoria para escribir al final. En su lugar:
     1. Escribe al CSV en modo `append` cada `CHECKPOINT_EVERY` pÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ginas (valor por defecto: 10).
     2. Guarda un checkpoint en `data/raw/checkpoint.json` con `next_page_token`, `page` y `total_processed` al final de cada lote.
     3. Al iniciar, lee el checkpoint si existe para reanudar desde la ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºltima pÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡gina guardada en lugar de empezar desde cero.
     4. Elimina el checkpoint al terminar con ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©xito.
     5. El patrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n obligatorio es:

```python
CHECKPOINT_EVERY = 10
CHECKPOINT_FILE = Path("data/raw/checkpoint.json")

def save_checkpoint(next_page_token, page, total_processed):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({
            "next_page_token": next_page_token,
            "page": page,
            "total_processed": total_processed,
        }, f)

def load_checkpoint():
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)
    return None
```

   * **Lanzamiento con screen para extracciones largas:** Si se estima que la extracciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n tardarÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ mÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡s de 2 minutos, el script debe lanzarse dentro de una sesiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n `screen` para que sobreviva desconexiones de terminal y apagados de WSL2. El comando estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ndar de lanzamiento es:

```bash
screen -dmS extraction bash -c 'cd /ruta/proyecto && source .venv/bin/activate && python3 -u src/extract_api_data.py > logs/extraction.log 2>&1'
```

     Tras lanzar, verificar que el proceso estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ activo con `screen -ls extraction` y monitorizar con `tail -f logs/extraction.log`.

   * **ConvenciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de nombres en DuckDB:** Inserta los datos en `dwh_dev.duckdb` bajo el esquema `raw` siguiendo la convenciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n `raw_[nombre_fuente]` en snake_case. (Ej. si extraes de la API de Stripe, la tabla serÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ `raw.raw_stripe`). Usa SIEMPRE `CREATE OR REPLACE TABLE` al materializar en DuckDB, nunca `INSERT INTO`. Esto garantiza que relanzar el script no duplica filas si la tabla ya existe de un intento anterior.
   * **Cero limpieza:** No apliques `dropna`, `rename` ni ninguna transformaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de negocio. Los datos deben insertarse tal cual se reciben de la fuente.

3. Ejecuta el script de Python en la terminal.
4. Si el comando falla, no intentes resolverlo inline. Invoca inmediatamente al `Debug_Agent` transmitiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ndole: la fase actual, este skill o hook como origen, el comando exacto que fallÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ y el output completo del error. Si termina con ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©xito (exit code 0), dispara el hook `hook_gatekeeper_phase2_to_3`.