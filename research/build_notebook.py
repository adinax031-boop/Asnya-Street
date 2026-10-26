"""Generate a standalone notebook from the canonical research engine."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
cells = []
def add(kind, source):
    cell = {'cell_type': kind, 'id': f'asnya-{len(cells):02d}', 'metadata': {}, 'source': source.splitlines(keepends=True)}
    if kind == 'code': cell.update(execution_count=None, outputs=[])
    cells.append(cell)
add('markdown', '''# Asnya Research · Hypothesis to evidence
A reproducible daily-price strategy experiment. Synthetic data by default; no market feed.

**Question:** does a simple long/cash trend rule outperform buy-and-hold after costs on untouched chronological test data?

Change parameters, then restart the kernel and run all cells. Repeatedly examining the test split turns it into development data; reserve new data for further claims. Synthetic results establish software behavior, not a profitable edge.
''')
add('code', '''from pathlib import Path
import json, platform
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from IPython.display import display

SEED = 42
CSV_PATH = None  # Optional CSV with date,close, adjusted daily closes in ascending order.
TRAIN_FRACTION = 2 / 3
COST_BPS = 5
CANDIDATES = [(10, 40), (20, 60), (40, 120)]
OUTPUT_DIR = Path('artifacts')
OUTPUT_DIR.mkdir(exist_ok=True)
''')
add('markdown', '''## Engine and execution contract
The following engine is embedded from `asnya_research.py` so this notebook also runs standalone in Colab. Edit the Python source and regenerate the notebook for repository changes.

A signal computed at close t applies to the return t→t+1. Holdings are 100% long or cash. One-way cost in basis points is charged per position change. Each evaluation starts in cash; buy-and-hold pays the same entry cost. Warmup is excluded, cash earns zero, risk-free rate is zero, and annualization assumes 252 daily trading observations. No slippage beyond the configured cost, dividends, leverage, taxes or terminal liquidation cost. Supplied prices should account for corporate actions; the engine does not repair exchange calendars.
''')
add('code', (ROOT/'asnya_research.py').read_text())
add('code', '''data = synthetic_prices(SEED) if CSV_PATH is None else validate_prices(pd.read_csv(CSV_PATH))
if not 0.5 <= TRAIN_FRACTION <= 0.8:
    raise ValueError('Training fraction must be between 0.5 and 0.8')
split = int(len(data) * TRAIN_FRACTION)
DATA_LABEL = 'Seeded synthetic prices' if CSV_PATH is None else 'User-supplied daily CSV'
print(DATA_LABEL, '| rows:', len(data), '| SHA-256:', fingerprint(data))
print('Train through:', data.iloc[split-1]['date'].date(), '| Test starts:', data.iloc[split]['date'].date())
display(data.head())
''')
add('markdown', '''## Select on training data only
All candidates use the same warmup cutoff. Select the highest training Sharpe; ties prefer the smaller windows. This is a demonstration search, not a statistical significance test. Do not select using the held-out table below.
''')
add('code', '''chosen, training_ranking = select_on_training(data, split, CANDIDATES, COST_BPS)
display(training_ranking)
print('Frozen parameters:', chosen)
''')
add('markdown', '''## Evaluate the frozen rule once
The test can use earlier prices to calculate its first signal, but no future prices influence that signal. The position resets to cash at the test boundary, so its first entry incurs a cost. Results are for the test period only.
''')
add('code', '''test_path, test_metrics = backtest(data, **chosen, cost_bps=COST_BPS, start=split)
display(pd.Series(test_metrics, name='held_out_test'))
plt.style.use('dark_background')
fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
axes[0].plot(test_path.date, test_path.equity, color='#c5ee89', label='Frozen strategy, net of costs')
axes[0].plot(test_path.date, test_path.benchmark, color='#91a3a7', linestyle='--', label='Buy & hold, entry cost')
axes[0].set(title='Asnya Research · Held-out equity · ' + DATA_LABEL, ylabel='Equity, start = 100')
axes[0].legend()
axes[1].fill_between(test_path.date, 100 * test_path.drawdown, 0, color='#efa69c', alpha=0.6)
axes[1].set(ylabel='Drawdown %', xlabel='Date')
fig.tight_layout()
fig.savefig(OUTPUT_DIR / 'held_out_equity.png', dpi=150)
plt.show()
''')
add('markdown', '''## Export the evidence
The manifest captures parameters, input hash, split, engine and installed package versions. It does not prove statistical significance. Preserve the original CSV alongside this manifest for real-data reproduction. No automatic external data request is made.
''')
add('code', '''manifest = {
    'engine': ENGINE_VERSION, 'data_label': DATA_LABEL, 'seed': SEED if CSV_PATH is None else None,
    'data_sha256': fingerprint(data), 'rows': len(data), 'split_index': split,
    'train_end': str(data.iloc[split-1]['date'].date()), 'test_start': str(data.iloc[split]['date'].date()),
    'candidates': CANDIDATES, 'selected': chosen, 'cost_bps': COST_BPS,
    'test_metrics': test_metrics,
    'versions': {'python': platform.python_version(), 'numpy': np.__version__, 'pandas': pd.__version__, 'matplotlib': matplotlib.__version__}
}
(OUTPUT_DIR / 'manifest.json').write_text(json.dumps(manifest, indent=2, allow_nan=False))
training_ranking.to_csv(OUTPUT_DIR / 'training_ranking.csv', index=False)
test_path.to_csv(OUTPUT_DIR / 'held_out_returns.csv', index=False)
print('Exported manifest, ranking, returns and chart to', OUTPUT_DIR.resolve())
assert np.isfinite(test_path.equity).all()
assert test_path.date.iloc[1] == data.date.iloc[split]
''')
notebook = {'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.12'}},'cells':cells}
(ROOT/'01_strategy_research.ipynb').write_text(json.dumps(notebook, indent=1)+'\n')
print('Generated 01_strategy_research.ipynb')
