"""Energy satellite sleeve - committee app (Streamlit).

Run from the project folder:   streamlit run app.py
All finance math is imported from portfolio.py; this file only collects inputs and
displays results.
"""
from pathlib import Path

import streamlit as st

import portfolio as P

DATA = str(Path(__file__).resolve().parent / "data" / "prices.csv")

st.set_page_config(page_title="Energy Sleeve - Committee App", layout="wide")
st.title("Energy Satellite Sleeve: Committee App")
st.info("**AI use:** built with Claude (Anthropic), which wrote code and drafted documents at my "
        "direction. The analysis and the decision are mine. **Education, not investment advice.**")

# ---------------------------------------------------------------- sidebar: mandate controls
with st.sidebar:
    st.header("Mandate (as written)")
    st.markdown(f"**Objective:** expected return ≥ {P.OBJECTIVE_RETURN:.0%}  \n"
                "**Universe:** XLE, XOP, AMLP, ICLN, NLR  \n**Benchmark:** equal weight  \n"
                "**Risk measure:** annualized volatility; max drawdown as the stop limit  \n"
                f"**Limits:** no fund above {P.MAX_WEIGHT:.0%}; long-only, fully invested; annual rebalance")
    st.header("What-if search settings")
    st.caption("These change what the search is allowed to pick. Verdicts always judge the mandate as written.")
    objective = st.number_input("Search objective: minimum expected return (%)",
                                value=P.OBJECTIVE_RETURN * 100, step=0.5, format="%.1f", key="objective") / 100
    cap = st.slider("Search cap: single-fund maximum (%)", min_value=20, max_value=100,
                    value=int(P.MAX_WEIGHT * 100), step=5, key="cap") / 100
    st.header("Data")
    upload = st.file_uploader("Monthly prices CSV (Date first, oldest first)", type="csv")
    window = st.radio("Estimation window", ["All 60 months", "Last 36 months"], index=0)
    st.caption(f"Search: every long-only mix in {P.STEP:.0%} steps, capped at the slider value.")

source = upload if upload is not None else DATA
try:
    last_n = None if window.startswith("All") else 36
    est = P.estimate_from_prices(source, last_n=last_n)
    if upload is not None:
        upload.seek(0)
    names, dates, prices = P.read_prices(source if upload is None else upload)
    P.validate_correlation(est["correlation"], len(est["names"]))
except (ValueError, OSError) as error:
    st.error(f"Refusing to run: {error}")
    st.stop()

st.caption(f"Data: Yahoo Finance monthly Adj Close (`data/prices.csv`). Estimated from {est['months']} "
           f"monthly returns, {est['first_return_month']} to {est['last_return_month']}: mean × 12, "
           f"sd × √12, correlations. **As of {dates[-1]} month-end.** Historical estimates, not forecasts.")

# ---------------------------------------------------------------- editable return views
with st.expander("Edit expected returns (test a view; volatility and correlation stay as estimated)"):
    cols = st.columns(len(names))
    edited = []
    for col, name, r, v in zip(cols, names, est["returns"], est["volatilities"]):
        with col:
            edited.append(st.number_input(f"{name} (%)", value=round(r * 100, 2), step=0.5,
                                          format="%.2f", key=f"r-{window}-{name}") / 100)
            st.caption(f"Volatility {v:.2%}")

cov = P.covariance_matrix(est["correlation"], est["volatilities"])
current = P.lowest_risk_mix(edited, cov, objective, cap)

# ---------------------------------------------------------------- portfolio + two baselines
st.subheader("Your portfolio and two baselines, each with its mandate verdict")
candidates = {
    "Constrained portfolio (lowest risk within the mandate)": None if current is None else current["weights"],
    "Baseline 1: equal weight (also the benchmark)": P.equal_weights(len(names)),
    "Baseline 2: inverse volatility": P.inverse_volatility_weights(est["volatilities"]),
}
rows = {"Portfolio": [], **{n: [] for n in names}, "Exp. return": [], "Volatility": [], "Mandate verdict": []}
for label, w in candidates.items():
    rows["Portfolio"].append(label)
    if w is None:
        for n in names:
            rows[n].append("—")
        rows["Exp. return"].append("—")
        rows["Volatility"].append("—")
        rows["Mandate verdict"].append("❌ No mix meets the search objective under this search cap")
        continue
    check = P.mandate_check(w, edited)          # always the mandate as written
    for n, x in zip(names, w):
        rows[n].append(f"{x:.0%}")
    rows["Exp. return"].append(f"{P.portfolio_return(w, edited):.2%}")
    rows["Volatility"].append(f"{P.portfolio_volatility(w, cov):.2%}")
    rows["Mandate verdict"].append("✅ PASS" if check["passes"] else "❌ FAIL: " + "; ".join(check["failed_rules"]))
st.table(rows)
if current is not None:
    st.caption(f"{current['eligible_mixes']:,} mixes meet the objective under a {cap:.0%} cap.")

# ---------------------------------------------------------------- point-in-time signal
st.subheader("Point-in-time risk signal")
weights_for_signal = current["weights"] if current is not None else P.equal_weights(len(names))
eligible_dates = [d for d in dates if P.risk_signal(dates, prices, weights_for_signal, d) is not None]
as_of = st.select_slider("As known at month-end", options=eligible_dates, value=eligible_dates[-1])
sig = P.risk_signal(dates, prices, weights_for_signal, as_of)
c1, c2, c3 = st.columns(3)
c1.metric("Trailing 12-month volatility", f"{sig['annual_volatility']:.2%}")
c2.metric("Trailing 12-month return", f"{sig['trailing_return']:.2%}")
c3.metric("Status", sig["status"], help=f"REVIEW at or above {P.SIGNAL_THRESHOLD:.0%}")
st.caption(f"Uses only prices dated on or before {as_of}. Applies to the next month's decision. "
           "Data card: `data/SIGNAL-DATA-CARD.md`.")

# ---------------------------------------------------------------- stress run
with st.expander("Stress run: single-fund cap levels (estimates on this window)"):
    stress = {"Cap": [], "Mix": [], "Volatility": [], "Meets 40% mandate": []}
    for c in (0.30, 0.35, 0.40, 0.50, 1.00):
        m = P.lowest_risk_mix(edited, cov, objective, c)
        stress["Cap"].append(f"{c:.0%}")
        stress["Mix"].append("none" if m is None else " / ".join(f"{n} {x:.0%}" for n, x in zip(names, m["weights"])))
        stress["Volatility"].append("—" if m is None else f"{m['volatility']:.2%}")
        stress["Meets 40% mandate"].append("—" if m is None else ("yes" if max(m["weights"]) <= P.MAX_WEIGHT + 1e-9 else "no"))
    st.table(stress)

st.markdown("**Stop condition:** reject if the paper portfolio's drawdown is worse than −25% or the "
            f"re-estimated capped mix cannot reach 8%; pause for review when the signal is at or above "
            f"{P.SIGNAL_THRESHOLD:.0%}. Full results: `output/visible-output.md`.")
