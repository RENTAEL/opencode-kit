---
name: hook_gatekeeper_dbt_review
description: "Bloquea el avance del proyecto hasta que el Supervisor audite el cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo SQL y la arquitectura del DAG."
---
# HOOK: GATEWAY HITL DE REVISIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN ANALÃƒÆ’Ã†â€™Ãƒâ€šÃ‚ÂTICA (FASE 3 - PASO FINAL)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Bloquea el avance del proyecto hasta que el Supervisor audite el cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo SQL y la arquitectura del DAG.

## INSTRUCCIONES PARA EL AGENTE
1. Antes de redactar ningÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºn informe, ejecuta obligatoriamente:

```bash
cd dbt_project && dbt build -t dev
```

   * **Si el build FALLA:** No presentes ningÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºn informe al Supervisor. Escala al Main Agent con este mensaje exacto: *"El hook gatekeeper_dbt_review ha detectado un fallo en dbt build antes de presentar el informe. Fase: 3. Skill o acciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n: dbt build -t dev. Output del error: [mensaje completo]."* El Main Agent invocarÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ al `Debug_Agent`. Una vez confirmado que el error estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ resuelto y que `dbt build -t dev` pasa, reinicia este hook desde el paso 1.

   * **Si el build PASA:** ContinÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºa al paso 2.

2. Al terminar los tests, redacta un breve informe en consola (Markdown) que contenga:
   * **Modelos creados:** Lista en formato ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡rbol de los `.sql` (Staging -> Marts).
   * **LÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³gica aplicada:** Breve explicaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n humana de cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³mo calculaste los KPIs del SLA.
   * **Tests implementados:** QuÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© validaciones de calidad se han configurado.
   * **Resultado del build:** Indica explÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­citamente cuÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ntos modelos y tests pasaron (ej. `46/46 PASS`).

3. Detente y pregunta: *"He finalizado la arquitectura de dbt y el build pasa con todos los tests en verde. ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Apruebas el cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo generado y me autorizas a apagar el Analytics_Engineer_Agent para devolver el control al Main Agent? (S/N)"*.

4. **Si "N":** Distingue entre dos situaciones:
   * **El Supervisor rechaza por razones de negocio** (ej. un KPI estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ mal calculado, falta una dimensiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n): Pregunta quÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© SQL o      regla de negocio estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ mal, corrige los modelos afectados, recompila con `dbt build -t dev` y vuelve a lanzar este Gateway. Lleva un contador interno de rechazos consecutivos. Si el Supervisor rechaza **3 veces seguidas**, detente y muestra este mensaje exacto:
   *"He alcanzado 3 intentos de correcciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n sin aprobaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n. Esto indica un posible desacuerdo estructural sobre la lÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³gica de negocio o las fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rmulas del SLA. Por favor revisemos juntos el archivo docs/SLA.md antes de continuar. ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿QuÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© secciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n necesita ser corregida en el documento base?"* No recompiles ni relances el Gateway hasta que el Supervisor haya actualizado el SLA y dado instrucciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n explÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­cita de reiniciar.
   * **Se produce un error tÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cnico** durante la recompilaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n (ej. fallo de sintaxis SQL, error de compilaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n dbt): No intentes resolverlo inline. Escala al Main Agent con el mensaje estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ndar de gestiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de errores para que invoque al `Debug_Agent`.

5. **Si "S":** Apaga el subagente y devuelve el control al Main Agent.