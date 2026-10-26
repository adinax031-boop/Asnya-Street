# Asnya Street
An open quantitative research workbench. Browser-local, dependency-free research engine with seeded synthetic scenarios, daily-price CSV import, long/cash trend and mean-reversion strategies, net-cost backtests, equity and drawdown charts, local experiment ledger and CSV exports.

Serve `dist/` using any static web server. Run `node test.cjs` for engine checks. Read the in-app Methodology for all execution and annualization assumptions. No live market feeds or broker integration. Imported files stay in browser storage. This first release is a research prototype; it does not establish profitable strategies.

## Files
- `dist/engine.js`: deterministic data, validation and backtest engine
- `dist/app.js`: UI, charts, storage and exports
- `dist/index.html`: responsive interface

## License
MIT — Copyright (c) 2026 Asnya Street contributors. Permission is granted, free of charge, to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software, provided this notice is retained. THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM OR DAMAGES ARISING FROM THE SOFTWARE OR ITS USE.

## Development infrastructure
Requires Node 22+. No dependencies or install step. Run `npm test`, `npm run build`, then `npm run dev`. Edit `src/` and commit generated `dist/` with source. GitHub Actions checks Node 22/24, engine behavior, build reproducibility, HTTP serving and generated-asset drift. See CONTRIBUTING.md. This does not add backend services, live data or brokerage connections.

## Financial Core: Portfolio desk
Add and edit long holdings (quantity, average cost, manually entered current price) and cash in USD. Inspect value, unrealized P&L, allocation and largest-position concentration. Run all-holdings or single-holding price shocks; cash remains unchanged. Import/export validated version-1 JSON; browser-local persistence. A fictional example is provided. No market data feed is connected; there is no transaction history, FX conversion, fees, taxes, or cash-flow-adjusted return calculation. Stress tests are deterministic scenarios, not probability or liquidity estimates.

## Asnya Research · Jupyter workspace

[Open research notebook](research/01_strategy_research.ipynb) · [Run in Colab](https://colab.research.google.com/github/adinax031-boop/Asnya-Street/blob/main/research/01_strategy_research.ipynb)

A standalone Python notebook with supplied CSV or seeded synthetic prices, training-only parameter selection, frozen chronological holdout, transaction costs, charts and exported evidence. See [research setup](research/README.md) for JupyterLab installation and automated execution. This runs in a Python kernel alongside the browser terminal; the static hosted site does not provide remote kernels.

