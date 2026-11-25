---
name: resume-ats-beater
description: "Aplicar as orientaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes deste skill considerando o cenÃƒÆ’Ã‚Â¡rio brasileiro de ATS (Gupy, Vagas.com, PandaPÃƒÆ’Ã‚Â© e SÃƒÆ’Ã‚Â³lides), no qual o ranqueamento combina parsing do currÃƒÆ’Ã‚Â­culo, aderÃƒÆ’Ã‚Âªncia semÃƒÆ’Ã‚Â¢ntica ÃƒÆ’Ã‚Â vaga, requisitos eliminatÃ..."
---
# Resume ATS Beater + LinkedIn Optimizer

## Contexto ATS no Brasil

Aplicar as orientaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes deste skill considerando o cenÃƒÆ’Ã‚Â¡rio brasileiro de ATS (Gupy, Vagas.com, PandaPÃƒÆ’Ã‚Â© e SÃƒÆ’Ã‚Â³lides), no qual o ranqueamento combina parsing do currÃƒÆ’Ã‚Â­culo, aderÃƒÆ’Ã‚Âªncia semÃƒÆ’Ã‚Â¢ntica ÃƒÆ’Ã‚Â  vaga, requisitos eliminatÃƒÆ’Ã‚Â³rios, histÃƒÆ’Ã‚Â³rico de progressÃƒÆ’Ã‚Â£o e desempenho em testes da plataforma. Tratar o processo como otimizaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de score e ordenaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o, nÃƒÆ’Ã‚Â£o como aprovaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o binÃƒÆ’Ã‚Â¡ria.

Aplicar avaliaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o com perspectiva dupla: especialista tÃƒÆ’Ã‚Â©cnico em ATS e recrutador experiente no `cargo_alvo` e `industria_alvo`. Conciliar as duas lentes para maximizar parse/ranqueamento ATS e impacto na leitura humana de 6 segundos.

## Modos de execuÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o

Executar em um dos modos abaixo. Quando nÃƒÆ’Ã‚Â£o especificado, adotar `modo_completo` como padrÃƒÆ’Ã‚Â£o e informar o usuÃƒÆ’Ã‚Â¡rio.

1. `modo_diagnostico`: analisar currÃƒÆ’Ã‚Â­culo atual e apontar melhorias ATS sem reescrita integral.
2. `modo_reescrita`: reescrever currÃƒÆ’Ã‚Â­culo completo sem entregar diagnÃƒÆ’Ã‚Â³stico detalhado.
3. `modo_completo`: executar diagnÃƒÆ’Ã‚Â³stico estruturado e, em seguida, entregar reescrita final.
4. `modo_linkedin`: auditoria completa do perfil LinkedIn com score, findings, fix prompts e mega-prompt de reescrita.
5. `modo_unificado`: executa `modo_completo` (CV) + `modo_linkedin` em sequÃƒÆ’Ã‚Âªncia, garantindo consistÃƒÆ’Ã‚Âªncia entre ambos.

## ParÃƒÆ’Ã‚Â¢metros de entrada

### ObrigatÃƒÆ’Ã‚Â³rios

Coletar antes de qualquer outra aÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o. Se `curriculo_atual` estiver ausente em modos CV, solicitÃƒÆ’Ã‚Â¡-lo imediatamente e nÃƒÆ’Ã‚Â£o prosseguir.

- `curriculo_atual` (texto ou arquivo): conteÃƒÆ’Ã‚Âºdo completo do currÃƒÆ’Ã‚Â­culo atual. ObrigatÃƒÆ’Ã‚Â³rio em modos CV (diagnostico, reescrita, completo, unificado).
- `cargo_alvo` (texto): cargo principal buscado.
- `industria_alvo` (texto): segmento/mercado alvo.
- `nivel_senioridade_alvo` (texto): jÃƒÆ’Ã‚Âºnior, pleno, sÃƒÆ’Ã‚Âªnior, lideranÃƒÆ’Ã‚Â§a etc.
- `idioma_curriculo` (texto): idioma final do currÃƒÆ’Ã‚Â­culo.
- `requisitos_eliminatorios` (lista): critÃƒÆ’Ã‚Â©rios mandatÃƒÆ’Ã‚Â³rios da vaga (ex.: inglÃƒÆ’Ã‚Âªs fluente, cidade, certificaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o, disponibilidade).
- `modo_execucao` (texto): `modo_diagnostico`, `modo_reescrita`, `modo_completo`, `modo_linkedin` ou `modo_unificado`.

### ObrigatÃƒÆ’Ã‚Â³rios para modo LinkedIn / unificado

- `perfil_linkedin` (texto ou URL): conteÃƒÆ’Ã‚Âºdo do perfil LinkedIn (headline, about, experiÃƒÆ’Ã‚Âªncias, skills, featured, configuraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes) ou URL para anÃƒÆ’Ã‚Â¡lise.

### Recomendados

- `descricao_vaga` (texto): descriÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o da vaga alvo para extraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de palavras-chave.
- `especificacao_vaga_completa` (texto): vaga completa (requisitos, responsabilidades, habilidades, empresa, benefÃƒÆ’Ã‚Â­cios e contexto).
- `metricas_por_experiencia` (lista): resultados por cargo (%, R$, tempo, volume, NPS, SLA etc.).
- `localizacao_alvo` (texto): paÃƒÆ’Ã‚Â­s/regiÃƒÆ’Ã‚Â£o/cidade para adaptar vocabulÃƒÆ’Ã‚Â¡rio e contexto.
- `skills_prioritarias` (lista): competÃƒÆ’Ã‚Âªncias estratÃƒÆ’Ã‚Â©gicas a enfatizar.
- `plataforma_ats_alvo` (texto): Gupy, Vagas.com, PandaPÃƒÆ’Ã‚Â©, SÃƒÆ’Ã‚Â³lides ou "nÃƒÆ’Ã‚Â£o informado". Quando informada, priorizar vocabulÃƒÆ’Ã‚Â¡rio e critÃƒÆ’Ã‚Â©rios especÃƒÆ’Ã‚Â­ficos da plataforma.
- `historico_linkedin` (objeto): datas/cargos/empresas para checagem de consistÃƒÆ’Ã‚Âªncia com currÃƒÆ’Ã‚Â­culo.
- `detalhes_educacao` (objeto): GPA/CR, honras, certificaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes, projetos acadÃƒÆ’Ã‚Âªmicos.
- `status_testes_plataforma` (objeto): testes exigidos e resultado atual (lÃƒÆ’Ã‚Â³gica, portuguÃƒÆ’Ã‚Âªs, fit cultural etc.).
- `secoes_prioritarias_cv` (lista): seÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes que exigem otimizaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o imediata.
- `ssi_scores` (objeto): pontuaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o SSI do LinkedIn (4 pilares + total). Opcional; quando fornecido, enriquece diagnÃƒÆ’Ã‚Â³stico.
- `mercado_alvo` (texto): `brasil`, `gringa` ou `ambos`. Afeta idioma, formato de headline e vocabulÃƒÆ’Ã‚Â¡rio.
- `cargo_preset` (texto): preset de cargo para aplicar padrÃƒÆ’Ã‚Âµes especÃƒÆ’Ã‚Â­ficos. Exemplos disponÃƒÆ’Ã‚Â­veis em `references/presets-formatos.md`. O usuÃƒÆ’Ã‚Â¡rio pode definir qualquer cargo ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â presets sÃƒÆ’Ã‚Â£o apenas atalhos.

### RestriÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes de seguranÃƒÆ’Ã‚Â§a factual

- NÃƒÆ’Ã‚Â£o inventar conquistas, nÃƒÆ’Ã‚Âºmeros, certificaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes ou responsabilidades.
- Solicitar complementos quando faltarem mÃƒÆ’Ã‚Â©tricas relevantes.
- Preservar todos os cargos e formaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes existentes; alterar apenas quando correÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o factual for solicitada pelo usuÃƒÆ’Ã‚Â¡rio.
- Para LinkedIn: nÃƒÆ’Ã‚Â£o fabricar endorsements, recomendaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes ou mÃƒÆ’Ã‚Â©tricas de engajamento.

---

## Workflow operacional ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â CV (modos diagnostico, reescrita, completo)

### Etapa 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Validar objetivo e contexto

1. Confirmar `curriculo_atual`; solicitar imediatamente se ausente.
2. Confirmar `cargo_alvo`, `industria_alvo`, `nivel_senioridade_alvo` e `idioma_curriculo`.
3. Solicitar `descricao_vaga` se nÃƒÆ’Ã‚Â£o fornecida; informar ao usuÃƒÆ’Ã‚Â¡rio que a anÃƒÆ’Ã‚Â¡lise serÃƒÆ’Ã‚Â¡ mais genÃƒÆ’Ã‚Â©rica sem ela.
4. Coletar `requisitos_eliminatorios` e sinalizar riscos de eliminaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o prÃƒÆ’Ã‚Â¡tica.
5. Identificar lacunas crÃƒÆ’Ã‚Â­ticas de dados, especialmente mÃƒÆ’Ã‚Â©tricas por experiÃƒÆ’Ã‚Âªncia.
6. Confirmar `modo_execucao`; adotar `modo_completo` se nÃƒÆ’Ã‚Â£o especificado.
7. Pausar e coletar dados mÃƒÆ’Ã‚Â­nimos antes de avanÃƒÆ’Ã‚Â§ar.

### Etapa 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Diagnosticar currÃƒÆ’Ã‚Â­culo e aderÃƒÆ’Ã‚Âªncia ATS

> Executar esta etapa em `modo_diagnostico` e `modo_completo`. Pular para Etapa 3 em `modo_reescrita`.

1. Mapear estrutura atual (resumo, experiÃƒÆ’Ã‚Âªncia, educaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o, skills).
2. Medir aderÃƒÆ’Ã‚Âªncia semÃƒÆ’Ã‚Â¢ntica com a vaga (competÃƒÆ’Ã‚Âªncias, termos tÃƒÆ’Ã‚Â©cnicos e contexto).
3. Identificar hard skills, soft skills e palavras-chave ausentes de alta prioridade.
4. Identificar bullets fracos (tarefa sem impacto), jargÃƒÆ’Ã‚Âµes vazios e habilidades obsoletas.
5. Verificar sinais de progressÃƒÆ’Ã‚Â£o de carreira e lacunas temporais.
6. Confirmar consistÃƒÆ’Ã‚Âªncia com `historico_linkedin`, quando fornecido.
7. Aplicar os quatro eixos de anÃƒÆ’Ã‚Â¡lise definidos em `references/diagnostico-ats.md`.
8. Quando `descricao_vaga` ou `especificacao_vaga_completa` disponÃƒÆ’Ã‚Â­vel, aplicar tambÃƒÆ’Ã‚Â©m o diagnÃƒÆ’Ã‚Â³stico avanÃƒÆ’Ã‚Â§ado definido em `references/diagnostico-avancado.md`.

### Etapa 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Reescrever do zero com padrÃƒÆ’Ã‚Â£o ATS

> Executar em `modo_reescrita` e `modo_completo`. Em `modo_diagnostico`, encerrar na Etapa 2.

1. Reconstruir o currÃƒÆ’Ã‚Â­culo integralmente; nÃƒÆ’Ã‚Â£o fazer ediÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o superficial.
2. Manter todos os cargos e entradas de educaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o existentes.
3. Produzir `Resumo Profissional` em 3ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“4 linhas com identidade, anos de experiÃƒÆ’Ã‚Âªncia, forÃƒÆ’Ã‚Â§as centrais e proposta de valor.
4. Reescrever cada experiÃƒÆ’Ã‚Âªncia com 4ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“6 bullets orientados a resultado.
5. Priorizar verbos de aÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o e impacto mensurÃƒÆ’Ã‚Â¡vel.
6. Inserir palavras-chave do alvo de forma natural.
7. Escrever datas por extenso (ex.: "Janeiro de 2020 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“ Dezembro de 2021") para reduzir erro de cÃƒÆ’Ã‚Â¡lculo de experiÃƒÆ’Ã‚Âªncia.
8. Manter layout de coluna ÃƒÆ’Ã‚Âºnica e leitura linear.

Formato por experiÃƒÆ’Ã‚Âªncia:

```
Cargo
Empresa | Local | Datas

ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¢ Bullet orientado a impacto
ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¢ Bullet orientado a impacto
ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¢ Bullet orientado a impacto
ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¢ Bullet orientado a impacto
```

### Etapa 4 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Otimizar educaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o e competÃƒÆ’Ã‚Âªncias

1. Manter grau, instituiÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o e ano de conclusÃƒÆ’Ã‚Â£o.
2. Melhorar clareza e padronizaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o da seÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de educaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o.
3. Incluir honras, cursos relevantes, certificaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes e projetos apenas quando informados pelo usuÃƒÆ’Ã‚Â¡rio.
4. Organizar competÃƒÆ’Ã‚Âªncias por categorias (`TÃƒÆ’Ã‚Â©cnicas`, `Ferramentas`, `Interpessoais`, `Idiomas`).
5. Remover competÃƒÆ’Ã‚Âªncias desatualizadas ou desalinhadas com o `cargo_alvo`.

### Etapa 5 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Validar conformidade ATS

1. Usar cabeÃƒÆ’Ã‚Â§alhos padrÃƒÆ’Ã‚Â£o: `Resumo Profissional`, `ExperiÃƒÆ’Ã‚Âªncia Profissional`, `FormaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o AcadÃƒÆ’Ã‚Âªmica`, `CompetÃƒÆ’Ã‚Âªncias`. Evitar tÃƒÆ’Ã‚Â­tulos criativos.
2. Evitar tabelas, mÃƒÆ’Ã‚Âºltiplas colunas, grÃƒÆ’Ã‚Â¡ficos, caixas de texto, ÃƒÆ’Ã‚Â­cones e fotos.
3. Garantir legibilidade linear para parser ATS.
4. Garantir consistÃƒÆ’Ã‚Âªncia de datas, verbos e densidade de palavras-chave ao longo do documento.
5. Usar termos exatos da vaga e, quando ÃƒÆ’Ã‚Âºtil, variaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes com siglas e nomes completos.
6. Confirmar formato de arquivo final: DOCX ou PDF textual, nunca imagem escaneada.

### Etapa 6 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Entregar saÃƒÆ’Ã‚Â­da final CV

Estruturar a entrega conforme `references/template-saida.md`, respeitando o escopo do `modo_execucao`:

- **Todos os modos CV**: itens 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“5 (currÃƒÆ’Ã‚Â­culo reescrito, resumo de melhorias, palavras-chave, checklist eliminatÃƒÆ’Ã‚Â³rios, riscos de ranking).
- **`modo_diagnostico` / `modo_completo`**: adicionar diagnÃƒÆ’Ã‚Â³stico padrÃƒÆ’Ã‚Â£o (eixos IÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“V).
- **Qualquer modo com vaga definida**: adicionar diagnÃƒÆ’Ã‚Â³stico avanÃƒÆ’Ã‚Â§ado (PARTES A, B e C).

---

## Workflow operacional ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â LinkedIn (modo_linkedin, modo_unificado)

### Etapa L1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Coletar perfil e contexto

1. Confirmar `perfil_linkedin` (conteÃƒÆ’Ã‚Âºdo textual ou URL).
2. Confirmar `cargo_alvo`, `industria_alvo`, `nivel_senioridade_alvo`.
3. Identificar `mercado_alvo` (brasil/gringa/ambos) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â afeta idioma e formato.
4. Coletar `ssi_scores` se disponÃƒÆ’Ã‚Â­vel; informar que enriquece a anÃƒÆ’Ã‚Â¡lise mas nÃƒÆ’Ã‚Â£o ÃƒÆ’Ã‚Â© obrigatÃƒÆ’Ã‚Â³rio.
5. Verificar se hÃƒÆ’Ã‚Â¡ `cargo_preset` aplicÃƒÆ’Ã‚Â¡vel ou definir padrÃƒÆ’Ã‚Âµes genÃƒÆ’Ã‚Â©ricos.

### Etapa L2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Auditar por ÃƒÆ’Ã‚Â¡rea

Auditar cada ÃƒÆ’Ã‚Â¡rea do perfil LinkedIn aplicando regras de severidade. Para cada finding, classificar como:

| Severidade | Penalidade | Significado |
|---|---|---|
| `critical` | -15 pts | Problema grave que prejudica visibilidade ou causa impressÃƒÆ’Ã‚Â£o negativa imediata |
| `warning` | -6 pts | Oportunidade perdida significativa |
| `info` | -2 pts | Melhoria incremental recomendada |
| `ok` | 0 pts | ÃƒÆ’Ã‚Ârea adequada, sem aÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o necessÃƒÆ’Ã‚Â¡ria |

**ÃƒÆ’Ã‚Âreas auditadas:**

1. **Foto e banner**: presenÃƒÆ’Ã‚Â§a, qualidade profissional, alinhamento com ÃƒÆ’Ã‚Â¡rea.
2. **Headline**: formato, keywords, diferenciaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ver formato obrigatÃƒÆ’Ã‚Â³rio abaixo.
3. **About/Resumo**: estrutura, storytelling, CTA, keywords, comprimento.
4. **ExperiÃƒÆ’Ã‚Âªncias**: bullets com impacto, mÃƒÆ’Ã‚Â©tricas, verbos de aÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o, progressÃƒÆ’Ã‚Â£o.
5. **Idioma do perfil**: coerÃƒÆ’Ã‚Âªncia com `mercado_alvo`.
6. **Skills & Endorsements**: quantidade, relevÃƒÆ’Ã‚Â¢ncia, ordenaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o.
7. **Featured/Destaques**: presenÃƒÆ’Ã‚Â§a, qualidade, atualizaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o.
8. **ConfiguraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes de visibilidade**: Open to Work, Creator Mode, URL customizada.
9. **RecomendaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes**: quantidade, diversidade (recebidas e dadas).
10. **Atividade/Engajamento**: frequÃƒÆ’Ã‚Âªncia de posts, comentÃƒÆ’Ã‚Â¡rios, artigos.

#### Formato obrigatÃƒÆ’Ã‚Â³rio de headline

```
PosiÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o | ÃƒÆ’Ã‚Âreas fortes | CompetÃƒÆ’Ã‚Âªncias-chave (separadas por Ãƒâ€šÃ‚Â·)
```

**Exemplos por ÃƒÆ’Ã‚Â¡rea:**

- Marketing: `Head de Growth | AquisiÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o Ãƒâ€šÃ‚Â· CRO Ãƒâ€šÃ‚Â· Dados | Google Ads Ãƒâ€šÃ‚Â· HubSpot Ãƒâ€šÃ‚Â· SQL`
- FinanÃƒÆ’Ã‚Â§as: `Controller SÃƒÆ’Ã‚Âªnior | FP&A Ãƒâ€šÃ‚Â· Tesouraria Ãƒâ€šÃ‚Â· M&A | SAP Ãƒâ€šÃ‚Â· Power BI Ãƒâ€šÃ‚Â· IFRS`
- Engenharia Civil: `Gerente de Obras | Infraestrutura Ãƒâ€šÃ‚Â· OrÃƒÆ’Ã‚Â§amento Ãƒâ€šÃ‚Â· Planejamento | MS Project Ãƒâ€šÃ‚Â· AutoCAD Ãƒâ€šÃ‚Â· BIM`
- Dados: `Data Engineer SÃƒÆ’Ã‚Âªnior | Pipelines Ãƒâ€šÃ‚Â· Lakehouse Ãƒâ€šÃ‚Â· MLOps | Spark Ãƒâ€šÃ‚Â· dbt Ãƒâ€šÃ‚Â· Airflow`
- JurÃƒÆ’Ã‚Â­dico: `Advogado Tributarista | Planejamento Fiscal Ãƒâ€šÃ‚Â· Contencioso Ãƒâ€šÃ‚Â· M&A | Thomson Reuters Ãƒâ€šÃ‚Â· SPED`
- Dev: `Staff Engineer | Backend Ãƒâ€šÃ‚Â· Plataforma Ãƒâ€šÃ‚Â· Observabilidade | Go Ãƒâ€šÃ‚Â· K8s Ãƒâ€šÃ‚Â· Terraform`

**Regras da headline:**
- MÃƒÆ’Ã‚Â¡ximo 220 caracteres (limite LinkedIn).
- Sem buzzwords genÃƒÆ’Ã‚Â©ricas (ver constantes abaixo).
- PosiÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o deve refletir o cargo almejado, nÃƒÆ’Ã‚Â£o necessariamente o atual.
- ÃƒÆ’Ã‚Âreas fortes: 2ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“3 domÃƒÆ’Ã‚Â­nios de especializaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o.
- CompetÃƒÆ’Ã‚Âªncias-chave: 3ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“5 termos tÃƒÆ’Ã‚Â©cnicos/ferramentas separados por `Ãƒâ€šÃ‚Â·`.

### Etapa L3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Calcular score

Score punitivo: inicia em 100 e subtrai penalidades.

```
score_final = 100 - (qtd_critical ÃƒÆ’Ã¢â‚¬â€ 15) - (qtd_warning ÃƒÆ’Ã¢â‚¬â€ 6) - (qtd_info ÃƒÆ’Ã¢â‚¬â€ 2)
```

**ClassificaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o:**

| Faixa | Status |
|---|---|
| 90ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“100 | Excelente ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â perfil competitivo |
| 75ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“89 | Bom ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ajustes pontuais |
| 60ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“74 | Regular ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â melhorias necessÃƒÆ’Ã‚Â¡rias |
| 40ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“59 | Fraco ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â reescrita recomendada |
| < 40 | CrÃƒÆ’Ã‚Â­tico ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â perfil prejudica candidatura |

### Etapa L4 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â AnÃƒÆ’Ã‚Â¡lise SSI (quando `ssi_scores` fornecido)

#### Como auxiliar o usuÃƒÆ’Ã‚Â¡rio a obter o SSI

Quando o usuÃƒÆ’Ã‚Â¡rio nÃƒÆ’Ã‚Â£o informar `ssi_scores`, instruÃƒÆ’Ã‚Â­-lo com:

> **Para consultar seu SSI:**
> 1. Acesse [linkedin.com/sales/ssi](https://www.linkedin.com/sales/ssi) (precisa estar logado no LinkedIn).
> 2. A pÃƒÆ’Ã‚Â¡gina mostra 4 scores (cada um de 0 a 25) e o total:
>    - **Establish your professional brand** (Laranja)
>    - **Find the right people** (Roxo)
>    - **Engage with insights** (Verde)
>    - **Build relationships** (Verde-ÃƒÆ’Ã‚Â¡gua)
> 3. Me informe os 4 valores com decimais. Exemplo: `17.42, 10.01, 11.00, 15.60`
>
> NÃƒÆ’Ã‚Â£o precisa ter Sales Navigator ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â o link funciona com qualquer conta LinkedIn.

**Se o usuÃƒÆ’Ã‚Â¡rio nÃƒÆ’Ã‚Â£o conseguir acessar:** informar que a anÃƒÆ’Ã‚Â¡lise continua sem SSI, mas perde a camada de diagnÃƒÆ’Ã‚Â³stico comportamental (rede, engajamento, relacionamentos). Prosseguir normalmente com as demais etapas.

**Formato aceito para `ssi_scores`:**
- 4 nÃƒÆ’Ã‚Âºmeros separados por vÃƒÆ’Ã‚Â­rgula na ordem: marca profissional, encontrar pessoas, engajar insights, construir relacionamentos
- Ou objeto com as 4 chaves nomeadas
- Aceitar decimais com ponto ou vÃƒÆ’Ã‚Â­rgula (ex: `17.42` ou `17,42`)

---

O Social Selling Index mede 4 pilares (0ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“25 cada, total 0ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“100):

| Pilar | DescriÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o |
|---|---|
| Marca Profissional | Completude do perfil, publicaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes, engajamento recebido |
| Encontrar Pessoas | Uso de busca, visualizaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de perfis, conexÃƒÆ’Ã‚Âµes estratÃƒÆ’Ã‚Â©gicas |
| Engajar com Insights | Compartilhamento, comentÃƒÆ’Ã‚Â¡rios, artigos publicados |
| Construir Relacionamentos | ConexÃƒÆ’Ã‚Âµes de decisores, taxa de aceitaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o, InMail |

**ClassificaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o por pilar:**

| PontuaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o | Status | AÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o |
|---|---|---|
| 20ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“25 | Excelente | Manter cadÃƒÆ’Ã‚Âªncia |
| 15ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“19 | Bom | OtimizaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes pontuais |
| 10ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“14 | Regular | Plano de aÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o semanal |
| 0ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“9 | Fraco | IntervenÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o urgente |

Para cada pilar abaixo de 15, gerar 2ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“3 tips acionÃƒÆ’Ã‚Â¡veis especÃƒÆ’Ã‚Â­ficos.

### Etapa L5 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Gerar relatÃƒÆ’Ã‚Â³rio + fix prompts + mega-prompt

**RelatÃƒÆ’Ã‚Â³rio de auditoria:**
1. Score final com breakdown de penalidades.
2. Findings organizados por severidade (critical primeiro).
3. Para cada finding: ÃƒÆ’Ã‚Â¡rea, severidade, problema detectado, impacto.
4. ClassificaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o SSI (quando disponÃƒÆ’Ã‚Â­vel).

**Fix prompts individuais:**
Para cada finding critical ou warning, gerar um prompt autÃƒÆ’Ã‚Â´nomo que o usuÃƒÆ’Ã‚Â¡rio pode usar em qualquer LLM para corrigir aquele item especÃƒÆ’Ã‚Â­fico. Formato:

```
## Fix: [ÃƒÆ’Ã‚Ârea] ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [Problema resumido]
Severidade: critical|warning

### Contexto
[O que estÃƒÆ’Ã‚Â¡ errado e por que importa]

### Prompt para correÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o
"Reescreva minha [seÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o] do LinkedIn considerando que sou [cargo_alvo] com experiÃƒÆ’Ã‚Âªncia em [ÃƒÆ’Ã‚Â¡reas]. 
Meu perfil atual diz: [conteÃƒÆ’Ã‚Âºdo atual].
Reescreva para: [critÃƒÆ’Ã‚Â©rios especÃƒÆ’Ã‚Â­ficos da regra violada]."

### Onde editar no LinkedIn
[Caminho exato: Perfil ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Editar ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ SeÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Campo]
```

**Mega-prompt de reescrita completa:**
Gerar um prompt ÃƒÆ’Ã‚Âºnico e consolidado para reescrever o perfil inteiro de uma vez, incorporando:
- Cargo alvo e mercado
- Formato de headline obrigatÃƒÆ’Ã‚Â³rio
- Estrutura de about (storytelling + keywords + CTA)
- PadrÃƒÆ’Ã‚Â£o de bullets de experiÃƒÆ’Ã‚Âªncia
- Skills priorizadas
- Idioma adequado ao `mercado_alvo`

### Etapa L6 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Mapa de ediÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o no LinkedIn

Fornecer instruÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes de navegaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o para cada correÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o:

| SeÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o | Caminho no LinkedIn |
|---|---|
| Foto/Banner | Perfil ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ÃƒÆ’Ã‚Â­cone de cÃƒÆ’Ã‚Â¢mera |
| Headline | Perfil ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ÃƒÆ’Ã‚Â­cone de lÃƒÆ’Ã‚Â¡pis (intro) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ TÃƒÆ’Ã‚Â­tulo |
| About | Perfil ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Sobre ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ÃƒÆ’Ã‚Â­cone de lÃƒÆ’Ã‚Â¡pis |
| ExperiÃƒÆ’Ã‚Âªncia | Perfil ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ExperiÃƒÆ’Ã‚Âªncia ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ + ou lÃƒÆ’Ã‚Â¡pis |
| Skills | Perfil ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ CompetÃƒÆ’Ã‚Âªncias ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ + ou reordenar |
| Featured | Perfil ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Destaques ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ + |
| URL customizada | ConfiguraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Visibilidade ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Editar perfil pÃƒÆ’Ã‚Âºblico ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ URL |
| Open to Work | Perfil ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ botÃƒÆ’Ã‚Â£o "DisponÃƒÆ’Ã‚Â­vel para" |
| Idioma | Perfil ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ lÃƒÆ’Ã‚Â¡pis (intro) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "Nome do perfil em outro idioma" |

---

## Workflow ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Modo unificado

No `modo_unificado`, executar sequencialmente:

1. Workflow CV completo (Etapas 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“6).
2. Workflow LinkedIn completo (Etapas L1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“L6).
3. **Etapa de consistÃƒÆ’Ã‚Âªncia**: verificar alinhamento entre CV e LinkedIn:
   - Cargos e datas idÃƒÆ’Ã‚Âªnticos.
   - Headline LinkedIn coerente com resumo profissional do CV.
   - Keywords presentes em ambos.
   - Sem contradiÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes factuais.
4. Reportar divergÃƒÆ’Ã‚Âªncias encontradas com sugestÃƒÆ’Ã‚Â£o de correÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o.

---

## IntegraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o com skill `humanizar`

Quando a skill `humanizar` estiver disponÃƒÆ’Ã‚Â­vel, aplicÃƒÆ’Ã‚Â¡-la **apÃƒÆ’Ã‚Â³s a geraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de conteÃƒÆ’Ã‚Âºdo** e **antes da validaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o final**, com escopo restrito:

### SeÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes onde rodar `humanizar`
- About / Resumo do LinkedIn
- Resumo Profissional do CV
- Carta de apresentaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o (se houver)

### SeÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes onde NÃƒÆ’Ã†â€™O rodar `humanizar`
- Headline LinkedIn (formato rÃƒÆ’Ã‚Â­gido 3 blocos)
- Bullets de experiÃƒÆ’Ã‚Âªncia (formato ATS: verbo + mÃƒÆ’Ã‚Â©trica + ferramenta + impacto)
- SeÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de competÃƒÆ’Ã‚Âªncias / skills
- EducaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o e certificaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes
- ConfiguraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes (Open to Work, idioma, URL)

### Fluxo com `humanizar`

1. `resume-ats-beater` gera o conteÃƒÆ’Ã‚Âºdo (reescrita/auditoria)
2. `humanizar` roda nas seÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes permitidas (preset sugerido: `corporativo-informal` ou `crÃƒÆ’Ã‚Â´nica` conforme tom do mercado)
3. `resume-ats-beater` valida pÃƒÆ’Ã‚Â³s-humanizaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o:
   - Keywords do cargo-alvo ainda presentes?
   - MÃƒÆ’Ã‚Â©tricas/nÃƒÆ’Ã‚Âºmeros intactos?
   - Comprimento dentro do range (About: 1000-2000 chars)?
   - Nenhuma informaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o factual removida?
4. Se validaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o falhar ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ restaurar trecho afetado da versÃƒÆ’Ã‚Â£o prÃƒÆ’Ã‚Â©-humanizaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o

### Quando NÃƒÆ’Ã†â€™O invocar `humanizar`
- `modo_diagnostico` (nÃƒÆ’Ã‚Â£o hÃƒÆ’Ã‚Â¡ reescrita)
- Quando o usuÃƒÆ’Ã‚Â¡rio pedir explicitamente tom formal/acadÃƒÆ’Ã‚Âªmico
- Textos jurÃƒÆ’Ã‚Â­dicos ou regulatÃƒÆ’Ã‚Â³rios

---

## Constantes

### Buzzwords rejeitadas (nÃƒÆ’Ã‚Â£o usar em headline, about ou bullets)

```
proativo, dinÃƒÆ’Ã‚Â¢mico, resiliente, apaixonado, entusiasta, inovador, 
criativo, visionÃƒÆ’Ã‚Â¡rio, guru, ninja, rockstar, evangelista, 
pensador estratÃƒÆ’Ã‚Â©gico, orientado a resultados (sem dados), 
profissional comprometido, busco novos desafios, em busca de recolocaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o
```

### Verbos de aÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o preferidos (usar em bullets de experiÃƒÆ’Ã‚Âªncia)

```
Liderou, Implementou, Reduziu, Aumentou, Otimizou, Automatizou, 
Negociou, Estruturou, Escalou, Desenvolveu, Migrou, Consolidou, 
Projetou, Integrou, Reestruturou, Capacitou, Mensurou, Viabilizou,
Orquestrou, Acelerou, Recuperou, Transformou, Padronizou
```

### Regex de mÃƒÆ’Ã‚Â©tricas (validar presenÃƒÆ’Ã‚Â§a em bullets)

```
\d+%|\d+x|R\$[\d.,]+|US\$[\d.,]+|\d+\s*(pessoas|clientes|usuÃƒÆ’Ã‚Â¡rios|projetos|contratos|unidades|obras|operaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes)
```

Bullets sem match neste regex em pelo menos 50% das experiÃƒÆ’Ã‚Âªncias geram warning `mÃƒÆ’Ã‚Â©tricas_insuficientes`.

---

## Presets de cargo

Presets sÃƒÆ’Ã‚Â£o atalhos opcionais com padrÃƒÆ’Ã‚Âµes de headline, skills priorizadas e vocabulÃƒÆ’Ã‚Â¡rio tÃƒÆ’Ã‚Â©cnico. DisponÃƒÆ’Ã‚Â­veis em `references/presets-formatos.md`.

O usuÃƒÆ’Ã‚Â¡rio pode definir qualquer cargo ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â presets apenas aceleram a configuraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o.

**Exemplos de presets disponÃƒÆ’Ã‚Â­veis:**

| Preset | ÃƒÆ’Ã‚Ârea |
|---|---|
| `marketing_growth` | Marketing Digital / Growth |
| `dados_engenharia` | Engenharia de Dados |
| `dados_analytics` | Analytics / BI |
| `financas_controller` | Controladoria / FP&A |
| `financas_tesouraria` | Tesouraria / Cash Management |
| `engcivil_obras` | GerÃƒÆ’Ã‚Âªncia de Obras |
| `engcivil_projetos` | Projetos e OrÃƒÆ’Ã‚Â§amento |
| `juridico_tributario` | Direito TributÃƒÆ’Ã‚Â¡rio |
| `juridico_compliance` | Compliance / LGPD |
| `dev_backend` | Desenvolvimento Backend |
| `dev_fullstack` | Desenvolvimento Full Stack |
| `dev_platform` | Platform / SRE / DevOps |
| `produto_pm` | Product Manager |
| `produto_design` | Product Design / UX |
| `vendas_enterprise` | Vendas Enterprise / Key Account |
| `vendas_sdrbdr` | SDR / BDR |
| `rh_hrbp` | HR Business Partner |
| `rh_ta` | Talent Acquisition |

---

## Checklist de qualidade

Verificar antes de entregar:

### CV
- [ ] Resumo profissional objetivo, especÃƒÆ’Ã‚Â­fico e alinhado ao `cargo_alvo`.
- [ ] ExperiÃƒÆ’Ã‚Âªncias com foco em resultado e impacto; mÃƒÆ’Ã‚Â©tricas incluÃƒÆ’Ã‚Â­das quando disponÃƒÆ’Ã‚Â­veis.
- [ ] Nenhuma invenÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o factual; fatos preservados do currÃƒÆ’Ã‚Â­culo original.
- [ ] Estrutura ATS-safe: coluna ÃƒÆ’Ã‚Âºnica, cabeÃƒÆ’Ã‚Â§alhos padrÃƒÆ’Ã‚Â£o, sem elementos grÃƒÆ’Ã‚Â¡ficos.
- [ ] Alinhamento explÃƒÆ’Ã‚Â­cito com cargo, indÃƒÆ’Ã‚Âºstria e senioridade alvo.
- [ ] Requisitos eliminatÃƒÆ’Ã‚Â³rios mapeados e confrontados com status claro.
- [ ] Datas por extenso, coerentes e sem lacunas inexplicadas.
- [ ] ConsistÃƒÆ’Ã‚Âªncia com LinkedIn validada quando dados fornecidos.
- [ ] EquilÃƒÆ’Ã‚Â­brio entre ranqueamento ATS e poder de convencimento em leitura humana rÃƒÆ’Ã‚Â¡pida.

### LinkedIn
- [ ] Headline segue formato obrigatÃƒÆ’Ã‚Â³rio `PosiÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o | ÃƒÆ’Ã‚Âreas | CompetÃƒÆ’Ã‚ÂªnciasÃƒâ€šÃ‚Â·`.
- [ ] About com storytelling + keywords + CTA (nÃƒÆ’Ã‚Â£o muro de texto genÃƒÆ’Ã‚Â©rico).
- [ ] ExperiÃƒÆ’Ã‚Âªncias com bullets de impacto (nÃƒÆ’Ã‚Â£o descriÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de cargo).
- [ ] Sem buzzwords rejeitadas em nenhuma seÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o.
- [ ] Regex de mÃƒÆ’Ã‚Â©tricas aprovado em ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥50% dos bullets.
- [ ] Score calculado e classificado corretamente.
- [ ] Fix prompts gerados para todo finding critical/warning.
- [ ] Mega-prompt coerente com cargo_alvo e mercado_alvo.
- [ ] Mapa de ediÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o fornecido com caminhos corretos.
- [ ] Idioma do perfil coerente com mercado_alvo.

### Modo unificado (adicional)
- [ ] Cargos e datas idÃƒÆ’Ã‚Âªnticos entre CV e LinkedIn.
- [ ] Keywords presentes em ambos os documentos.
- [ ] Sem contradiÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes factuais entre perfil e currÃƒÆ’Ã‚Â­culo.
- [ ] Headline LinkedIn coerente com resumo profissional do CV.

---

## ReferÃƒÆ’Ã‚Âªncias

| Arquivo | ConteÃƒÆ’Ã‚Âºdo |
|---|---|
| `references/diagnostico-ats.md` | Eixos de anÃƒÆ’Ã‚Â¡lise ATS (parsing, aderÃƒÆ’Ã‚Âªncia, eliminatÃƒÆ’Ã‚Â³rios, progressÃƒÆ’Ã‚Â£o) |
| `references/diagnostico-avancado.md` | DiagnÃƒÆ’Ã‚Â³stico avanÃƒÆ’Ã‚Â§ado com vaga definida (PARTES A, B, C) |
| `references/template-saida.md` | Template de entrega final do CV |
| `references/auditoria-linkedin.md` | Regras detalhadas de auditoria LinkedIn por ÃƒÆ’Ã‚Â¡rea, severidades, exemplos por cargo |
| `references/ssi.md` | Guia SSI: pilares, benchmarks por indÃƒÆ’Ã‚Âºstria, tips acionÃƒÆ’Ã‚Â¡veis por faixa |
| `references/presets-formatos.md` | Presets de cargo com headline, skills, vocabulÃƒÆ’Ã‚Â¡rio tÃƒÆ’Ã‚Â©cnico por ÃƒÆ’Ã‚Â¡rea |
