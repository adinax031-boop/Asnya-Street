# Asnya Street
An open quantitative research workbench. Browser-local, dependency-free research engine with seeded synthetic scenarios, daily-price CSV import, long/cash trend and mean-reversion strategies, net-cost backtests, equity and drawdown charts, local experiment ledger and CSV exports.

Serve `dist/` using any static web server. Run `node test.cjs` for engine checks. Read the in-app Methodology for all execution and annualization assumptions. No live market feeds or broker integration. Imported files stay in browser storage. This first release is a research prototype; it does not establish profitable strategies.

## Files
- `dist/engine.js`: deterministic data, validation and backtest engine
- `dist/app.js`: UI, charts, storage and exports
- `dist/index.html`: responsive interface

## License
MIT — Copyright (c) 2026 Asnya Street contributors. Permission is granted, free of charge, to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software, provided this notice is retained. THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM OR DAMAGES ARISING FROM THE SOFTWARE OR ITS USE.
