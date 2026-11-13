# biblioteca-anuncios-meta

Uma skill para o Claude Code que descobre **quem está anunciando no Meta** num segmento ou região: quantos anúncios ativos cada empresa tem, há quanto tempo investe e qual criativo está rodando.

A Biblioteca de Anúncios da Meta é o único lugar público onde dá para ver o investimento em mídia da concorrência. Não é estimativa: é o anúncio real, com data de início. O problema é que ela é uma página em JavaScript, e a API oficial só cobre anúncios políticos. Esta skill ensina o Claude a coletar pela própria interface, com o Playwright, e a devolver só o resumo.

## Para que serve

- **Benchmark de concorrência:** "seu concorrente roda 14 anúncios há 8 meses" é o argumento mais concreto que existe num estudo de mercado.
- **Prospecção de clientes de mídia paga:** quem já anuncia já tem verba e já entendeu o canal. Quem anuncia mal, com poucos criativos parados há meses, é o lead ideal.

## Como funciona

1. Monta a URL de busca da biblioteca por palavra-chave ou por anunciante, com país e status.
2. Abre a página no navegador pelo Playwright MCP, sem login e sem chave de API.
3. Roda `scripts/extrair.js` dentro da página, que agrega os anúncios por anunciante e devolve só o resultado: algumas centenas de tokens em vez de dezenas de milhares.

Se você já tiver um snapshot da página salvo em arquivo, `scripts/parse-adlib.py` faz a mesma extração a partir dele.

Saída de exemplo:

```json
{ "nome": "Concorrente A", "anuncios": 5, "desde": "2024-10-22", "url": "..." }
```

## Como instalar

Pré-requisito: o [Playwright MCP](https://github.com/microsoft/playwright-mcp) configurado no Claude Code.

```bash
git clone https://github.com/pedroschell/biblioteca-anuncios-meta ~/.claude/skills/biblioteca-anuncios-meta
```

Pronto. Peça algo como *"quem anuncia clínica odontológica em Porto Alegre no Meta?"* e a skill é acionada.

## Limites

- Mostra **quantos** anúncios e **desde quando**, não quanto cada empresa gasta. Investimento em reais só é público para anúncio político.
- A interface da Meta muda de tempos em tempos. Se a extração voltar vazia, os seletores do `extrair.js` são o primeiro lugar a revisar.

## Licença

MIT
