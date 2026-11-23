"""Energy satellite sleeve - portfolio engine (Python standard library only).

Decision this engine supports: should the investment committee adopt, pilot, or reject
a five-ETF energy sleeve (XLE, XOP, AMLP, ICLN, NLR) built as the lowest-volatility,
long-only mix that meets the mandate below?

All math lives here. analysis.py, changed_input.py and app.py import these functions;
none of them re-implements the calculations.

Origin: extends the Lab 14/15 engine (covariance, grid search, price estimation).
New in Project 2: the single-fund cap is enforced inside the search, plus backtest,
drawdown, turnover and cost functions.
"""
from __future__ import annotations

import csv
import io
import math

# ---------------------------------------------------------------------------
# Mandate (working assumptions - see docs/validation-and-ai-use.md, section 2)
# ---------------------------------------------------------------------------
OBJECTIVE_RETURN = 0.08    # minimum expected annual return (arithmetic, decimal)
MAX_WEIGHT = 0.40          # hard cap: no single fund above 40%
STEP = 0.05                # search grid: every long-only mix in 5-point steps
REBALANCE_MONTHS = 12      # annual rebalancing back to target weights
COST_BPS = 10              # assumed one-way trading cost, basis points of value traded

TOLERANCE = 1e-9


# ---------------------------------------------------------------------------
# Data: read monthly prices and turn them into returns
# ---------------------------------------------------------------------------
def read_prices(source):
    """Read a prices CSV: Date first, oldest first, one column per ticker.

    `source` is a path or an open/uploaded file (text or bytes).
    Returns (tickers, dates, prices) where prices[i][j] is ticker j at date i.
    Refuses bad files with a clear ValueError instead of guessing.
    """
    if isinstance(source, str):
        with open(source, newline="") as handle:
            text = handle.read()
    else:
        raw = source.read()
        text = raw.decode("utf-8-sig") if isinstance(raw, bytes) else raw
    rows = [row for row in csv.reader(io.StringIO(text)) if row]
    if len(rows) < 4:
        raise ValueError("Need a header row and at least three months of prices.")
    tickers = [t.strip() for t in rows[0][1:]]
    if len(set(tickers)) != len(tickers):
        raise ValueError("Duplicate ticker columns.")
    dates, prices = [], []
    for row in rows[1:]:
        if len(row) != len(tickers) + 1:
            raise ValueError(f"Row {row[0]} has {len(row) - 1} prices; expected {len(tickers)}.")
        values = [float(x) for x in row[1:]]
        if any(not math.isfinite(v) or v <= 0 for v in values):
            raise ValueError(f"Row {row[0]} has a missing, zero or negative price.")
        dates.append(row[0].strip())
        prices.append(values)
    if dates != sorted(dates) or len(set(dates)) != len(dates):
        raise ValueError("Dates must run oldest first with no repeats.")
    return tickers, dates, prices


def monthly_returns(prices):
    """Simple return each month: price / previous price - 1."""
    return [[now / before - 1 for now, before in zip(prices[i], prices[i - 1])]
            for i in range(1, len(prices))]


def _mean(xs):
    return sum(xs) / len(xs)


def _stdev(xs):
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def _correlation(xs, ys):
    mx, my = _mean(xs), _mean(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))


def estimate(returns):
    """Annualized estimates from a list of monthly return rows.

    Return estimate = arithmetic monthly mean x 12; volatility = monthly sample
    standard deviation x sqrt(12); plus the correlation table. These are historical
    averages, not forecasts.
    """
    if len(returns) < 12:
        raise ValueError(f"Only {len(returns)} monthly returns; at least 12 needed.")
    columns = list(zip(*returns))
    n = len(columns)
    if any(_stdev(c) == 0 for c in columns):
        raise ValueError("A fund has zero volatility in this window; correlation is undefined.")
    corr =[[1.0 if i == j else _correlation(columns[i], columns[j]) for j in range(n)]
            for i in range(n)]
    return {
        "returns": [_mean(c) * 12 for c in columns],
        "volatilities": [_stdev(c) * math.sqrt(12) for c in columns],
        "correlation": corr,
        "months": len(returns),
    }


def estimate_from_prices(source, last_n=None):
    """Read prices and estimate on all months, or only the last `last_n` returns."""
    tickers, dates, prices = read_prices(source)
    returns = monthly_returns(prices)
    return_dates = dates[1:]
    if last_n is not None:
        if len(returns) < last_n:
            raise ValueError(f"Only {len(returns)} monthly returns; {last_n} needed.")
        returns, return_dates = returns[-last_n:], return_dates[-last_n:]
    out = estimate(returns)
    out.update({"names": tickers, "first_return_month": return_dates[0],
                "last_return_month": return_dates[-1]})
    return out


# ---------------------------------------------------------------------------
# Risk and return of a mix
# ---------------------------------------------------------------------------
def validate_correlation(corr, n):
    """Raise ValueError if the correlation table is the wrong size, out of range or asymmetric."""
    if len(corr) != n or any(len(row) != n for row in corr):
        raise ValueError(f"Correlation table must be {n} x {n}.")
    for i in range(n):
        if abs(corr[i][i] - 1) > 1e-6:
            raise ValueError(f"Correlation diagonal [{i}][{i}] must be 1.")
        for j in range(n):
            if not -1 - TOLERANCE <= corr[i][j] <= 1 + TOLERANCE:
                raise ValueError(f"Correlation [{i}][{j}] = {corr[i][j]} is outside -1 to 1.")
            if abs(corr[i][j] - corr[j][i]) > TOLERANCE:
                raise ValueError(f"Correlation table is not symmetric at [{i}][{j}].")


def covariance_matrix(corr, vols):
    """cov[i][j] = correlation[i][j] x volatility[i] x volatility[j]."""
    n = len(vols)
    return [[corr[i][j] * vols[i] * vols[j] for j in range(n)] for i in range(n)]


def portfolio_return(weights, returns):
    return sum(w * r for w, r in zip(weights, returns))


def portfolio_volatility(weights, cov):
    n = len(weights)
    variance = sum(weights[i] * weights[j] * cov[i][j] for i in range(n) for j in range(n))
    return math.sqrt(max(variance, 0.0))


# ---------------------------------------------------------------------------
# Mandate check and the lowest-risk search
# ---------------------------------------------------------------------------
def mandate_check(weights, returns, objective=OBJECTIVE_RETURN, max_weight=MAX_WEIGHT):
    """Every checkable mandate rule, each as pass/fail, so a verdict is never implied."""
    expected = portfolio_return(weights, returns)
    checks = {
        "weights sum to 100%": abs(sum(weights) - 1) <= 1e-6,
        "long-only (no weight below 0)": min(weights) >= -TOLERANCE,
        f"no fund above {max_weight:.0%}": max(weights) <= max_weight + TOLERANCE,
        f"expected return at least {objective:.1%}": expected >= objective - TOLERANCE,
    }
    return {"checks": checks, "passes": all(checks.values())}


def long_only_mixes(n_assets, step=STEP, max_weight=1.0):
    """Every long-only weight vector in `step` increments that sums to 1, with no
    single weight above `max_weight`. The cap is applied while building, so capped
    mixes are never generated (faster, and the cap cannot be forgotten later)."""
    units = round(1 / step)
    if abs(units * step - 1) > TOLERANCE:
        raise ValueError("step must divide 100% evenly, e.g. 0.05")
    cap_units = math.floor(max_weight / step + TOLERANCE)

    def build(remaining, slots):
        if slots == 1:
            if remaining <= cap_units:
                yield [remaining]
            return
        for k in range(min(remaining, cap_units) + 1):
            for rest in build(remaining - k, slots - 1):
                yield [k] + rest

    for counts in build(units, n_assets):
        yield [c * step for c in counts]


def lowest_risk_mix(returns, cov, objective=OBJECTIVE_RETURN, max_weight=MAX_WEIGHT,
                    step=STEP):
    """Lowest-volatility long-only mix on the grid with expected return >= objective
    and every weight <= max_weight. Returns a dict, or None when no mix qualifies.
    Ties in volatility keep the first mix found (deterministic)."""
    best, eligible = None, 0
    for weights in long_only_mixes(len(returns), step, max_weight):
        expected = portfolio_return(weights, returns)
        if expected < objective - TOLERANCE:
            continue
        eligible += 1
        vol = portfolio_volatility(weights, cov)
        if best is None or vol < best["volatility"] - 1e-12:
            best = {"weights": weights, "expected_return": expected, "volatility": vol}
    if best is not None:
        best["eligible_mixes"] = eligible
    return best


def max_feasible_return(returns, max_weight=MAX_WEIGHT):
    """Highest expected return any long-only mix can reach under the cap: fill the
    best funds to the cap in order. Used for the return-haircut break-even."""
    remaining, total = 1.0, 0.0
    for r in sorted(returns, reverse=True):
        w = min(max_weight, remaining)
        total += w * r
        remaining -= w
        if remaining <= TOLERANCE:
            break
    return total


def equal_weights(n):
    return [1.0 / n] * n


# ---------------------------------------------------------------------------
# Backtest: hold target weights, drift monthly, rebalance on schedule, pay costs
# ---------------------------------------------------------------------------
def backtest(target, returns, rebalance_months=REBALANCE_MONTHS, cost_bps=COST_BPS):
    """Simulate $1 invested at `target` weights over the monthly `returns` rows.

    Weights drift with returns; every `rebalance_months` months the portfolio trades
    back to target. Cost = one-way turnover x cost_bps / 10,000 of portfolio value,
    charged at each trade including the initial purchase.
    Returns the value path, monthly net returns and total turnover.
    """
    cost_rate = cost_bps / 10_000
    weights = list(target)
    path, net_returns, turnover_total = [1.0], [], sum(target)
    value = 1.0 - cost_rate * sum(target)          # initial purchase from cash
    start = value
    for month, row in enumerate(returns, start=1):
        gross = sum(w * r for w, r in zip(weights, row))
        weights = [w * (1 + r) / (1 + gross) for w, r in zip(weights, row)]
        value *= 1 + gross
        if month % rebalance_months == 0 and month < len(returns):
            turnover = sum(abs(t - w) for t, w in zip(target, weights)) / 2
            value *= 1 - cost_rate * turnover * 2   # buys + sells, both pay one-way cost
            turnover_total += turnover * 2
            weights = list(target)
        net_returns.append(value / path[-1] - 1)
        path.append(value)
    return {"path": path, "net_returns": net_returns, "turnover": turnover_total,
            "start_value": start}


def performance(path, net_returns):
    """Annualized geometric return, annualized volatility, max drawdown, worst month."""
    years = len(net_returns) / 12
    peak, max_dd = path[0], 0.0
    for v in path:
        peak = max(peak, v)
        max_dd = min(max_dd, v / peak - 1)
    return {
        "annual_return": (path[-1] / path[0]) ** (1 / years) - 1 if years > 0 else 0.0,
        "annual_volatility": _stdev(net_returns) * math.sqrt(12) if len(net_returns) > 1 else 0.0,
        "max_drawdown": max_dd,
        "worst_month": min(net_returns),
        "ending_value_per_dollar": path[-1],
    }
