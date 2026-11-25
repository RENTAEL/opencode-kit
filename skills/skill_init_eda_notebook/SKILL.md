---
name: skill_init_eda_notebook
description: "Genera un archivo Jupyter Notebook `.ipynb` fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­sico, establece la estructura de Markdown inicial y configura la conexiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n segura (read-only) a DuckDB."
---
# SKILL: INICIALIZACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN DEL NOTEBOOK EDA Y CONEXIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN (FASE 4 - PASO 1)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Genera un archivo Jupyter Notebook `.ipynb` fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­sico, establece la estructura de Markdown inicial y configura la conexiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n segura (read-only) a DuckDB.

## INSTRUCCIONES PARA EL AGENTE
1. Crea un archivo secuencial en la carpeta de notebooks (ej. `notebooks/01_exploration_SLA.ipynb`).
2. El notebook debe tener una estructura clara en celdas de Markdown y CÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo:
   * **Celda 1 (Markdown):** TÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­tulo del anÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡lisis y objetivo extraÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­do del SLA.
   * **Celda 2 (CÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo):** ImportaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de `pandas`, `matplotlib.pyplot`, `seaborn`, `duckdb` y `pathlib`.
   * **Celda 3 (CÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo):** CreaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n del objeto de conexiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n estricto `read-only` a DuckDB usando la ruta absoluta del proyecto. ObtÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©n la ruta absoluta del proyecto ejecutando `pwd` en la terminal antes de escribir esta celda, y ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºsala directamente en el cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo:

```python
from pathlib import Path

DB_PATH = Path("/ruta/absoluta/al/proyecto/data/dwh_dev.duckdb")
if not DB_PATH.exists():
   raise FileNotFoundError(f"Base de datos no encontrada en {DB_PATH}. Verifica que la Fase 2 completÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ correctamente.")
con = duckdb.connect(str(DB_PATH), read_only=True)
print(f"Conectado a: {DB_PATH}")
```

   Sustituye `/ruta/absoluta/al/proyecto` por la ruta real obtenida con `pwd`. Usar una ruta absoluta explÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­cita garantiza que el notebook funciona correctamente independientemente del directorio de trabajo desde el que VS Code lo ejecute.

3. Guarda el archivo y verifica que es un JSON de Jupyter vÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡lido.