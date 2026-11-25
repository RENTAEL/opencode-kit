---
name: hook_close_project_workflow
description: "Es el punto de control definitivo. Valida el ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©xito de la integraciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n con Power BI y realiza el cierre formal del ciclo de vida del cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo en Git."
---
# HOOK: GATEWAY HITL DE CIERRE DE PROYECTO (FASE 5 - PASO FINAL)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Es el punto de control definitivo. Valida el ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©xito de la integraciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n con Power BI y realiza el cierre formal del ciclo de vida del cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo en Git.

## INSTRUCCIONES PARA EL AGENTE (MAIN AGENT)
1. Tras proporcionar el DAX y los Tie-outs, detente y lanza esta pregunta exacta al Supervisor:
  
  *"He entregado los materiales de Reporting. Por favor, construye el dashboard en Power BI y audita los nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºmeros. ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Cuadran los datos de Power BI con las consultas de DuckDB? ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Me autorizas a cerrar el proyecto y fusionar los cambios? (S/N)"*.

2. **Si la respuesta es "N":** Pregunta en quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© KPI hay discrepancias. Revisa las tablas de dbt o el DAX generado para encontrar el error, y vuelve a intentar la validaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n.

3. **Si la respuesta es "S":**
  * Primero ejecuta el protocolo de compilaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n obligatorio independientemente del volumen de errores:
    1. Lee todas las entradas con estado RESUELTO en `logs/errors.md`.
    2. Si existen entradas resueltas, compÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­lalas en `docs/SYSTEM_MEMORY.md` bajo la secciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n "Conocimiento Acumulado" siguiendo el formato existente del documento.
    3. Limpia las entradas con estado RESUELTO de `logs/errors.md`, pero mantÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©n el resto ademÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡s de la plantilla inicial.
    
    * Si `logs/errors.md` no tiene entradas, omite este paso e indica al Supervisor: *"No hubo errores durante este proyecto. SYSTEM_MEMORY.md no requiere actualizaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n automÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡tica."*

  * Tras la compilaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n automÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡tica, pregunta al Supervisor: 
    *"ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Hubo durante este proyecto alguna lecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n aprendida, decisiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de arquitectura incorrecta o problema conceptual que no generÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ un error tÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cnico pero que merezca documentarse en SYSTEM_MEMORY.md para proyectos futuros? (S/N)"*

    * **Si la respuesta es "S":** Pide al Supervisor que describa la lecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n aprendida y aÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡dela manualmente en `docs/SYSTEM_MEMORY.md` bajo la secciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n "Conocimiento Acumulado" con este formato:

      ```markdown
      ### LecciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n aprendida: [tÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­tulo breve]
      **Contexto:** [en quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© situaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n ocurriÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³]
      **Problema:** [quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© saliÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ mal o quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© decisiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n resultÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ incorrecta]
      **Aprendizaje:** [quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© hacer diferente en proyectos futuros]
      ```

    * **Si la respuesta es "N":** ContinÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºa con el commit final sin modificaciones adicionales.

  * Antes del commit final, verifica en quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© rama estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡s con `git branch --show-current`. Si estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡s en `main`, crea una feature branch primero: `git checkout -b feature/entrega-final-[nombre_proyecto]`. Si ya estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡s en una feature branch, continÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºa directamente. Ejecuta el `git commit` final con el mensaje: `feat: entrega final dashboard [nombre_proyecto] v1.0.0`.

  * Pregunta al Supervisor: *"ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Tienes repositorio remoto (GitHub/GitLab) o trabajas solo en local?"*

    * **Si la respuesta es "remoto":** Pregunta al Supervisor: *"ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿EstÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ el repositorio remoto vacÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­o y sin configurar? (S/N)"*

      * **Si la respuesta es "S":** Configura el remote (pide al Supervisor la informaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n que necesites para ello) y haz push de la feature branch.
      * **Si la respuesta es "N":** Pide al Supervisor que te explique cuales son la condiciones del repositorio remoto. Una vez comprendidas las condiciones del repositorio remoto, realiza los pasos necesarios para configurar el remote y hacer push de la feature branch.
    
      Una vez realizado el push de la feature branch. Indica al Supervisor: *"Por favor abre una Pull Request desde la rama actual hacia `main`, revisa los cambios y aprueba el merge. Una vez hecho el merge, indÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­came 'merge completado' para ejecutar el tag sobre main."* Espera la confirmaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n antes de continuar. Tras recibirla, ejecuta:
   
      ```bash
      git checkout main
      git pull origin main
      git tag -a v1.0.0 -m "Entrega final: [nombre_proyecto]"
      git push origin v1.0.0
      ```

    * **Si la respuesta es "local":** Ejecuta el merge directamente:

      ```bash
      git checkout main
      git merge feature/entrega-final-[nombre_proyecto]
      git tag -a v1.0.0 -m "Entrega final: [nombre_proyecto]"
      ```

  * Muestra un mensaje de celebraciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n indicando que el pipeline analÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­tico ha sido completado con ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©xito siguiendo el estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ndar HITL.

  * Tras el mensaje de celebraciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n, compara `docs/SYSTEM_MEMORY.md` y `logs/errors.md` del proyecto con sus equivalentes en `~/projects/hitl-analytics-team/` para identificar entradas nuevas. Muestra al Supervisor un resumen de lo encontrado y pregunta exactamente: *"He detectado las siguientes entradas nuevas que podrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­an propagarse al hitl-analytics-team: [lista de entradas nuevas]. ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Apruebas propagar este conocimiento al framework base para que estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© disponible en proyectos futuros? (S/N)"*

    * **Si la respuesta es "N":** No modifiques el framework base. Cierra el proyecto.
    * **Si la respuesta es "S":** Propaga el conocimiento acumulado al framework base ejecutando los siguientes pasos:

      1. Lee las entradas en `logs/errors.md` del proyecto actual.
      2. Lee las entradas nuevas de `docs/SYSTEM_MEMORY.md` del proyecto actual.
      3. Compara ambos archivos con los equivalentes en `~/projects/hitl-analytics-team/` para identificar entradas que no existan aÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºn en el framework base.
      4. Si existen entradas nuevas en `logs/errors.md`, aÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡delas a `~/projects/hitl-analytics-team/logs/errors.md`.
      5. Si existen entradas nuevas en `docs/SYSTEM_MEMORY.md`, aÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡delas a `~/projects/hitl-analytics-team/docs/SYSTEM_MEMORY.md` bajo la secciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n correspondiente (DuckDB, dbt Core, Python, Entorno).
      6. Confirma al Supervisor: *"Los archivos del framework base han sido actualizados con las entradas nuevas de este proyecto."*
  
  * Si no hay entradas nuevas en ninguno de los dos archivos, indica: *"Los archivos del framework base ya estaban al dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­a. No se requieren cambios."*