---
name: skill_data_source_router
description: "Esta habilidad determina la complejidad de la ingesta de datos y decide quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© agente debe ejecutar el trabajo."
---
# SKILL: ENRUTADOR DE ORIGEN DE DATOS (FASE 2 - INICIO)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Esta habilidad determina la complejidad de la ingesta de datos y decide quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© agente debe ejecutar el trabajo.

## INSTRUCCIONES PARA EL AGENTE (MAIN AGENT)
1. Lee el archivo `docs/SLA.md` para entender de dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³nde provienen los datos.
2. Lanza esta pregunta exacta al Supervisor:
**"He revisado el SLA. Para proceder con la ingesta, confirma la vÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­a de acciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n:
A. Los datos ya son archivos locales (.csv / .parquet). Yo (Main Agent) los cargarÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© directamente en DuckDB.
B. Los datos provienen de una API/Web. InvocarÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© al subagente Data_Engineer_Agent para extraerlos con Python.
Por favor, responde A o B."**

3. **Si la respuesta es A:** Antes de cargar nada, ejecuta estos dos pasos previos obligatorios:

  **3a.** Lista todos los archivos disponibles en `data/raw/` y cruza contra las fuentes mencionadas en el SLA. Presenta al Supervisor esta tabla:

  | Estado | Archivo |
  |--------|---------|
  | En SLA | [archivos mencionados en el SLA] |
  | Adicional | [archivos no mencionados en el SLA] |

  Si no hay archivos adicionales, indica: "Todos los archivos coinciden con el SLA."

  **3b.** Lanza esta pregunta exacta al Supervisor:
  **"He encontrado los archivos anteriores en `data/raw/`. ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Deseas cargar:
  A1. Solo los archivos mencionados en el SLA.
  A2. Todos los archivos disponibles.
  A3. Una selecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n especÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­fica (indÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­came cuÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡les)."**

  No ejecutes ninguna carga hasta recibir respuesta.

  Una vez confirmada la selecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n, ejecuta un script SQL o comando DuckDB nativo (`read_csv_auto` o `read_parquet`) para cargar los archivos locales seleccionados en `data/raw/` directamente a la base de datos `dwh_dev.duckdb` siguiendo esta convenciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n obligatoria:
  * **Esquema:** siempre `raw`.
  * **Nombre de tabla:** `raw_[nombre_del_archivo_sin_extension]` en snake_case. Ej: si el archivo es `ventas_2024.csv`, la tabla se llamarÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ `raw.raw_ventas_2024`.
  * **MaterializaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n:** usa SIEMPRE `CREATE OR REPLACE TABLE` al cargar con `read_csv_auto` o `read_parquet`. Esto garantiza que recargar un archivo no duplica datos si la tabla ya existe de un intento anterior:

```sql
CREATE OR REPLACE TABLE raw.raw_[nombre] AS
  SELECT * FROM read_csv_auto('data/raw/[archivo].csv');
```

  * Si hay mÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºltiples archivos, crea una tabla separada por cada uno respetando la misma convenciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n.

Al terminar, dispara el hook de cierre de fase.

4. **Si la respuesta es B:** Antes de invocar al `Data_Engineer_Agent` realiza una llamada de prueba a la API con pageSize mÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­nimo para obtener el totalCount estimado y determinar el nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºmero de pÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ginas (~totalCount / PAGE_SIZE). Presenta este estimado al Supervisor antes de continuar. Luego invoca al `Data_Engineer_Agent` y transfiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rele el control.