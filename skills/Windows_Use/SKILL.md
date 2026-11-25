---
name: Windows_Use
description: "AutomatizaciÃƒÆ’Ã‚Â³n de escritorio Windows mediante el paquete `windows-use`."
---
# Windows-Use Skill

AutomatizaciÃƒÆ’Ã‚Â³n de escritorio Windows mediante el paquete `windows-use`.

## ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â CONFIRMACIÃƒÆ’Ã¢â‚¬Å“N REQUERIDA

**Este skill requiere confirmaciÃƒÆ’Ã‚Â³n del usuario ANTES de ejecutarse.**

El agente @computer debe:
1. Explicar quÃƒÆ’Ã‚Â© acciÃƒÆ’Ã‚Â³n va a realizar
2. Pedir permiso explÃƒÆ’Ã‚Â­cito
3. Esperar confirmaciÃƒÆ’Ã‚Â³n antes de ejecutar

El agente debe retornar:
```
[WINDOWS_USE_CONFIRMATION_REQUIRED]
Task: <descripciÃƒÆ’Ã‚Â³n de la acciÃƒÆ’Ã‚Â³n>
Reason: <por quÃƒÆ’Ã‚Â© es necesaria>
Risk: <riesgos potenciales>
```

## PropÃƒÆ’Ã‚Â³sito

Usa este skill cuando el subagente @computer necesite control de GUI en el escritorio local de Windows: abrir aplicaciones, hacer clic, escribir, cambiar ventanas, o completar tareas interactivas cortas.

## Requisitos

- Windows
- Python 3.10+
- `pip install windows-use`
- Un proveedor LLM configurado (por defecto OpenRouter)

## Script

- `.\.opencode\skills\Windows_Use\scripts\Invoke-WindowsUse.ps1`

## Uso

### Desde OpenCode (subagente @computer)

```powershell
[CMD: powershell -File ".\.opencode\skills\Windows_Use\scripts\Invoke-WindowsUse.ps1" -Task "Open Notepad and type a short note" -Provider "openrouter" -Model "minimax/minimax-m2.7" -ReasoningEffort "medium"]
```

**Importante:** Desde OpenCode, siempre usar `-Provider "openrouter" -Model "minimax/minimax-m2.7" -ReasoningEffort "medium"`.

### Desde el orquestador (Telegram)

```powershell
[CMD: powershell -File ".\.opencode\skills\Windows_Use\scripts\Invoke-WindowsUse.ps1" -Task "Open Notepad and type a short note"]
```

Usa la configuraciÃƒÆ’Ã‚Â³n por defecto de `config/settings.json` (minimax/minimax-m2.7 con reasoning medium).

## ParÃƒÆ’Ã‚Â¡metros opcionales

- `-Provider openrouter|openai|anthropic|google|groq|ollama`
- `-Model "model-name"`
- `-Browser edge|chrome|firefox`
- `-MaxSteps 25`
- `-UseVision`
- `-Experimental`
- `-RunnerDebug`

## Capacidades

Este skill permite al subagente @computer:

- **Abrir aplicaciones**: Notepad, Calculator, Outlook, navegadores, etc.
- **Control de mouse**: Clic, doble clic, arrastrar, scroll
- **Control de teclado**: Escribir texto, presionar teclas, atajos
- **GestiÃƒÆ’Ã‚Â³n de ventanas**: Cambiar, minimizar, maximizar, cerrar
- **InteracciÃƒÆ’Ã‚Â³n con GUI**: Botones, campos de texto, menÃƒÆ’Ã‚Âºs, diÃƒÆ’Ã‚Â¡logos
- **Capturas de pantalla**: Para tareas con visiÃƒÆ’Ã‚Â³n habilitada

## Seguridad

- Este skill puede controlar el escritorio y aplicaciones en vivo.
- Requiere confirmaciÃƒÆ’Ã‚Â³n antes de la ejecuciÃƒÆ’Ã‚Â³n.
- Mantener las tareas acotadas y explÃƒÆ’Ã‚Â­citas.
- Preferir una VM o mÃƒÆ’Ã‚Â¡quina de prueba para automatizaciones riesgosas.

## ConfiguraciÃƒÆ’Ã‚Â³n

El skill lee su configuraciÃƒÆ’Ã‚Â³n desde `config/settings.json` bajo la secciÃƒÆ’Ã‚Â³n `windowsUse`:

```json
{
  "windowsUse": {
    "enabled": true,
    "provider": "openrouter",
    "model": "minimax/minimax-m2.7",
    "reasoningEffort": "medium",
    "browser": "edge",
    "maxSteps": 30,
    "useVision": false,
    "experimental": true
  }
}
```
