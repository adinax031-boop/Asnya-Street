"""Daily long/cash research baseline. No live data or broker execution."""
import hashlib
import numpy as np
import pandas as pd

ENGINE_VERSION = 'research-0.1'

def validate_prices(frame):
    if not {'date', 'close'}.issubset(frame.columns):
        raise ValueError('Expected date,close columns')
    data = frame[['date', 'close']].copy()
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d', errors='raise')
    data['close'] = pd.to_numeric(data['close'], errors='raise')
    if len(data) < 260 or len(data) > 20000:
        raise ValueError('Expected 260–20,000 daily observations')
    if data.isna().any().any() or not np.isfinite(data['close']).all() or (data['close'] <= 0).any():
        raise ValueError('Prices must be finite and positive; no missing values')
    if data['date'].duplicated().any() or not data['date'].is_monotonic_increasing:
        raise ValueError('Dates must be unique and ascending')
    return data.reset_index(drop=True)

def synthetic_prices(seed=42, observations=756):
    rng = np.random.default_rng(seed)
    returns = rng.normal(0.0004, 0.012, observations)
    return validate_prices(pd.DataFrame({'date': pd.bdate_range('2023-01-02', periods=observations),
                                        'close': 100 * np.exp(np.cumsum(returns))}))

def fingerprint(data):
    return hashlib.sha256(data.to_csv(index=False, date_format='%Y-%m-%d').encode()).hexdigest()

def backtest(data, fast=20, slow=60, cost_bps=5, start=None):
    data = validate_prices(data)
    if not isinstance(fast, int) or not isinstance(slow, int) or not 2 <= fast < slow <= 250:
        raise ValueError('Require integer windows: 2 <= fast < slow <= 250')
    if not np.isfinite(cost_bps) or not 0 <= cost_bps <= 200:
        raise ValueError('Cost must be 0–200 bps')
    start = slow if start is None else start
    if not isinstance(start, int) or not slow <= start < len(data) - 1:
        raise ValueError('Invalid evaluation start')
    close = data['close']
    signal = (close.rolling(fast).mean() > close.rolling(slow).mean()).astype(float)
    # Signal at previous close determines exposure to today's close-to-close return.
    position = signal.shift(1).fillna(0).iloc[start:].copy()
    turnover = position.diff().abs()
    turnover.iloc[0] = position.iloc[0]  # Evaluation starts in cash, including held-out test.
    returns = close.pct_change().iloc[start:]
    net = position * returns - turnover * cost_bps / 10000
    benchmark = returns.copy()
    benchmark.iloc[0] -= cost_bps / 10000
    equity = np.r_[100., 100 * (1 + net).cumprod().to_numpy()]
    benchmark_equity = np.r_[100., 100 * (1 + benchmark).cumprod().to_numpy()]
    out = data.iloc[start-1:].copy().reset_index(drop=True)
    out['position'] = np.r_[0., position.to_numpy()]
    out['return'] = np.r_[0., net.to_numpy()]
    out['equity'] = equity
    out['benchmark'] = benchmark_equity
    out['drawdown'] = equity / np.maximum.accumulate(equity) - 1
    sd = float(net.std(ddof=1))
    metrics = {'total_return': float(equity[-1]/100-1),
               'annualized_return': float((equity[-1]/100)**(252/len(net))-1),
               'sharpe': float(net.mean()/sd*np.sqrt(252)) if sd > 0 else 0.,
               'max_drawdown': float(out['drawdown'].min()),
               'position_changes': int(turnover.sum()), 'evaluated_returns': len(net)}
    return out, metrics

def select_on_training(data, split, candidates, cost_bps=5):
    """Reads only rows before split. Shared warmup makes candidates comparable."""
    if not isinstance(split, int) or not 260 <= split <= len(data)-60:
        raise ValueError('Need >=260 training rows and >=60 test rows')
    train = data.iloc[:split].copy()
    common_start = max(slow for _, slow in candidates)
    records = []
    for fast, slow in candidates:
        _, metrics = backtest(train, fast, slow, cost_bps, start=common_start)
        records.append({'fast': fast, 'slow': slow, **metrics})
    ranking = pd.DataFrame(records).sort_values(['sharpe', 'fast', 'slow'], ascending=[False, True, True]).reset_index(drop=True)
    winner = ranking.iloc[0]
    return {'fast': int(winner['fast']), 'slow': int(winner['slow'])}, ranking
