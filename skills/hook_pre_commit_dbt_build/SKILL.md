---
name: hook_pre_commit_dbt_build
description: "Este hook del ciclo de vida asegura que nunca se suba cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo analÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­tico roto al repositorio."
---
# HOOK: BARRERA DE SEGURIDAD PRE-COMMIT (GIT HOOK - GLOBAL)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Este hook del ciclo de vida asegura que nunca se suba cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo analÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­tico roto al repositorio.

## CONDICIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN DE DISPARO
Este hook se activa de forma automÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡tica **cada vez que el Agente intente ejecutar un comando `git commit`** tras haber modificado archivos dentro de `dbt_project/`.

## INSTRUCCIONES PARA EL AGENTE
1. Antes de ejecutar el commit propuesto, ejecuta obligatoriamente el comando desde el directorio correcto:

```bash
cd dbt_project && dbt build -t dev
```

  Alternativamente, si ya estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡s dentro de `dbt_project/`, ejecuta `dbt build -t dev` directamente. Nunca ejecutes este comando desde la raÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­z del proyecto ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â dbt no encontrarÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ `dbt_project.yml` y fallarÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ con un error de configuraciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n no relacionado con la calidad del cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo.

2. **Si el build/test FALLA:** Aborta la operaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de Git inmediatamente. No intentes resolver el error inline. Escala al Main Agent con este mensaje exacto: *"El hook pre-commit ha fallado. Fase: [fase actual]. Skill o acciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n: dbt build -t dev. Output del error: [mensaje completo]."* El Main Agent invocarÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ al `Debug_Agent`. Una vez confirmado que el error estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ resuelto y que `dbt build -t dev` pasa reinicia el proceso de commit desde cero.

3. **Si el build/test PASA:** Ejecuta el commit utilizando Conventional Commits detallando el impacto en la capa de datos.