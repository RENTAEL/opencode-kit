---
name: padrao-lucas
description: "Aplica e fiscaliza o guia de boas prÃƒÆ’Ã‚Â¡ticas multi-linguagem (sÃƒÆ’Ã‚Â­ntese de Clean Code, Clean Architecture e obras O'Reilly). Postura: **gate proporcional** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â violaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de DEVE/NÃƒÆ’Ã†â€™O DEVE no caminho tocado ÃƒÆ’Ã‚Â© bloqueadora. Em c..."
---
# padrÃƒÆ’Ã‚Â£o-lucas

## VisÃƒÆ’Ã‚Â£o geral

Aplica e fiscaliza o guia de boas prÃƒÆ’Ã‚Â¡ticas multi-linguagem (sÃƒÆ’Ã‚Â­ntese de Clean
Code, Clean Architecture e obras O'Reilly). Postura: **gate proporcional** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
violaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de DEVE/NÃƒÆ’Ã†â€™O DEVE no caminho tocado ÃƒÆ’Ã‚Â© bloqueadora. Em cÃƒÆ’Ã‚Â³digo novo que
vocÃƒÆ’Ã‚Âª escreve: corrija antes de entregar; reportar sozinho nÃƒÆ’Ã‚Â£o basta. Em cÃƒÆ’Ã‚Â³digo
legado fora do escopo autorizado: registre pendÃƒÆ’Ã‚Âªncia com impacto. PREFIRA ÃƒÆ’Ã‚Â©
recomendaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o contextual, nunca bloqueio.

## Fonte do guia (use a primeira que existir)

1. Guia indicado pelo AGENTS.md/CLAUDE.md do projeto.
2. `llms.txt`/`llms-full.txt` na raiz do projeto.
3. CÃƒÆ’Ã‚Â³pia embutida: `references/llms-full.txt` desta skill (pin da v1.0.1;
   atualize o pin quando o guia-fonte mudar de versÃƒÆ’Ã‚Â£o).

## Escolha do modo ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â dimensione por RISCO, nÃƒÆ’Ã‚Â£o por tamanho

- **Inline**: mudanÃƒÆ’Ã‚Â§a rotineira E de risco baixo (sem dinheiro, autenticaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o,
  dados pessoais, concorrÃƒÆ’Ã‚Âªncia, migraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o ou contrato pÃƒÆ’Ã‚Âºblico).
- **OrquestraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o**: mudanÃƒÆ’Ã‚Â§a ampla, pedido explÃƒÆ’Ã‚Â­cito de revisÃƒÆ’Ã‚Â£o, OU risco alto
  mesmo pequena (pagamentos, senhas, SQL, transaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes). VocÃƒÆ’Ã‚Âª ÃƒÆ’Ã‚Â© o coordenador e
  despacha subagentes de revisÃƒÆ’Ã‚Â£o em paralelo.

## Modo inline

1. Leia do guia: seÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes 00, 02, 03, a seÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o tÃƒÆ’Ã‚Â©cnica pertinente e 22.
2. Implemente sem reproduzir no cÃƒÆ’Ã‚Â³digo novo violaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes que existam no arquivo
   (veja a tabela de desculpas).
3. Entregue no formato 23.1: Resultado, DecisÃƒÆ’Ã‚Âµes, ValidaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o, LimitaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes,
   Compatibilidade.

## Modo orquestraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o

1. Identifique arquivos/diff e as dimensÃƒÆ’Ã‚Âµes de risco presentes. Menu:
   contratos/erros (seÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes 04, 09), seguranÃƒÆ’Ã‚Â§a (13), concorrÃƒÆ’Ã‚Âªncia/persistÃƒÆ’Ã‚Âªncia
   (10, 11), testes/validaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o (14), arquitetura/nomes (05, 07, 08). Despache
   apenas as dimensÃƒÆ’Ã‚Âµes realmente presentes.
2. Um subagente por dimensÃƒÆ’Ã‚Â£o, em paralelo. O subagente NÃƒÆ’Ã†â€™O tem esta skill: cole
   no prompt dele (a) os arquivos ou diff, (b) as seÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes do guia daquela
   dimensÃƒÆ’Ã‚Â£o, (c) o contrato de saÃƒÆ’Ã‚Â­da abaixo.
3. Contrato de saÃƒÆ’Ã‚Â­da de cada subagente ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â um bloco por achado, campos na ordem:
   Achado / Severidade (bloqueador | relevante | sugestÃƒÆ’Ã‚Â£o, critÃƒÆ’Ã‚Â©rios da seÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o
   22.3) / Local (arquivo:linha) / CenÃƒÆ’Ã‚Â¡rio que reproduz ou evidencia / Impacto /
   CorreÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o sugerida / Incerteza ou validaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o pendente. Sem achados relevantes,
   declare isso; nÃƒÆ’Ã‚Â£o invente APIs, resultados ou execuÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes (CORE-03, CORE-12).
4. Como coordenador: verifique cada bloqueador lendo o local citado; descarte os
   nÃƒÆ’Ã‚Â£o sustentados; deduza repetidos; corrija os vÃƒÆ’Ã‚Â¡lidos no cÃƒÆ’Ã‚Â³digo ou registre
   como pendÃƒÆ’Ã‚Âªncia com justificativa e impacto.
5. Entregue no formato 23.1 + achados agrupados por severidade.

Se o ambiente bloquear o despacho de subagentes (vocÃƒÆ’Ã‚Âª ÃƒÆ’Ã‚Â© um agente-folha),
execute a revisÃƒÆ’Ã‚Â£o multidimensional inline usando o mesmo contrato de saÃƒÆ’Ã‚Â­da e
reporte o desvio na entrega.

## Desculpas que nÃƒÆ’Ã‚Â£o valem (observadas no baseline sem skill)

| Pensamento | Realidade |
| --- | --- |
| "O arquivo jÃƒÆ’Ã‚Â¡ usa esse estilo; sÃƒÆ’Ã‚Â³ segui o padrÃƒÆ’Ã‚Â£o local" | Copiar violaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o DEVE/NÃƒÆ’Ã†â€™O DEVE cria um defeito novo; nÃƒÆ’Ã‚Â£o ÃƒÆ’Ã‚Â© refatoraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o. |
| "Pediram pressa / para nÃƒÆ’Ã‚Â£o refatorar" | O gate exige corrigir ou reportar o bloqueador, nÃƒÆ’Ã‚Â£o refatorar tudo; no trecho tocado custa quase nada. |
| "ÃƒÆ’Ã¢â‚¬Â° sÃƒÆ’Ã‚Â³ uma funÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o pequena" | Risco decide: reembolso, senha e SQL sÃƒÆ’Ã‚Â£o crÃƒÆ’Ã‚Â­ticos em qualquer tamanho. |
| "JÃƒÆ’Ã‚Â¡ avisei numa nota de rodapÃƒÆ’Ã‚Â©" | Em cÃƒÆ’Ã‚Â³digo novo, avisar nÃƒÆ’Ã‚Â£o basta: corrija. Em cÃƒÆ’Ã‚Â³digo legado fora do escopo, registre a pendÃƒÆ’Ã‚Âªncia com impacto. |
| "A instruÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o do usuÃƒÆ’Ã‚Â¡rio prevalece sobre o guia" | InstruÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o do usuÃƒÆ’Ã‚Â¡rio define escopo, nÃƒÆ’Ã‚Â£o licencia defeito novo: nÃƒÆ’Ã‚Â£o refatorar tudo nÃƒÆ’Ã‚Â£o ÃƒÆ’Ã‚Â© autorizaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o para escrever concatenaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de SQL ou catch engolido no trecho novo. |
| "NÃƒÆ’Ã‚Â£o dÃƒÆ’Ã‚Â¡ para testar aqui" | Reporte em LimitaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes (23.1) o que nÃƒÆ’Ã‚Â£o foi executado; nunca omita nem invente. |

## Red flags ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â pare e reavalie

- Catch que devolve flag de sucesso indistinguÃƒÆ’Ã‚Â­vel de falha.
- SQL, comando ou caminho montado por concatenaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de entrada.
- Efeito parcial sem anÃƒÆ’Ã‚Â¡lise (por exemplo: update + pagamento + e-mail numa
  sequÃƒÆ’Ã‚Âªncia que pode falhar no meio).
- Resumo de entrega sem LimitaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes quando nada foi executado.
- CÃƒÆ’Ã‚Â³digo novo entregue com bloqueador conhecido "porque o arquivo jÃƒÆ’Ã‚Â¡ era assim".
