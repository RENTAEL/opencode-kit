---
name: skill_generate_deliverables
description: "Genera la carpeta `outputs/` con el archivo `final_analysis.md`, un paquete de entrega completo y listo para que el Supervisor construya el dashboard en Power BI sin necesidad de buscar informaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n en otros archivos del proyecto."
---
# SKILL: GENERACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN DE ENTREGABLES FINALES (FASE 5 - PASO 3)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Genera la carpeta `outputs/` con el archivo `final_analysis.md`, un paquete de entrega completo y listo para que el Supervisor construya el dashboard en Power BI sin necesidad de buscar informaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n en otros archivos del proyecto.

## INSTRUCCIONES PARA EL AGENTE (MAIN AGENT)
1. Crea la carpeta `outputs/` en la raÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­z del proyecto si no existe.

2. Genera el archivo `outputs/final_analysis.md` con las siguientes secciones, extrayendo la informaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de los pasos anteriores de Fase 5:

### SecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n 1 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ConexiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n a DuckDB
Instrucciones para conectar Power BI al archivo DuckDB del proyecto:
- Ruta absoluta del archivo `dwh_dev.duckdb`
- Tipo de conector recomendado (DuckDB ODBC)
- Lista de tablas marts a importar con una lÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­nea de descripciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n cada una

### SecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n 2 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Modelo Dimensional
Por cada tabla mart, indica:
- Nombre de la tabla
- DescripciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de una fila
- Columnas clave y sus tipos

### SecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n 3 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Medidas DAX
Todas las medidas generadas en `skill_generate_dax_measures`, organizadas por categorÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­a y listas para copiar y pegar en Power BI. Incluye los comentarios explicativos de cada medida.

### SecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n 4 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â NÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºmeros de Tie-out
Tabla con los valores exactos que arrojÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ DuckDB en `skill_write_sql_tieout`. El Supervisor debe usar estos nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºmeros para auditar que el dashboard muestra los mismos resultados.

| KPI | Valor DuckDB |
|-----|-------------|
| [KPI] | [Valor] |

3. Confirma al Supervisor:
  *"El archivo `outputs/final_analysis.md` ha sido generado. ÃƒÆ’Ã†â€™Ãƒâ€¦Ã‚Â¡salo como referencia completa para construir y auditar tu dashboard en Power BI."*

4. Tras confirmar al Supervisor, dispara inmediatamente y de forma automÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡tica el hook `hook_close_project_workflow`. No esperes instrucciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n del Supervisor para hacerlo.