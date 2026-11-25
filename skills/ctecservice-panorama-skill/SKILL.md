---
name: ctecservice-panorama-skill
description: "Manter um arquivo ÃƒÆ’Ã‚Âºnico ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `panorama-atual.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â que responde em segundos: como estÃƒÆ’Ã‚Â¡ o projeto, o que jÃƒÆ’Ã‚Â¡ foi feito, o que falta fazer e quais decisÃƒÆ’Ã‚Âµes vigentes o moldam."
---
# Panorama ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â estado atual do projeto

## Objetivo

Manter um arquivo ÃƒÆ’Ã‚Âºnico ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `panorama-atual.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â que responde em segundos: como estÃƒÆ’Ã‚Â¡ o projeto, o que jÃƒÆ’Ã‚Â¡ foi feito, o que falta fazer e quais decisÃƒÆ’Ã‚Âµes vigentes o moldam.

## Quando usar

- O usuÃƒÆ’Ã‚Â¡rio pede "panorama", "status das implementaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes", "como estÃƒÆ’Ã‚Â¡ o projeto", "o que falta".
- VocÃƒÆ’Ã‚Âª comeÃƒÆ’Ã‚Â§a a trabalhar num projeto que nÃƒÆ’Ã‚Â£o tem o arquivo ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ gerar do zero.
- VocÃƒÆ’Ã‚Âª concluiu uma implementaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o, correÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o ou decisÃƒÆ’Ã‚Â£o relevante ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ atualizar no mesmo commit (ver "Workflow de atualizaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o").
- O `AGENTS.md` do projeto exige manter o panorama atualizado (padrÃƒÆ’Ã‚Â£o recomendado).

## O arquivo (estrutura obrigatÃƒÆ’Ã‚Â³ria)

Ordem fixa das seÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use o template `templates/panorama-atual.template.md`:

1. **CabeÃƒÆ’Ã‚Â§alho** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â regra de manutenÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o + "ÃƒÆ’Ã…Â¡ltima atualizaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o" com data real.
2. **DecisÃƒÆ’Ã‚Âµes vigentes** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â decisÃƒÆ’Ã‚Âµes que moldam o projeto (ex.: "sem repo git prÃƒÆ’Ã‚Â³prio por enquanto").
3. **Fase atual** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â versÃƒÆ’Ã‚Â£o/fase em vigor + 1-2 linhas de resumo; prÃƒÆ’Ã‚Â³xima fase com escopo resumido.
4. **Implementado** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â por ÃƒÆ’Ã‚Â¡rea: tabela de mÃƒÆ’Ã‚Â³dulos (arquivo ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ responsabilidade em 1 linha), testes com contagem real, CI.
5. **Pendente (roadmap)** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â tabela fase ÃƒÆ’Ã¢â‚¬â€ status (NÃƒÆ’Ã‚Â£o iniciada / Parcial / ConcluÃƒÆ’Ã‚Â­da) com observaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o do que falta.
6. **Como manter este arquivo** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â instruÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes curtas.

## Local e nome do arquivo

- **PadrÃƒÆ’Ã‚Â£o:** `panorama-atual.md` na **raiz do workspace** (pasta do projeto).
- **ExceÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o:** se o `AGENTS.md` do projeto definir outro caminho/nome (ex.: `docs/panorama-atual.md`), use exatamente o que estiver definido lÃƒÆ’Ã‚Â¡ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â o `AGENTS.md` tem precedÃƒÆ’Ã‚Âªncia.

## Workflow ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â gerar do zero

1. **Contexto do projeto**: leia o `AGENTS.md` (se existir) e os docs de plano/roadmap. Se o projeto tiver mais de uma fonte de plano, leia as duas.
2. **Coleta em paralelo** (use background/subagentes quando disponÃƒÆ’Ã‚Â­veis ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â nunca faÃƒÆ’Ã‚Â§a buscas sequenciais desnecessÃƒÆ’Ã‚Â¡rias):
   - ExploraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o do cÃƒÆ’Ã‚Â³digo: liste os mÃƒÆ’Ã‚Â³dulos/arquivos principais e a responsabilidade de cada um (1 linha); testes e o que cobrem; CI/workflows e scripts do `package.json`.
   - Leitura dos docs de plano: fases/milestones e critÃƒÆ’Ã‚Â©rios de saÃƒÆ’Ã‚Â­da.
3. **Cruzamento**: marque cada fase do roadmap como concluÃƒÆ’Ã‚Â­da/parcial/nÃƒÆ’Ã‚Â£o iniciada **com base no cÃƒÆ’Ã‚Â³digo**, nÃƒÆ’Ã‚Â£o no plano.
4. **Escrita**: gere o arquivo no local definido (padrÃƒÆ’Ã‚Â£o: `panorama-atual.md` na raiz do workspace; se o `AGENTS.md` definir outro caminho/nome, use o definido) seguindo o template, apenas com fatos verificados.
5. **Regra no AGENTS.md**: se o projeto nÃƒÆ’Ã‚Â£o tiver a regra de manutenÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o, adicione ao `AGENTS.md` do projeto (seÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de fluxo de trabalho):
   > `panorama-atual.md` ÃƒÆ’Ã‚Â© o arquivo-base de status: toda implementaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o, correÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o ou decisÃƒÆ’Ã‚Â£o relevante deve atualizÃƒÆ’Ã‚Â¡-lo no mesmo commit, usando a skill `panorama`.
   - Se o usuÃƒÆ’Ã‚Â¡rio quiser o arquivo em outro lugar ou com outro nome, ele deve deixar isso **explÃƒÆ’Ã‚Â­cito no `AGENTS.md`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a skill segue o caminho definido lÃƒÆ’Ã‚Â¡.

## Workflow ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â atualizar

- MudanÃƒÆ’Ã‚Â§as pequenas (1-2 mÃƒÆ’Ã‚Â³dulos, contagem de testes, decisÃƒÆ’Ã‚Â£o nova): edite apenas as seÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes afetadas + "ÃƒÆ’Ã…Â¡ltima atualizaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o".
- MudanÃƒÆ’Ã‚Â§as grandes (nova fase concluÃƒÆ’Ã‚Â­da, refatoraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o ampla): refaÃƒÆ’Ã‚Â§a o levantamento do cÃƒÆ’Ã‚Â³digo em vez de editar de memÃƒÆ’Ã‚Â³ria.
- Atualize no **mesmo commit** da mudanÃƒÆ’Ã‚Â§a que o gerou.

## Regras obrigatÃƒÆ’Ã‚Â³rias

- **Apenas fatos verificados**: nunca invente mÃƒÆ’Ã‚Â³dulos, nÃƒÆ’Ã‚Âºmeros de testes ou status; na dÃƒÆ’Ã‚Âºvida, leia o cÃƒÆ’Ã‚Â³digo ou rode o runner de testes para obter a contagem real.
- **Encoding**: UTF-8 sem BOM; apÃƒÆ’Ã‚Â³s gravar, verifique se acentos e caracteres especiais estÃƒÆ’Ã‚Â£o intactos.
- **Idioma**: o idioma do projeto (padrÃƒÆ’Ã‚Â£o: portuguÃƒÆ’Ã‚Âªs do Brasil). Nomes tÃƒÆ’Ã‚Â©cnicos (variÃƒÆ’Ã‚Â¡veis, mÃƒÆ’Ã‚Â³dulos, ferramentas) permanecem como estÃƒÆ’Ã‚Â£o.
- **Data real** em "ÃƒÆ’Ã…Â¡ltima atualizaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o" (formato DD/MM/AAAA).
- **NÃƒÆ’Ã‚Â£o substitui os docs de plano**: o panorama ÃƒÆ’Ã‚Â© o resumo do estado real; detalhes continuam no roadmap/plano ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â link para eles quando fizer sentido.
- Se o projeto jÃƒÆ’Ã‚Â¡ tiver o arquivo de panorama em outro idioma/formato/caminho, respeite o existente e o registrado no `AGENTS.md`.

## Coleta eficiente

- Paralelize: exploraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de cÃƒÆ’Ã‚Â³digo e leitura de docs ao mesmo tempo.
- Use subagentes de exploraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o (ex.: explorer no opencode) para mapear o cÃƒÆ’Ã‚Â³digo e manter seu contexto limpo.
- PeÃƒÆ’Ã‚Â§a contagens reais (testes, arquivos) por terminal (ex.: `node --test`) em vez de estimar.
