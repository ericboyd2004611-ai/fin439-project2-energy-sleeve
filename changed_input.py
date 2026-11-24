"""Locked Changed-Input Record runner (run with AI closed).

Order the course requires:
  1. YOU write the prediction in docs/locked-changed-input-record.md (AI off).
  2. Set the change in docs/locked-changed-input.json.
  3. git add + git commit both files (this is the immutable lock).
  4. python changed_input.py      <- refuses to run unless steps 1-3 are done.

It records the commit hash, timestamp, before/after output and decision effect to
output/changed-input-result.json and prints a table to paste under "Actual results".
It never writes your prediction or your reconciliation - those must be yours.

Supported inputs (docs/locked-changed-input.json, "input"):
  "max_weight"          old/new as decimals, e.g. 0.40 -> 0.30
  "objective"           old/new as decimals, e.g. 0.08 -> 0.10
  "cost_bps"            old/new in basis points (affects the holdout only)
  "return:<TICKER>"     shift that fund's return estimate; old = 0, new = shift in decimals
  "window"              old/new number of most recent monthly returns, e.g. 60 -> 36
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

import portfolio as P

ROOT = Path(__file__).resolve().parent
RECORD = ROOT / "docs" / "locked-changed-input-record.md"
CONFIG = ROOT / "docs" / "locked-changed-input.json"
PLACEHOLDER = "[WRITE YOUR PREDICTION HERE"


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def refuse(msg):
    sys.exit(f"Refusing to run: {msg}")


def check_lock():
    text = RECORD.read_text()
    if PLACEHOLDER in text:
        refuse("the prediction in docs/locked-changed-input-record.md is still the placeholder.")
    for path in (RECORD, CONFIG):
        rel = path.relative_to(ROOT).as_posix()
        if not git("log", "-1", "--format=%H", "--", rel).stdout.strip():
            refuse(f"{rel} has never been committed. Commit the prediction before running.")
        if git("status", "--porcelain", "--", rel).stdout.strip():
            refuse(f"{rel} has uncommitted edits. The prediction must be locked as committed.")
    dirty = git("status", "--porcelain", "--", "portfolio.py", "data/prices.csv").stdout.strip()
    if dirty:
        refuse("portfolio.py or data/prices.csv differ from the commit; the model and data must be locked too.")
    return git("rev-parse", "HEAD").stdout.strip(), git("log", "-1", "--format=%cI").stdout.strip()


def run(settings, returns):
    rows = returns[-settings["window"]:]
    est = P.estimate(rows)
    rets = list(est["returns"])
    for t, shift in settings["shifts"].items():
        rets[settings["names"].index(t)] += shift
    cov = P.covariance_matrix(est["correlation"], est["volatilities"])
    mix = P.lowest_risk_mix(rets, cov, settings["objective"], settings["max_weight"])
    out = {"weights": None, "expected_return": None, "volatility": None,
           "mandate_passes": False, "holdout_annual_return": None,
           "holdout_volatility": None, "holdout_max_drawdown": None, "decision": "REJECT"}
    if mix is not None:
        out = {"weights": dict(zip(settings["names"], [round(w, 4) for w in mix["weights"]])),
               "expected_return": mix["expected_return"], "volatility": mix["volatility"],
               "mandate_passes": P.mandate_check(mix["weights"], rets, settings["objective"],
                                                 settings["max_weight"])["passes"]}
        train, test = returns[:24], returns[24:]
        t_est = P.estimate(train)
        t_rets = list(t_est["returns"])
        for t, shift in settings["shifts"].items():
            t_rets[settings["names"].index(t)] += shift
        t_mix = P.lowest_risk_mix(t_rets, P.covariance_matrix(t_est["correlation"], t_est["volatilities"]),
                                  settings["objective"], settings["max_weight"])
        if t_mix is not None:
            bt = P.backtest(t_mix["weights"], test, cost_bps=settings["cost_bps"])
            perf = P.performance(bt["path"], bt["net_returns"])
            ew = P.backtest(P.equal_weights(len(rets)), test, cost_bps=settings["cost_bps"])
            ew_perf = P.performance(ew["path"], ew["net_returns"])
            out["holdout_annual_return"] = perf["annual_return"]
            out["holdout_volatility"] = perf["annual_volatility"]
            out["holdout_max_drawdown"] = perf["max_drawdown"]
            conds = [out["mandate_passes"], perf["annual_return"] >= settings["objective"],
                     perf["annual_volatility"] <= ew_perf["annual_volatility"],
                     perf["max_drawdown"] >= ew_perf["max_drawdown"]]
            if all(conds):
                out["decision"] = "ADOPT"
            elif not out["mandate_passes"] or (perf["annual_return"] < 0 and
                                               perf["annual_volatility"] > ew_perf["annual_volatility"]):
                out["decision"] = "REJECT"
            else:
                out["decision"] = "PILOT"
    return out


def show(result, header):
    def fmt(x):
        return "none" if x is None else f"{x * 100:.2f}%"
    print(header)
    print(f"Changed {result['input']}: {result['old']} -> {result['new']} {result['units']}\n")
    print("| Result | Before | After |\n|---|---|---|")
    for label, k in [("Weights", "weights"), ("Expected return", "expected_return"),
                     ("Volatility", "volatility"), ("Mandate passes", "mandate_passes"),
                     ("Holdout annual return (net)", "holdout_annual_return"),
                     ("Holdout volatility", "holdout_volatility"),
                     ("Holdout max drawdown", "holdout_max_drawdown"), ("Decision (rule in analysis.py)", "decision")]:
        b, a = result["before"][k], result["after"][k]
        if k == "weights":
            b = "none" if b is None else " / ".join(f"{t} {w*100:.0f}" for t, w in b.items())
            a = "none" if a is None else " / ".join(f"{t} {w*100:.0f}" for t, w in a.items())
        elif k not in ("mandate_passes", "decision"):
            b, a = fmt(b), fmt(a)
        print(f"| {label} | {b} | {a} |")


def main():
    saved = ROOT / "output" / "changed-input-result.json"
    if saved.exists() and "--rerun" not in sys.argv:
        # The locked run already happened: never overwrite its evidence, just show it.
        r = json.loads(saved.read_text())
        show(r, f"Locked run already recorded (prediction lock commit {r['locked_commit'][:7]}, "
                f"committed {r['commit_time']}; run {r['run_time']}). Showing the saved result; "
                "nothing was overwritten. Use --rerun to recompute into output/changed-input-rerun.json.")
        return
    commit, commit_time = check_lock()
    cfg = json.loads(CONFIG.read_text())
    names, _, prices = P.read_prices(str(ROOT / "data" / "prices.csv"))
    returns = P.monthly_returns(prices)
    base = {"names": names, "window": len(returns), "objective": P.OBJECTIVE_RETURN,
            "max_weight": P.MAX_WEIGHT, "cost_bps": P.COST_BPS, "shifts": {}}
    changed = {**base, "shifts": {}}
    key, old, new = cfg["input"], cfg["old"], cfg["new"]
    if key.startswith("return:"):
        changed["shifts"] = {key.split(":", 1)[1]: new - old}
    elif key in ("max_weight", "objective", "cost_bps", "window"):
        if base[key] != old:
            refuse(f"config says old {key} = {old} but the locked model uses {base[key]}.")
        changed[key] = new
    else:
        refuse(f"unsupported input {key!r}.")
    before, after = run(base, returns), run(changed, returns)
    result = {"locked_commit": commit, "commit_time": commit_time,
              "run_time": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
              "input": key, "old": old, "new": new, "units": cfg.get("units", ""),
              "before": before, "after": after}
    (ROOT / "output").mkdir(exist_ok=True)
    target = "changed-input-rerun.json" if saved.exists() else "changed-input-result.json"
    (ROOT / "output" / target).write_text(json.dumps(result, indent=2))

    def fmt(x):
        return "none" if x is None else f"{x * 100:.2f}%"
    print(f"Locked commit {commit} ({commit_time}); run {result['run_time']}")
    print(f"Changed {key}: {old} -> {new} {result['units']}\n")
    print("| Result | Before | After |\n|---|---|---|")
    for label, k in [("Weights", "weights"), ("Expected return", "expected_return"),
                     ("Volatility", "volatility"), ("Mandate passes", "mandate_passes"),
                     ("Holdout annual return (net)", "holdout_annual_return"),
                     ("Holdout volatility", "holdout_volatility"),
                     ("Holdout max drawdown", "holdout_max_drawdown"), ("Decision (rule in analysis.py)", "decision")]:
        b, a = before[k], after[k]
        if k == "weights":
            b = "none" if b is None else " / ".join(f"{t} {w*100:.0f}" for t, w in b.items())
            a = "none" if a is None else " / ".join(f"{t} {w*100:.0f}" for t, w in a.items())
        elif k not in ("mandate_passes", "decision"):
            b, a = fmt(b), fmt(a)
        print(f"| {label} | {b} | {a} |")


if __name__ == "__main__":
    main()
