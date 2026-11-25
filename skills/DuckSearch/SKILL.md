---
name: DuckSearch
description: "Permite realizar bÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºsquedas web utilizando DuckDuckGo directamente desde Reinike Bot."
---
# DuckSearch Skill

## PropÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³sito
Permite realizar bÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºsquedas web utilizando DuckDuckGo directamente desde Reinike Bot.

## Comandos disponibles

### BÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºsqueda bÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡sica
```bash
python duck_search.py <query>
powershell duck_search.ps1 -Query "<query>"
```

Donde `<query>` es el tÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rmino de bÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºsqueda.

## Ejemplos de uso

### Python
```bash
python duck_search.py "chile noticias"
python duck_search.py "recetas de cocina"
python duck_search.py "python tutorials"
```

### PowerShell
```powershell
.\duck_search.ps1 -Query "chile noticias"
.\duck_search.ps1 -Query "recetas de cocina"
.\duck_search.ps1 -Query "python tutorials"
```

## Requisitos
- Python 3.7+
- Paquete `ddgs`: `pip install ddgs`

## Salida
El script retorna hasta 10 resultados con:
- TÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­tulo del resultado
- URL
- DescripciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n (truncada a 200 caracteres)
