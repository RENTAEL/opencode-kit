---
name: skill_setup_environment
description: "Esta habilidad aÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­sla el entorno de desarrollo mediante un entorno virtual de Python, instala las dependencias del stack analÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­tico y asegura las polÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­ticas de exclusiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de Git."
---
# SKILL: CONFIGURACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN DEL ENTORNO VIRTUAL PYTHON (FASE 0 - PASO 2)

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Esta habilidad aÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­sla el entorno de desarrollo mediante un entorno virtual de Python, instala las dependencias del stack analÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­tico y asegura las polÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­ticas de exclusiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de Git.

## INSTRUCCIONES PARA EL AGENTE
1. Lanza la pregunta de confirmaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n: **"ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Deseas crear el entorno virtual de Python e instalar las dependencias (dbt, DuckDB, pandas, Jupyter, matplotlib, seaborn)? (S/N)"**.
2. Si la respuesta es "S", ejecuta en la terminal raÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­z:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install dbt-duckdb pandas jupyter ipykernel matplotlib seaborn
pip freeze > requirements.txt

# Guard: aÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±adir entradas al .gitignore solo si no existen ya
for entry in ".venv/" "data/" "*.duckdb" "*.duckdb.wal" "__pycache__/" ".env" ".agents/" "logs/" "outputs/" "AGENTS.md" "opencode.json" "docs/*" "!docs/SLA.md"; do
  grep -qxF "$entry" .gitignore || echo "$entry" >> .gitignore
done