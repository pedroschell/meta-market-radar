# meta-market-radar

[Português](README.md) | **English**

A Claude Code skill that finds out **who is advertising on Meta** in a given industry or region: how many active ads each company runs, how long it has been investing, and which creative is live.

Meta's Ad Library is the only public place where you can see what competitors put into paid media. It isn't an estimate: it's the actual ad, with its start date. The catch is that it's a JavaScript page, and the official API only covers political ads. This skill teaches Claude to collect the data through the page itself, using Playwright, and to return only the summary.

## What it's for

- **Competitor benchmarking:** "your competitor has been running 14 ads for 8 months" is about as concrete as an argument gets in a market study.
- **Prospecting paid media clients:** whoever already advertises already has a budget and already understands the channel. A company advertising poorly, with a few creatives left untouched for months, is the ideal lead.

## How it works

1. Builds the library's search URL by keyword or by advertiser, with country and status.
2. Opens the page in the browser through Playwright MCP, with no login and no API key.
3. Runs `scripts/extrair.js` inside the page, which groups the ads by advertiser and returns only the result: a few hundred tokens instead of tens of thousands.

If you already have a snapshot of the page saved to a file, `scripts/parse-adlib.py` does the same extraction from it.

Sample output:

```json
{ "nome": "Concorrente A", "anuncios": 5, "desde": "2024-10-22", "url": "..." }
```

The output keys are in Portuguese: `nome` is the advertiser's name, `anuncios` the number of active ads, and `desde` the date of the oldest one still running.

## Installation

Prerequisite: [Playwright MCP](https://github.com/microsoft/playwright-mcp) set up in Claude Code.

```bash
git clone https://github.com/pedroschell/meta-market-radar ~/.claude/skills/meta-market-radar
```

That's it. Ask something like *"who advertises dental clinics in Porto Alegre on Meta?"* and the skill kicks in.

## Limits

- It shows **how many** ads and **since when**, not how much each company spends. Spend in reais is only public for political ads.
- Meta's interface changes from time to time. If the extraction comes back empty, the selectors in `extrair.js` are the first place to check.

## License

MIT
