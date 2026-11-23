"""Project 2 analysis - energy satellite sleeve.

Run from the project folder:   python analysis.py
Writes:  output/results.json        (every number, machine-readable)
         output/visible-output.md   (inputs, as-of date, results and decision for a grader)

Every number in the memo, validation record and video scripts comes from this run.
Standard library only; all finance math is imported from portfolio.py.
"""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

import portfolio as P

ROOT = Path(__file__).resolve().parent
PRICES = ROOT / "data" / "prices.csv"
OUT = ROOT / "output"

# Holdout design (frozen before the holdout was run, 2026-11-23):
ESTIMATION_MONTHS = 24     # first 24 monthly returns (Oct 2021 - Sep 2023) choose the mix
#                            the remaining 36 (Oct 2023 - Sep 2026) are never seen by the search
BOOTSTRAP_DRAWS = 200
BOOTSTRAP_SEED = 43900
COST_GRID_BPS = [0, 10, 25, 50]

# Decision rule (written before the holdout results were computed; see validation record):
#   ADOPT  = mandate passes AND holdout net return >= objective AND holdout volatility
#            <= equal-weight AND holdout max drawdown no worse than equal-weight
#   REJECT = mandate fails on the full sample, OR holdout net return < 0 AND holdout
#            volatility above equal-weight
#   PILOT  = anything in between (paper portfolio, no capital, re-review in 12 months)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pick(est, objective=P.OBJECTIVE_RETURN, max_weight=P.MAX_WEIGHT, step=P.STEP):
    P.validate_correlation(est["correlation"], len(est["returns"]))
    cov = P.covariance_matrix(est["correlation"], est["volatilities"])
    return P.lowest_risk_mix(est["returns"], cov, objective, max_weight, step), cov


def describe(names, weights):
    return {n: round(w, 4) for n, w in zip(names, weights)}


def stats_for(weights, est):
    cov = P.covariance_matrix(est["correlation"], est["volatilities"])
    return {"expected_return": P.portfolio_return(weights, est["returns"]),
            "volatility": P.portfolio_volatility(weights, cov)}


def main():
    names, dates, prices = P.read_prices(str(PRICES))
    returns = P.monthly_returns(prices)
    return_months = dates[1:]
    n = len(names)
    results = {
        "data": {
            "file": "data/prices.csv", "sha256": sha256(PRICES), "tickers": names,
            "price_months": [dates[0], dates[-1]], "monthly_returns": len(returns),
            "return_months": [return_months[0], return_months[-1]],
            "as_of": "2026-09-30 (last complete month-end in the file)",
            "source": "Yahoo Finance monthly Adj Close, downloaded 2026-10-22 (see data/DATA-SOURCE.md)",
        },
        "mandate": {"objective_return": P.OBJECTIVE_RETURN, "max_weight": P.MAX_WEIGHT,
                    "long_only": True, "grid_step": P.STEP,
                    "rebalance_months": P.REBALANCE_MONTHS, "cost_bps_one_way": P.COST_BPS},
    }

    # 1. Full-sample estimates and the recommended mix ---------------------------------
    full = P.estimate(returns)
    # Standard error of an annualized mean = 12 x monthly sd / sqrt(T) = annual vol x sqrt(12 / T)
    se = [v * (12 / full["months"]) ** 0.5 for v in full["volatilities"]]
    results["estimates_60m"] = {
        "return_standard_errors": describe(names, se),
        "returns": describe(names, full["returns"]),
        "volatilities": describe(names, full["volatilities"]),
        "correlation": [[round(x, 4) for x in row] for row in full["correlation"]],
    }
    capped, cov = pick(full)
    uncapped, _ = pick(full, max_weight=1.0)
    results["recommended_60m"] = {
        "weights": describe(names, capped["weights"]),
        "expected_return": capped["expected_return"], "volatility": capped["volatility"],
        "eligible_mixes": capped["eligible_mixes"],
        "mandate": P.mandate_check(capped["weights"], full["returns"])["checks"],
    }
    results["uncapped_60m"] = {
        "weights": describe(names, uncapped["weights"]),
        "expected_return": uncapped["expected_return"], "volatility": uncapped["volatility"],
        "mandate_passes": P.mandate_check(uncapped["weights"], full["returns"])["passes"],
    }

    # 2. Baselines on the same estimates -------------------------------------------------
    ew = P.equal_weights(n)
    xle = [1.0 if t == "XLE" else 0.0 for t in names]
    results["baselines_60m"] = {
        "equal_weight": stats_for(ew, full),
        "XLE_only": stats_for(xle, full),
    }

    # 3. Estimation-window sensitivity ---------------------------------------------------
    windows = {}
    for label, rows in {"all 60 months": returns, "last 36 months": returns[-36:],
                        "first 24 months": returns[:ESTIMATION_MONTHS]}.items():
        est = P.estimate(rows)
        mix, _ = pick(est)
        windows[label] = None if mix is None else {
            "weights": describe(names, mix["weights"]),
            "expected_return": mix["expected_return"], "volatility": mix["volatility"]}
    results["window_sensitivity"] = windows

    # 4. Holdout: choose on first 24 months, test on the next 36, net of costs ----------
    train, test = returns[:ESTIMATION_MONTHS], returns[ESTIMATION_MONTHS:]
    train_est = P.estimate(train)
    train_mix, _ = pick(train_est)
    holdout = {"estimation_months": [return_months[0], return_months[ESTIMATION_MONTHS - 1]],
               "test_months": [return_months[ESTIMATION_MONTHS], return_months[-1]],
               "chosen_weights": None if train_mix is None else describe(names, train_mix["weights"])}
    candidates = {"equal_weight": ew, "XLE_only": xle}
    if train_mix is not None:
        candidates = {"strategy": train_mix["weights"], **candidates}
    perf = {}
    for label, w in candidates.items():
        bt = P.backtest(w, test)
        perf[label] = {**P.performance(bt["path"], bt["net_returns"]), "turnover": bt["turnover"]}
    holdout["performance_net_10bps"] = perf
    if train_mix is not None:
        holdout["cost_sensitivity"] = {
            str(bps): P.performance(*(lambda b: (b["path"], b["net_returns"]))(
                P.backtest(train_mix["weights"], test, cost_bps=bps)))["annual_return"]
            for bps in COST_GRID_BPS}
    # In-sample backtest of the 60-month mix: shown ONLY to illustrate look-ahead bias.
    bt_in = P.backtest(capped["weights"], returns)
    holdout["in_sample_60m_mix_NOT_evidence"] = P.performance(bt_in["path"], bt_in["net_returns"])
    results["holdout"] = holdout

    # 5. Robustness tests on the 60-month estimates --------------------------------------
    robust = {}
    fine, _ = pick(full, step=0.025)
    robust["grid_2.5pt"] = {"weights": describe(names, fine["weights"]),
                            "volatility": fine["volatility"],
                            "expected_return": fine["expected_return"]}
    # Objective sweep: where does the target start to bind, and where is it infeasible?
    sweep, previous, binding_at = [], None, None
    max_ret = P.max_feasible_return(full["returns"])
    obj = P.OBJECTIVE_RETURN
    while obj <= max_ret + 1e-9:
        mix = P.lowest_risk_mix(full["returns"], cov, obj)
        w = None if mix is None else tuple(round(x, 4) for x in mix["weights"])
        if previous is not None and w != previous and binding_at is None:
            binding_at = obj
        sweep.append({"objective": round(obj, 4), "weights": w,
                      "volatility": None if mix is None else mix["volatility"]})
        previous = w
        obj += 0.005
    robust["objective_sweep"] = {"first_objective_that_changes_mix": binding_at,
                                 "max_feasible_return_under_cap": max_ret, "rows": sweep}
    # Uniform return haircut: how far below history can every return fall before the
    # 8% objective is unreachable for ANY capped mix, and for the recommended mix?
    robust["return_haircut_breakeven"] = {
        "any_capped_mix": max_ret - P.OBJECTIVE_RETURN,
        "recommended_mix": capped["expected_return"] - P.OBJECTIVE_RETURN,
    }
    # Correlation stress: oil trio (XLE, XOP, AMLP) moves together at 0.95.
    oil = [names.index(t) for t in ("XLE", "XOP", "AMLP")]
    stressed = [row[:] for row in full["correlation"]]
    for i in oil:
        for j in oil:
            if i != j:
                stressed[i][j] = 0.95
    P.validate_correlation(stressed, n)
    s_cov = P.covariance_matrix(stressed, full["volatilities"])
    s_mix = P.lowest_risk_mix(full["returns"], s_cov)
    robust["oil_correlation_0.95"] = {
        "recommended_mix_volatility": P.portfolio_volatility(capped["weights"], s_cov),
        "reoptimized_weights": describe(names, s_mix["weights"]),
        "reoptimized_volatility": s_mix["volatility"]}
    # Bootstrap: resample the 60 months with replacement; how often does each weight appear?
    rng = random.Random(BOOTSTRAP_SEED)
    draws = []
    for _ in range(BOOTSTRAP_DRAWS):
        sample = [returns[rng.randrange(len(returns))] for _ in returns]
        mix, _ = pick(P.estimate(sample))
        draws.append(None if mix is None else mix["weights"])
    feasible = [d for d in draws if d is not None]
    ranges = {}
    for j, t in enumerate(names):
        col = sorted(d[j] for d in feasible)
        ranges[t] = {"p10": col[int(0.10 * (len(col) - 1))], "median": col[len(col) // 2],
                     "p90": col[int(0.90 * (len(col) - 1))]}
    same = sum(1 for d in feasible if all(abs(a - b) < 1e-9 for a, b in zip(d, capped["weights"])))
    robust["bootstrap"] = {"draws": BOOTSTRAP_DRAWS, "seed": BOOTSTRAP_SEED,
                           "feasible_draws": len(feasible),
                           "share_identical_to_recommended": same / len(feasible),
                           "weight_range_p10_median_p90": ranges}
    results["robustness"] = robust

    # 6. Decision (rule fixed above, applied mechanically) -------------------------------
    mandate_ok = P.mandate_check(capped["weights"], full["returns"])["passes"]
    reasons = []
    if train_mix is None:
        decision = "REJECT"
        reasons.append("No capped mix met the objective in the estimation window.")
    else:
        s, e = perf["strategy"], perf["equal_weight"]
        conds = {
            "mandate passes (full sample)": mandate_ok,
            "holdout net return >= objective": s["annual_return"] >= P.OBJECTIVE_RETURN,
            "holdout volatility <= equal weight": s["annual_volatility"] <= e["annual_volatility"],
            "holdout max drawdown no worse than equal weight": s["max_drawdown"] >= e["max_drawdown"],
        }
        results["decision_conditions"] = conds
        if all(conds.values()):
            decision = "ADOPT"
        elif (not mandate_ok) or (s["annual_return"] < 0 and s["annual_volatility"] > e["annual_volatility"]):
            decision = "REJECT"
        else:
            decision = "PILOT"
        reasons = [f"{k}: {'PASS' if v else 'FAIL'}" for k, v in conds.items()]
    results["decision"] = {"action": decision, "reasons": reasons}

    OUT.mkdir(exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(results, indent=2))
    (OUT / "visible-output.md").write_text(render(results))
    print(render(results))


def pct(x, d=2):
    return "n/a" if x is None else f"{x * 100:.{d}f}%"


def mixline(weights):
    return " / ".join(f"{t} {w * 100:.1f}" if abs(w * 100 - round(w * 100)) > 1e-6
                      else f"{t} {w * 100:.0f}" for t, w in weights.items())


def render(r):
    d, m, rec = r["data"], r["mandate"], r["recommended_60m"]
    h = r["holdout"]
    L = []
    L.append("# Energy Satellite Sleeve - Visible Executed Output\n")
    L.append("Generated by `python analysis.py`. Historical estimates, not forecasts. "
             "A course project, not investment advice.\n")
    L.append("## Inputs and as-of boundary\n")
    L.append(f"- **Data:** `{d['file']}` - {d['source']}")
    L.append(f"- **SHA-256:** `{d['sha256']}`")
    L.append(f"- **Tickers:** {', '.join(d['tickers'])}")
    L.append(f"- **Prices:** month-ends {d['price_months'][0]} to {d['price_months'][1]}; "
             f"{d['monthly_returns']} monthly returns ({d['return_months'][0]} to {d['return_months'][1]})")
    L.append(f"- **As-of:** {d['as_of']}")
    L.append(f"- **Mandate:** expected return >= {pct(m['objective_return'], 1)}; no fund above "
             f"{pct(m['max_weight'], 0)}; long-only; {pct(m['grid_step'], 0)} grid; "
             f"rebalance every {m['rebalance_months']} months; {m['cost_bps_one_way']} bps one-way cost\n")
    L.append(f"## Decision: **{r['decision']['action']}**\n")
    for reason in r["decision"]["reasons"]:
        L.append(f"- {reason}")
    L.append("")
    L.append("## Recommended mix (all 60 months, 40% cap enforced)\n")
    L.append(f"**{mixline(rec['weights'])}** - expected return {pct(rec['expected_return'])}, "
             f"volatility {pct(rec['volatility'])}; {rec['eligible_mixes']:,} capped mixes met the objective.\n")
    L.append("| Mandate check | Result |\n|---|---|")
    for k, v in rec["mandate"].items():
        L.append(f"| {k} | {'PASS' if v else 'FAIL'} |")
    u = r["uncapped_60m"]
    L.append(f"\nWithout the cap the search picks **{mixline(u['weights'])}** "
             f"({pct(u['volatility'])} volatility) - mandate passes: **{u['mandate_passes']}**.\n")
    L.append("## Estimates (60 months, annualized)\n")
    L.append("| Fund | Return (mean x 12) | Std. error of return | Volatility (sd x sqrt 12) |\n|---|---:|---:|---:|")
    est = r["estimates_60m"]
    for t in d["tickers"]:
        L.append(f"| {t} | {pct(est['returns'][t])} | ±{pct(est['return_standard_errors'][t])} | "
                 f"{pct(est['volatilities'][t])} |")
    L.append("\nA 60-month mean is noisy: roughly two standard errors either side is a plausible range.")
    L.append("\n## Baselines on the same estimates\n")
    L.append("| Portfolio | Expected return | Volatility |\n|---|---:|---:|")
    L.append(f"| Recommended (capped) | {pct(rec['expected_return'])} | {pct(rec['volatility'])} |")
    for k, v in r["baselines_60m"].items():
        L.append(f"| {k.replace('_', ' ')} | {pct(v['expected_return'])} | {pct(v['volatility'])} |")
    L.append("\n## Estimation-window sensitivity (cap enforced)\n")
    L.append("| Window | Mix | Return | Volatility |\n|---|---|---:|---:|")
    for k, v in r["window_sensitivity"].items():
        L.append(f"| {k} | {'no feasible mix' if v is None else mixline(v['weights'])} | "
                 f"{pct(None if v is None else v['expected_return'])} | {pct(None if v is None else v['volatility'])} |")
    L.append("\n## Out-of-sample holdout (net of costs)\n")
    L.append(f"Mix chosen using only {h['estimation_months'][0]} to {h['estimation_months'][1]} returns: "
             f"**{'none' if h['chosen_weights'] is None else mixline(h['chosen_weights'])}**. "
             f"Tested on {h['test_months'][0]} to {h['test_months'][1]} with annual rebalancing.\n")
    L.append("| Portfolio | Annual return | Volatility | Max drawdown | Worst month | $1 grows to |\n"
             "|---|---:|---:|---:|---:|---:|")
    for k, v in h["performance_net_10bps"].items():
        L.append(f"| {k.replace('_', ' ')} | {pct(v['annual_return'])} | {pct(v['annual_volatility'])} | "
                 f"{pct(v['max_drawdown'])} | {pct(v['worst_month'])} | ${v['ending_value_per_dollar']:.3f} |")
    if "cost_sensitivity" in h:
        L.append("\nStrategy holdout annual return by one-way cost: " + "; ".join(
            f"{k} bps {pct(v)}" for k, v in h["cost_sensitivity"].items()))
    ins = h["in_sample_60m_mix_NOT_evidence"]
    L.append(f"\nFor contrast only (look-ahead, not evidence): the 60-month mix backtested on the "
             f"same 60 months shows {pct(ins['annual_return'])} a year.\n")
    rb = r["robustness"]
    L.append("## Robustness\n")
    g = rb["grid_2.5pt"]
    L.append(f"- **Finer 2.5-point grid:** {mixline(g['weights'])}, volatility {pct(g['volatility'])}")
    sw = rb["objective_sweep"]
    L.append(f"- **Objective sweep:** the mix first changes at a {pct(sw['first_objective_that_changes_mix'], 1)} "
             f"objective; the highest return any capped mix can reach is {pct(sw['max_feasible_return_under_cap'])}")
    hb = rb["return_haircut_breakeven"]
    L.append(f"- **Return haircut break-even:** every return can fall {pct(hb['any_capped_mix'])} before no capped "
             f"mix reaches 8%; the recommended mix itself has {pct(hb['recommended_mix'])} of slack")
    oc = rb["oil_correlation_0.95"]
    L.append(f"- **Oil correlation stress (XLE/XOP/AMLP at 0.95):** recommended mix volatility rises to "
             f"{pct(oc['recommended_mix_volatility'])}; re-optimized {mixline(oc['reoptimized_weights'])} at "
             f"{pct(oc['reoptimized_volatility'])}")
    bs = rb["bootstrap"]
    L.append(f"- **Bootstrap ({bs['draws']} resamples, seed {bs['seed']}):** {bs['feasible_draws']} feasible; "
             f"{pct(bs['share_identical_to_recommended'], 0)} identical to the recommended mix")
    L.append("\n| Fund | 10th pct weight | Median | 90th pct |\n|---|---:|---:|---:|")
    for t, v in bs["weight_range_p10_median_p90"].items():
        L.append(f"| {t} | {pct(v['p10'], 0)} | {pct(v['median'], 0)} | {pct(v['p90'], 0)} |")
    L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    main()
