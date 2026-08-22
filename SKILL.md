---
name: biblioteca-anuncios-meta
description: Use para descobrir quem está anunciando no Meta em um segmento ou região — quantos anúncios ativos, há quanto tempo cada concorrente investe e qual criativo está rodando. Serve para benchmark de concorrência em estudo de mercado e para encontrar leads de mídia paga (quem já anuncia é quem já compra). Aciona quando o pedido envolver: biblioteca de anúncios, ad library, quem anuncia, concorrente anunciando, há quanto tempo investe, prospecção de clientes de tráfego.
---

# Biblioteca de Anúncios da Meta

## Por que essa fonte vale mais que as outras

É o único lugar público onde se vê **investimento em mídia da concorrência**. Não é estimativa: é o anúncio real, com data de início.

Dois usos, mesma coleta:

- **No estudo:** "seu concorrente roda 14 anúncios há 8 meses" é o argumento mais concreto que existe num benchmark.
- **Na prospecção:** quem já anuncia é quem já tem verba e já entendeu o canal. Quem anuncia **mal** (2 criativos, parados há meses) é o lead ideal.

## Como acessar

**A API oficial da Meta não serve.** Ela cobre apenas anúncios políticos e de temas sociais. Para anúncios comerciais, só a interface web — que é uma SPA em JavaScript, então `WebFetch` e `curl` retornam página vazia. **Use o Playwright MCP.**

Sem login, sem chave de API.

### 1. Navegar

```
mcp__playwright__browser_navigate com a URL montada:

https://www.facebook.com/ads/library/
  ?active_status=active        # active | inactive | all
  &ad_type=all
  &country=BR
  &q=TERMO%20DE%20BUSCA
  &search_type=keyword_unordered
  &media_type=all
```

Para buscar por anunciante específico em vez de palavra-chave, troque
`search_type=keyword_unordered` por `search_type=page` e use `view_all_page_id=<id>`.

### 2. Extrair dentro da página

**Nunca use `browser_snapshot` aqui.** O snapshot passa de 90 mil caracteres: estoura o contexto se voltar inline, e com `filename` despeja um arquivo de 100 KB na raiz do repositório. Testado, e é lixo nos dois casos.

Use `mcp__playwright__browser_evaluate` com o conteúdo de `scripts/extrair.js`. O código roda dentro da página, agrega ali e devolve só o resultado:

```json
{
  "total": "~140 resultados",
  "cards_lidos": 29,
  "anunciantes": [
    { "nome": "Concorrente A", "anuncios": 5, "desde": "2024-10-22", "url": "..." }
  ]
}
```

Custo: algumas centenas de tokens em vez de ~25 mil, sem arquivo intermediário.

O `scripts/parse-adlib.py` continua no repositório como alternativa para quando já existir um snapshot salvo — mas não é o caminho padrão.

## Limite importante

A página carrega por rolagem. Um snapshot direto pega **~27 anúncios**, não os 10 mil que o contador mostra. Para uma amostra maior, role antes de capturar (`browser_evaluate` com `window.scrollTo`) e capture de novo.

Para benchmark de concorrência isso raramente importa — os anunciantes relevantes de uma região aparecem nos primeiros resultados. Para mapear um mercado inteiro, role.

## Como ler o resultado

| Sinal | Leitura |
|---|---|
| Muitos anúncios, data antiga | Concorrente maduro, investe com constância. Difícil de bater no lance. |
| Poucos anúncios, data antiga | Rodando no automático, criativo cansado. Vulnerável. |
| Muitos anúncios, data recente | Entrou agora com verba. Vale monitorar. |
| Não aparece | Não anuncia. É lead, ou é concorrente que vive de indicação. |

A **data de início do mais antigo** é o número mais útil: separa quem testa de quem opera.

## Refinar por região

A busca é nacional por padrão. Para recortar praça, combine o termo com a cidade
(`proteção veicular Torres`) e cruze com o resultado nacional — anunciante que aparece
nas duas buscas atua na região; o que só aparece na nacional é player grande sem foco local.

## Checklist

- [ ] Snapshot salvo em arquivo, não trazido inline
- [ ] Parser rodado, saída conferida
- [ ] Buscas nacional e regional comparadas
- [ ] Anunciantes ausentes anotados — são leads ou concorrentes de indicação
- [ ] Datas de início citadas no relatório (é o dado que sustenta o argumento)
