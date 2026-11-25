---
name: skill_generate_eda_visualizations
description: "Desarrolla el cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo analÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­tico utilizando DataFrames y librerÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­as visuales para responder al SLA."
---
# SKILL: DESARROLLO DE ANÃƒÆ’Ã†â€™Ãƒâ€šÃ‚ÂLISIS Y GRÃƒÆ’Ã†â€™Ãƒâ€šÃ‚ÂFICOS (FASE 4 - PASO 2)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Desarrolla el cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo analÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­tico utilizando DataFrames y librerÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­as visuales para responder al SLA.

## INSTRUCCIONES PARA EL AGENTE
1. Abre el notebook creado en el paso anterior y aÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ade nuevas celdas de cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo.
2. Crea la carpeta de exportaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de grÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ficas si no existe:

```python
from pathlib import Path
charts_dir = Path("/ruta/absoluta/al/proyecto/outputs/charts")
charts_dir.mkdir(parents=True, exist_ok=True)
```

   Sustituye `/ruta/absoluta/al/proyecto` por la misma ruta absoluta usada en la celda de conexiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n a DuckDB.

3. Por cada KPI o pregunta del SLA:
   * Escribe una celda ejecutando una query SQL contra las tablas `marts` para cargar el resultado en un DataFrame de pandas (ej. `df = con.execute("SELECT ...").df()`).
   * **PrecauciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n en JOINs:** Cuando una query hace JOIN entre dos o mÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡s tablas que comparten nombres de columna (ej. `is_completed`, `is_abandoned`, `status`), califica siempre las columnas con el alias de tabla explÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­cito (ej. `f.is_completed`, `s.status_label`). Las referencias ambiguas causan `BinderException` en DuckDB.
   * Escribe la celda de visualizaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n usando `matplotlib` o `seaborn` (barras, dispersiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n, tendencias segÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºn aplique).
   * Al final de cada celda de visualizaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n, guarda la grÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡fica como `.png` en `outputs/charts/` usando un nombre secuencial y descriptivo:

```python
fig.savefig(charts_dir / "01_nombre_descriptivo_del_kpi.png", dpi=150, bbox_inches='tight')
plt.show()
```

   El nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºmero secuencial debe coincidir con el orden de apariciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de la grÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡fica en el notebook (01, 02, 03...). El nombre descriptivo debe reflejar el KPI que representa (ej. `01_revenue_total.png`, `02_aov_distribution.png`, `03_ontime_rate.png`).

4. AÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ade una celda final de Markdown titulada "Conclusiones Clave" donde resumas en viÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±etas los hallazgos de negocio (tendencias, outliers, patrones, respuestas al SLA).
5. AÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ade una celda final de cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo que cierre explÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­citamente la conexiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n a DuckDB antes de terminar:

```python
con.close()
```

6. Guarda los cambios asegurando la integridad del notebook.
7. **ValidaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de ejecuciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n obligatoria antes de disparar el hook:** Ejecuta el notebook completo en modo headless para verificar que todas las celdas pasan sin errores:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/[nombre_notebook].ipynb
```

   * **Si el comando termina con exit code 0:** El notebook es vÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡lido. ContinÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºa al paso 8.
   * **Si el comando falla:** No avances al hook. Identifica el tipo de error antes de actuar:
     * **Error de SQL en una celda concreta** (`BinderException`, `SyntaxError`, `CatalogException`, `ColumnNotFoundException`): CorrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­gelo directamente en el notebook ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â califica columnas ambiguas con alias de tabla, corrige nombres de columna o tabla, ajusta la sintaxis. Reejecutar este paso una vez corregido. No es necesario invocar al `Debug_Agent` para este tipo de errores.
     * **Error de entorno o infraestructura** (el notebook no arranca, `ModuleNotFoundError`, fallo de conexiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n a DuckDB, error de kernel, permisos de escritura): No intentes resolverlo inline. Invoca inmediatamente al `Debug_Agent` transmitiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ndole: la fase actual, esta skill como origen, el comando exacto que fallÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ y el output completo del error. Una vez resuelto, repite este paso desde el inicio.
8. Al terminar, dispara el hook de cierre de fase.