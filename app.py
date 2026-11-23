"""Energy satellite sleeve - interactive explorer (Streamlit).

Run from the project folder:   streamlit run app.py
All finance math is imported from portfolio.py; this file only collects inputs and
displays results. Fixes the Lab 15 defect: the 40% single-fund cap is now enforced
inside the search, and every answer shows its mandate check.
"""
from pathlib import Path

import streamlit as st

import portfolio as P

DATA = str(Path(__file__).resolve().parent / "data" / "prices.csv")

st.set_page_config(page_title="Energy Sleeve - Lowest-Risk Mix", layout="wide")
st.title("Energy Satellite Sleeve: Lowest-Risk Mix")
st.caption("Historical estimates, not forecasts. A course project, not investment advice. "
           "Built with AI assistance - see docs/validation-and-ai-use.md.")

with st.sidebar:
    st.header("Mandate")
    objective = st.number_input("Minimum expected annual return (%)", value=P.OBJECTIVE_RETURN * 100,
                                step=0.5, format="%.1f") / 100
    cap = st.slider("Single-fund cap (%)", min_value=20, max_value=100,
                    value=int(P.MAX_WEIGHT * 100), step=5) / 100
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
    est_all = P.estimate_from_prices(source if upload is None else upload)
    P.validate_correlation(est["correlation"], len(est["names"]))
except (ValueError, OSError) as error:
    st.error(f"Refusing to run: {error}")
    st.stop()

names = est["names"]
st.subheader(f"Universe: {', '.join(names)}")
st.write(f"Estimated from {est['months']} monthly returns ({est['first_return_month']} to "
         f"{est['last_return_month']}): mean × 12, standard deviation × √12, correlations. "
         "**As of the last month-end in the file.**")

st.markdown("**Expected returns (edit to test a view; volatility and correlation stay as estimated)**")
cols = st.columns(len(names))
edited = []
for col, name, r, v in zip(cols, names, est["returns"], est["volatilities"]):
    with col:
        edited.append(st.number_input(f"{name} (%)", value=round(r * 100, 2), step=0.5,
                                      format="%.2f", key=f"r-{window}-{name}") / 100)
        st.caption(f"Volatility {v:.2%}")

cov = P.covariance_matrix(est["correlation"], est["volatilities"])
cov_all = P.covariance_matrix(est_all["correlation"], est_all["volatilities"])
current = P.lowest_risk_mix(edited, cov, objective, cap)
reference = P.lowest_risk_mix(est_all["returns"], cov_all, P.OBJECTIVE_RETURN, P.MAX_WEIGHT)


def show(title, result, rets, obj, mx):
    st.markdown(f"#### {title}")
    if result is None:
        st.error("No mix meets the objective under this cap.")
        return
    st.table({"Fund": names, "Weight": [f"{w:.0%}" for w in result["weights"]]})
    st.markdown(f"Expected return **{result['expected_return']:.2%}** · "
                f"Volatility **{result['volatility']:.2%}**")
    check = P.mandate_check(result["weights"], rets, obj, mx)
    for rule, ok in check["checks"].items():
        st.write(("✅ " if ok else "❌ ") + rule)


left, right = st.columns(2)
with left:
    show("Your settings", current, edited, objective, cap)
with right:
    show("Reference: mandate as written, all 60 months", reference, est_all["returns"],
         P.OBJECTIVE_RETURN, P.MAX_WEIGHT)

if current is not None and reference is not None:
    moves = [abs(a - b) * 100 for a, b in zip(current["weights"], reference["weights"])]
    i = max(range(len(names)), key=lambda k: moves[k])
    st.metric("Largest weight change vs reference", f"{moves[i]:.0f} points", help=f"Fund: {names[i]}")
