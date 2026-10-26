# Asnya Research

A real Jupyter/Python workspace alongside the browser terminal. It does not run a remote Python kernel inside the hosted static site.

[Open notebook on GitHub](https://github.com/adinax031-boop/Asnya-Street/blob/main/research/01_strategy_research.ipynb) · [Open in Colab](https://colab.research.google.com/github/adinax031-boop/Asnya-Street/blob/main/research/01_strategy_research.ipynb)

## Run locally (Python 3.12)
From the repository root:

```sh
python -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install -r research/requirements.txt
jupyter lab research/01_strategy_research.ipynb
```

Restart the kernel and run all cells. The default seeded synthetic experiment needs no downloaded market data. Colab can run the notebook standalone using its supplied numpy/pandas/matplotlib; its package versions are recorded and may differ from local pins. For a supplied CSV, upload it to the notebook environment and set `CSV_PATH` in the first code cell. Requirements: date,close headers; unique ascending daily dates; positive adjusted closes; 260–20,000 observations. The split needs >=260 training observations and >=60 test observations, so at least 390 rows at the default 2/3 split.

## What it does
- Seeded synthetic prices or supplied CSV, with a SHA-256 input fingerprint.
- Three moving-average candidates, evaluated on the same training window.
- Chronological holdout with frozen parameters and next-period signal execution.
- One-way transaction costs; buy-and-hold comparison; equity and drawdown plots.
- CSV returns and ranking, PNG chart, and JSON reproducibility manifest.

No live feed, paper trading, recommendations, or statistical-significance claims. Historical results depend on data quality, calendar frequency and omitted costs. Repeated use of the same holdout contaminates it. Synthetic returns are not market evidence. The Python example is a separate documented baseline; its numpy-generated synthetic series is not the JavaScript terminal's LCG series.

## Automated verification
```sh
python research/test_research.py
python research/build_notebook.py
python research/execute_notebook.py /tmp/asnya-notebook-run
```
The runner validates schema, executes all cells in a fresh kernel with a 120-second per-cell timeout and fails on errors. It writes the executed notebook and evidence under the output directory; it never rewrites the clean source notebook. Edit `asnya_research.py` or `build_notebook.py`, regenerate and commit `01_strategy_research.ipynb`. CI checks that regeneration produces no notebook drift and executes the full notebook. Dependencies pin top-level packages; the manifest records installed analysis-library versions. This is not a fully locked transitive environment.

Official workflow references: https://jupyter.org/install and https://nbclient.readthedocs.io/en/latest/client.html
