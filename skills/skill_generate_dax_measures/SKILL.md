---
name: skill_generate_dax_measures
description: "Traduce las fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rmulas de negocio y KPIs definidos en el SLA a cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo DAX optimizado, listo para que el Supervisor lo copie y pegue en Power BI."
---
# SKILL: GENERACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN DE CÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œDIGO DAX (FASE 5 - PASO 1)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Traduce las fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rmulas de negocio y KPIs definidos en el SLA a cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo DAX optimizado, listo para que el Supervisor lo copie y pegue en Power BI.

## INSTRUCCIONES PARA EL AGENTE (MAIN AGENT)
1. Lee el archivo `docs/SLA.md` para extraer el glosario de KPIs.
2. Lee el archivo `docs/DESIGN_RULES.md` y evalÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºa quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© reglas de la secciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n **DAX y Capa SemÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ntica** aplican a las medidas que vas a construir. No todas las reglas serÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡n relevantes ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â aplica ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºnicamente las que correspondan al contexto de este proyecto.
3. ObtÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©n el esquema real de las tablas `marts` (Hechos y Dimensiones) ejecutando esta query directamente en `dwh_dev.duckdb`:

```sql
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'main'
  AND table_name IN (
    SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'main'
      AND table_name LIKE 'fct_%' OR table_name LIKE 'dim_%'
  )
ORDER BY table_name, ordinal_position;
```

   Usa los nombres de tabla y columna exactos que devuelva esta query al escribir el cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo DAX. No uses nombres de memoria.

4. Antes de escribir cualquier medida de agregaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n (`SUM`, `AVERAGE`, `COUNT`), evalÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºa este criterio para cada campo numÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rico:

   **Criterio de grain:** ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿El campo que vas a agregar pertenece al mismo nivel de detalle que el grain de la tabla, o es un valor calculado a un nivel superior (ej. total del pedido repetido en cada lÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­nea de ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­tem)?
   * **Si el grain coincide** (ej. `price` en una fact de ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­tems): usa `SUM()` directamente.
   * **Si el campo es de nivel superior al grain** (ej. `total_payment_value` del pedido repetido en cada ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­tem): calcula desde la dimensiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n que tiene ese nivel de agregaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n, no desde la fact. AÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ade un comentario DAX explicando por quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©.

5. Genera un reporte en la terminal (en formato Markdown) que contenga:
   * Las medidas base con los nombres exactos de columna obtenidos en el paso 3 (ej. `Total Ventas = SUM(fct_sales[amount])`).
   * Las medidas complejas solicitadas (ej. `CALCULATE`, `Time Intelligence`, `DIVIDE`).

6. AÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ade breves comentarios explicando quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© hace cada medida DAX y, cuando aplique el criterio del paso 4, indica desde quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© tabla se calcula y por quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©.