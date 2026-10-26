# Contributing
Requires Node 22+. No dependencies or install step.

Edit `src/index.html`, `src/engine.js`, and `src/app.js`. Run `npm test` and `npm run build`. Commit source and generated `dist/` together: CI rejects drift. Run `npm run dev` and open the printed URL to verify changes. Restart after edits; no hot reload. Check keyboard navigation and the command menu. Describe behavior and validation in each pull request. Financial-method changes need deterministic examples and no-future-price-leakage checks.

`npm start` serves an existing build. The server binds to loopback and serves only application assets; it is for development. Production hosting serves `dist/` statically. No broker credentials, market feeds, or backend services are configured by this infrastructure.
