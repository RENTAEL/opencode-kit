---
name: skill_write_sql_tieout
description: "Crea y ejecuta consultas SQL en DuckDB que sirven como \"fuente de la verdad\" para que el Supervisor valide que los nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºmeros mostrados en Power BI son exactos."
---
# SKILL: GENERACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN DE CONSULTAS DE AUDITORÃƒÆ’Ã†â€™Ãƒâ€šÃ‚ÂA / TIE-OUT (FASE 5 - PASO 2)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Crea y ejecuta consultas SQL en DuckDB que sirven como "fuente de la verdad" para que el Supervisor valide que los nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºmeros mostrados en Power BI son exactos.

## INSTRUCCIONES PARA EL AGENTE (MAIN AGENT)
1. BasÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ndote en los KPIs del paso anterior, redacta consultas SQL directas contra las tablas `marts` de DuckDB. (Ej. Si en DAX calculaste las ventas del ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºltimo mes, haz el `SELECT SUM(...) WHERE fecha = ...` equivalente).
2. Ejecuta esas consultas en la terminal.
3. Imprime en pantalla una tabla comparativa con los resultados exactos que arrojÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ DuckDB.
4. Indica al Supervisor: *"Estos son los nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºmeros exactos (Tie-out) que debe mostrar tu Power BI. ÃƒÆ’Ã†â€™Ãƒâ€¦Ã‚Â¡salos para auditar tu dashboard."*
5. Tras imprimir los resultados, dispara inmediatamente y de forma automÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡tica la skill `skill_generate_deliverables`. No esperes instrucciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n del Supervisor para hacerlo.