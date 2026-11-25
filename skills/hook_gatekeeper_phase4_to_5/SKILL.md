---
name: hook_gatekeeper_phase4_to_5
description: "Gateway de aprobaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n humana (HITL) para validar que el anÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡lisis exploratorio responde a las necesidades de negocio antes de preparar la entrega final. Se dispara tras guardar el Jupyter Notebook."
---
# HOOK: REVISIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN DE INSIGHTS Y CIERRE DE FASE (FASE 4 - PASO FINAL)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Gateway de aprobaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n humana (HITL) para validar que el anÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡lisis exploratorio responde a las necesidades de negocio antes de preparar la entrega final. Se dispara tras guardar el Jupyter Notebook.

## INSTRUCCIONES PARA EL AGENTE
1. Antes de extraer nada, verifica que el notebook contiene una celda de Markdown titulada "Conclusiones Clave" con contenido no vacÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­o. Para ello inspecciona el JSON del archivo `.ipynb` y busca una celda de tipo `markdown` que contenga ese tÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­tulo.

  * **Si la celda no existe o estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ vacÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­a:** No avances. Indica al Supervisor: *"La celda de Conclusiones Clave no existe o estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ vacÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­a en el notebook. Voy a reinvocar `skill_generate_eda_visualizations` para completarla antes de continuar."* Reinvoca el skill y vuelve a lanzar este hook desde el inicio.

  * **Si la celda existe y tiene contenido:** Extrae el texto en formato de viÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±etas y continÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºa al paso 2.

2. Detente y muestra este mensaje al Supervisor: *"He finalizado el AnÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡lisis Exploratorio. El archivo se encuentra en la carpeta notebooks/. Estas son mis conclusiones preliminares: [INSERTA AQUÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â LAS CONCLUSIONES EN VIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‹Å“ETAS] ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Apruebas estos hallazgos y me autorizas a apagar el Data_Scientist_Agent para devolver el control al Main Agent e iniciar la Fase 5 (Reporting y Power BI)? (S/N)"*.

3. **Si la respuesta es "N":** Pregunta al Supervisor quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© perspectiva adicional necesita (ej. "Analiza la tendencia por meses en lugar de aÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±os"), modifica el notebook y vuelve a lanzar este Gateway.

4. **Si la respuesta es "S":** Apaga el subagente y devuelve el control al Main Agent para la recta final.