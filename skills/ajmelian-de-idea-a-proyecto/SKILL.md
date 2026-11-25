---
name: ajmelian-de-idea-a-proyecto
description: "Convierte ideas, requisitos y repositorios existentes en **especificaciones OpenSpec, planes SDD/TDD y cambios verificables**, con trazabilidad de requisitos a evidencias y aprobaciones humanas antes de pasar de documentaciÃƒÆ’Ã‚Â³n a cÃƒÆ’Ã‚Â³digo."
---
# De idea a proyecto: OpenCode + OpenSpec + SDD/TDD

Convierte ideas, requisitos y repositorios existentes en **especificaciones OpenSpec,
planes SDD/TDD y cambios verificables**, con trazabilidad de requisitos a evidencias
y aprobaciones humanas antes de pasar de documentaciÃƒÆ’Ã‚Â³n a cÃƒÆ’Ã‚Â³digo.

**English:** Turn software ideas and existing codebases into reviewable OpenSpec
contracts, test-first implementation tasks and reproducible verification. Separate
read-only discovery, documentation, coding and closing with explicit human gates.

- **CuÃƒÆ’Ã‚Â¡ndo usar:** iniciar un proyecto, transformar una necesidad en requisitos,
  crear o revisar un cambio OpenSpec, planificar tareas TDD, auditar
  documentaciÃƒÆ’Ã‚Â³n o verificar un incremento antes de cerrarlo.
- **CuÃƒÆ’Ã‚Â¡ndo no usar:** tareas triviales que no requieren especificaciÃƒÆ’Ã‚Â³n ni
  trazabilidad, o cuando no hay acceso al repositorio y a sus especificaciones.
- **InstalaciÃƒÆ’Ã‚Â³n:** `npx skills add ajmelian/de-idea-a-proyecto`
- **DocumentaciÃƒÆ’Ã‚Â³n:** [README](README.md) Ãƒâ€šÃ‚Â· [InstalaciÃƒÆ’Ã‚Â³n](INSTALL.md) Ãƒâ€šÃ‚Â·
  [Ejemplos de uso](references/prompt-examples.md)

## Contrato innegociable

1. Tratar requisitos aprobados y OpenSpec versionado como contrato de desarrollo. No sustituir una decisiÃƒÆ’Ã‚Â³n humana por una inferencia del agente.
2. Nunca pasar directamente de una idea a cÃƒÆ’Ã‚Â³digo. Obtener primero requisitos verificables, escenarios y autorizaciÃƒÆ’Ã‚Â³n para implementar.
3. Interpretar **analizar, revisar, auditar, planificar** como SOLO LECTURA, salvo autorizaciÃƒÆ’Ã‚Â³n explÃƒÆ’Ã‚Â­cita para escribir archivos. Distinguir la autorizaciÃƒÆ’Ã‚Â³n para documentaciÃƒÆ’Ã‚Â³n de la autorizaciÃƒÆ’Ã‚Â³n para cÃƒÆ’Ã‚Â³digo.
4. No cambiar cÃƒÆ’Ã‚Â³digo, datos, dependencias, infraestructura, configuraciÃƒÆ’Ã‚Â³n, ramas, commits ni archivos fuera del alcance autorizado. Antes de acciones destructivas, solicitar aprobaciÃƒÆ’Ã‚Â³n especÃƒÆ’Ã‚Â­fica.
5. Registrar hechos, decisiones aprobadas, hipÃƒÆ’Ã‚Â³tesis reversibles, cuestiones bloqueantes y exclusiones. No presentar supuestos como acuerdos.
6. Mantener trazabilidad entre `REQ-ID`, escenarios, `TASK-ID`, pruebas, controles, evidencias y aceptaciÃƒÆ’Ã‚Â³n.
7. No falsificar ejecuciones, resultados, coberturas, auditorÃƒÆ’Ã‚Â­as ni validaciones. Si una herramienta falta o falla, seÃƒÆ’Ã‚Â±alarlo como **NO VERIFICADO**.
8. Redactar documentaciÃƒÆ’Ã‚Â³n y explicaciones en espaÃƒÆ’Ã‚Â±ol de Canarias, claro y profesional. Emplear identificadores y cÃƒÆ’Ã‚Â³digo en inglÃƒÆ’Ã‚Â©s, salvo convenciÃƒÆ’Ã‚Â³n del repositorio.

## Elegir el modo antes de actuar

| Modo | AutorizaciÃƒÆ’Ã‚Â³n que aporta el usuario | Acciones permitidas | LÃƒÆ’Ã‚Â­mite |
|---|---|---|---|
| `EXPLORAR` | Idea, preguntas, anÃƒÆ’Ã‚Â¡lisis o auditorÃƒÆ’Ã‚Â­a | Lectura, diagnÃƒÆ’Ã‚Â³stico, informe y propuestas | No escribir archivos en el repositorio |
| `DOCUMENTAR` | Pide explÃƒÆ’Ã‚Â­citamente crear/corregir documentos | Crear o editar solo documentos y artefactos OpenSpec aprobados | No tocar cÃƒÆ’Ã‚Â³digo ejecutable ni ejecutar migraciones |
| `IMPLEMENTAR` | Pide explÃƒÆ’Ã‚Â­citamente implementar y existe una especificaciÃƒÆ’Ã‚Â³n aceptada | TDD en la tarea autorizada, pruebas y documentaciÃƒÆ’Ã‚Â³n asociada | No ampliar el alcance ni saltarse controles |
| `VERIFICAR` | Pide comprobaciÃƒÆ’Ã‚Â³n o revisiÃƒÆ’Ã‚Â³n | Revisar y ejecutar controles no destructivos autorizados | No corregir archivos sin permiso adicional |
| `CERRAR` | Pide cierre del cambio | Comprobar DoD y preparar evidencias | Archivar, crear commit o publicar SOLO si se autorizan |

Si el modo es incierto, optar por `EXPLORAR` y ofrecer el siguiente paso. La solicitud de usar esta skill no equivale a autorizar cambios en el repositorio.

## OpenCode: elecciÃƒÆ’Ã‚Â³n de agente

- **`Plan`**: anÃƒÆ’Ã‚Â¡lisis, lectura, bÃƒÆ’Ã‚Âºsqueda y auditorÃƒÆ’Ã‚Â­a. En la configuraciÃƒÆ’Ã‚Â³n predeterminada de OpenCode v2 **no puede escribir** artefactos OpenSpec dentro del proyecto. Presentar propuestas en la respuesta, sin intentar rodear la restricciÃƒÆ’Ã‚Â³n con comandos shell.
- **`Build`**: usarlo solo tras autorizaciÃƒÆ’Ã‚Â³n para `DOCUMENTAR` o `IMPLEMENTAR`. En el primer caso, aplicar la frontera estricta de solo documentaciÃƒÆ’Ã‚Â³n. Las instrucciones de la skill son controles de proceso, NO una barrera tÃƒÆ’Ã‚Â©cnica de permisos.
- **Subagentes**: asignar revisiones independientes cuando exista un beneficio real, nunca para eludir permisos. Cada subagente puede tener permisos propios; comprobarlos antes de delegar.
- Leer [references/opencode-v2.md](references/opencode-v2.md) al configurar skills, permisos o roles; no mezclar el esquema de configuraciÃƒÆ’Ã‚Â³n de V1 con V2.

## Paso 0. InspecciÃƒÆ’Ã‚Â³n del repositorio (lectura)

1. Identificar raÃƒÆ’Ã‚Â­z del trabajo, `AGENTS.md`, instrucciones locales, tecnologÃƒÆ’Ã‚Â­a, pruebas, documentaciÃƒÆ’Ã‚Â³n y estado Git. No modificar un ÃƒÆ’Ã‚Â¡rbol con cambios previos ajenos.
2. Detectar OpenSpec existente: `openspec/config.yaml`, `openspec/changes`, especificaciones, esquema activo y versiÃƒÆ’Ã‚Â³n de la CLI. No ejecutar `openspec init`, `openspec update` ni crear cambios sin autorizaciÃƒÆ’Ã‚Â³n documental.
3. Si la CLI existe, consultar las instrucciones y el estado del cambio por sus comandos de lectura. Respetar rutas y dependencias devueltas por la versiÃƒÆ’Ã‚Â³n instalada; no asumir que todos los proyectos usan la misma estructura ni un ÃƒÆ’Ã‚Âºnico esquema.
4. Identificar restricciones de cumplimiento, datos sensibles, usuarios, roles, tenants, integraciones y despliegue.
5. Informar: estado observado, fuentes consultadas, contradicciones, lagunas y siguiente acciÃƒÆ’Ã‚Â³n mÃƒÆ’Ã‚Â­nima.

Se puede ejecutar manualmente `scripts/preflight.sh "<ruta-del-proyecto>"` para obtener un diagnÃƒÆ’Ã‚Â³stico no destructivo. No ejecutar scripts desconocidos del repositorio sin inspeccionarlos.

## Flujo SDD con puertas de aprobaciÃƒÆ’Ã‚Â³n

### 1. Descubrimiento y definiciÃƒÆ’Ã‚Â³n

- Establecer problema, objetivo medible, actores, contexto, MVP, fuera de alcance, casos de uso, restricciones, integraciones, datos y amenazas.
- Formular solo preguntas que cambien alcance, arquitectura, seguridad, responsabilidad legal o criterios de aceptaciÃƒÆ’Ã‚Â³n. Agruparlas y proponer alternativas; documentar supuestos reversibles.
- Seleccionar stack a partir del repositorio y las decisiones del proyecto; nunca migrarlo ni actualizarlo implÃƒÆ’Ã‚Â­citamente. Para APIs, preferir contrato OpenAPI si el proyecto lo requiere.
- Describir requisitos funcionales y no funcionales observables: seguridad, privacidad, aislamiento, rendimiento, accesibilidad, internacionalizaciÃƒÆ’Ã‚Â³n, observabilidad, recuperaciÃƒÆ’Ã‚Â³n y mantenimiento.

**Puerta D0:** decisiones crÃƒÆ’Ã‚Â­ticas resueltas o marcadas `BLOQUEANTE`. Sin aceptaciÃƒÆ’Ã‚Â³n, detenerse en la propuesta documental.

### 2. Contrato OpenSpec

- Si OpenSpec ya estÃƒÆ’Ã‚Â¡ configurado, **reutilizar su esquema** y los flujos instalados.
- Si no lo estÃƒÆ’Ã‚Â¡, proponer su inicializaciÃƒÆ’Ã‚Â³n; ejecutarla ÃƒÆ’Ã‚Âºnicamente con autorizaciÃƒÆ’Ã‚Â³n en `DOCUMENTAR`.
- Para cada cambio, definir propuesta, requisitos y escenarios verificables, diseÃƒÆ’Ã‚Â±o, dependencias y tareas conforme a la plantilla que entregue `openspec instructions`. En el esquema habitual `spec-driven` suelen corresponder a `proposal.md`, `specs/`, `design.md`, `tasks.md`, pero no asumir esos nombres si el esquema indica otros.
- Asegurar manejo de migraciones, retrocompatibilidad, rollback, seguridad y aceptaciÃƒÆ’Ã‚Â³n donde corresponda.
- Consultar [references/workflow.md](references/workflow.md) para secuencia, comandos y transiciones.

**Puerta D1 / DoR:** requisitos, escenarios y criterios de aceptaciÃƒÆ’Ã‚Â³n documentados, sin contradicciones bloqueantes y aceptados por el usuario. Documento creado no significa documento aprobado.

### 3. PlanificaciÃƒÆ’Ã‚Â³n atÃƒÆ’Ã‚Â³mica

- Construir tareas pequeÃƒÆ’Ã‚Â±as y ordenadas por dependencia. Asociar por tarea: IDs de requisito/escenario, prueba roja esperada, superficie de cambio, controles de seguridad, documentaciÃƒÆ’Ã‚Â³n y evidencia.
- Respetar Jira, GitFlow y convenciones de rama/commits **solo cuando existan**; no inventar IDs.
- Usar [references/traceability.md](references/traceability.md) para matriz, DoR/DoS/DoD y formatos de evidencia.

**Puerta D2 / DoS:** tarea lista, entorno y estrategia de pruebas identificados, riesgos acotados y autorizaciÃƒÆ’Ã‚Â³n explÃƒÆ’Ã‚Â­cita para empezar a implementar. Si solo se autorizaron documentos, PARAR aquÃƒÆ’Ã‚Â­.

### 4. EjecuciÃƒÆ’Ã‚Â³n TDD (solo modo IMPLEMENTAR)

1. Tomar una ÃƒÆ’Ã‚Âºnica tarea preparada y leer sus requisitos y escenarios.
2. Escribir prueba del comportamiento primero; constatar fallo por el motivo esperado (**rojo**).
3. Implementar el mÃƒÆ’Ã‚Â­nimo comportamiento (**verde**) y refactorizar sin romper pruebas.
4. Ejecutar regresiÃƒÆ’Ã‚Â³n y controles de calidad/seguridad correspondientes al riesgo.
5. Actualizar especificaciÃƒÆ’Ã‚Â³n, documentaciÃƒÆ’Ã‚Â³n, matriz y evidencia en la misma unidad de trabajo.
6. En caso de discrepancia: detener la tarea, exponer contradicciÃƒÆ’Ã‚Â³n y proponer revisiÃƒÆ’Ã‚Â³n OpenSpec antes de continuar.

Usar [references/quality-security.md](references/quality-security.md) al decidir stack, pruebas, seguridad, API y controles.

### 5. Verificar y cerrar

- En `VERIFICAR` ejecutar validaciones no destructivas: estructura OpenSpec, pruebas, anÃƒÆ’Ã‚Â¡lisis estÃƒÆ’Ã‚Â¡tico, seguridad, integraciones y trazabilidad segÃƒÆ’Ã‚Âºn el cambio.
- No declarar una tarea finalizada con verificaciones obligatorias fallidas, pendientes o no ejecutadas. Distinguir `SUPERADO`, `FALLIDO`, `NO EJECUTADO` y `NO APLICA` justificado.
- Mantener documentaciÃƒÆ’Ã‚Â³n viva pertinente (`README.md`, `ARCHITECTURE.md`, `SECURITY.md`, `CONFIGURATION.md`, `INTEGRATIONS.md`, `CHANGELOG.md`, y `VERSION.md` si aplica). Si existe registro de auditorÃƒÆ’Ã‚Â­a, respetar su nombre; para uno nuevo, preferir `AUDIT.md`.
- **Puerta D3 / DoD:** criterios demostrados, QA y seguridad sin bloqueos, trazabilidad y evidencia reproducible, coherencia cÃƒÆ’Ã‚Â³digo-especificaciÃƒÆ’Ã‚Â³n-documentaciÃƒÆ’Ã‚Â³n y aceptaciÃƒÆ’Ã‚Â³n. Commits, `git push`, sincronizaciÃƒÆ’Ã‚Â³n y archivo de cambios se ejecutan solo con autorizaciÃƒÆ’Ã‚Â³n expresa.
- No archivar un cambio OpenSpec antes de su verificaciÃƒÆ’Ã‚Â³n y aceptaciÃƒÆ’Ã‚Â³n.

## Entrega adaptada al modo

Responder con la informaciÃƒÆ’Ã‚Â³n necesaria para actuar: estado, evidencia y rutas concretas; decisiones/supuestos/bloqueos; requisitos y artefactos afectados; prÃƒÆ’Ã‚Â³ximo paso verificable. En `EXPLORAR`, mostrar propuestas sin escribir. En `DOCUMENTAR`, informar archivos realmente creados y controles documentales. En `IMPLEMENTAR`, informar tarea, resultados de TDD y pruebas, diferencias y documentaciÃƒÆ’Ã‚Â³n actualizada. Nunca marcar realizado algo que solo se ha recomendado.

## Recursos de lectura selectiva

- [references/workflow.md](references/workflow.md): proceso por fases y OpenSpec CLI/comandos `opsx`.
- [references/traceability.md](references/traceability.md): registros por tarea, matriz, evidencia y puertas DoR/DoS/DoD.
- [references/opencode-v2.md](references/opencode-v2.md): ubicaciÃƒÆ’Ã‚Â³n de skills, `Plan`/`Build`, permisos V2 y precedencia.
- [references/quality-security.md](references/quality-security.md): estrategias PHP/Java, seguridad, SaaS y QA.
- [references/prompt-examples.md](references/prompt-examples.md): formas de invocaciÃƒÆ’Ã‚Â³n seguras.
