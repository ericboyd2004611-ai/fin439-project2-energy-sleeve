# Energy Satellite Sleeve — FIN 43900 Project 2 (Investment Management Application)

**Decision:** should the investment committee **adopt, pilot or reject** a five-ETF energy sleeve (XLE, XOP, AMLP, ICLN, NLR)? The sleeve is built as the lowest-volatility long-only mix that meets the mandate.

**Intended user:** the investment committee of a client deciding whether to fund an energy satellite allocation. The portfolio analyst (me) is presenting.

**Current answer (as of 2026-09-30 data):** **PILOT.** Run a paper portfolio with no capital for 12 months. Target mix: XLE 15 / XOP 0 / AMLP 40 / ICLN 25 / NLR 20, with a tolerance range of XLE 5–25 / AMLP 40 / ICLN 15–35 / NLR 10–30 (bootstrap 10th–90th percentile). The rule-based decision and its evidence are in `output/visible-output.md`. The committee memo is `docs/decision-memo.pdf`.

> Course project using historical estimates, not forecasts. Not investment advice.

## Mandate (working assumptions)

| Rule | Value | Where it lives |
|---|---|---|
| Objective | Expected annual return ≥ 8.0% | `portfolio.OBJECTIVE_RETURN` |
| Hard cap | No single fund above 40% | `portfolio.MAX_WEIGHT` (enforced inside the search) |
| Positions | Long-only, fully invested, no leverage | `long_only_mixes` |
| Search | Every mix in 5-point steps | `portfolio.STEP` |
| Rebalancing | Annually, back to target | `portfolio.REBALANCE_MONTHS` |
| Trading cost | 10 bps one-way (assumption; 0–50 bps tested) | `portfolio.COST_BPS` |

## Setup and run (clean machine, Python 3.10+)

```sh
git clone <this repository URL>
cd <repository folder>
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt      # only needed for the app

python analysis.py                   # writes output/results.json and output/visible-output.md
python -m unittest discover -s tests -v     # 16 known-answer and failure tests
streamlit run app.py                 # interactive explorer at http://localhost:8501
```

`analysis.py` and the tests use only the standard library, so they run before `pip install`. The full analysis takes about 5 seconds. The same command always gives the same numbers, because the bootstrap seed is fixed.

**Expected result:** `output/visible-output.md` ends up identical to the committed copy. It shows **Decision: PILOT** and a recommended mix of **XLE 15 / XOP 0 / AMLP 40 / ICLN 25 / NLR 20** (15.20% expected return, 17.14% volatility).

## Repository map

| Path | What it does |
|---|---|
| `portfolio.py` | All finance math: reading and validating prices, estimates, covariance, the capped grid search, mandate checks, backtest with rebalancing and costs, drawdown |
| `analysis.py` | The full study: recommended mix, baselines, window sensitivity, out-of-sample holdout, robustness tests, and the rule-based decision. Writes `output/` |
| `changed_input.py` | Runs the **Locked Changed-Input Record**. It refuses to run until the prediction, config, model and data are committed |
| `app.py` | Streamlit explorer with a cap slider, window switch, editable return views and pass/fail mandate checks |
| `tests/test_portfolio.py` | Known answers (hand-calculated volatility, combinatorial grid count, closed-form minimum variance, drawdown) and refusals (bad prices, bad correlations) |
| `data/prices.csv`, `data/DATA-SOURCE.md` | Input data and its lineage (source, download date, SHA-256, conventions) |
| `output/visible-output.md`, `output/results.json` | Visible executed output |
| `docs/` | Research evolution, decision memo, validation and AI-use record, locked record, video scripts, transcripts |
| `submission/` | Frozen PDFs for Brightspace, plus the manifest |

## Data flow

```
data/prices.csv ─► read_prices (checks order, gaps, ≤0 prices)
                 ─► monthly_returns ─► estimate (mean×12, sd×√12, correlation)
                 ─► validate_correlation ─► covariance_matrix
                 ─► long_only_mixes (cap applied while generating)
                 ─► lowest_risk_mix (return ≥ objective, lowest volatility)
                 ─► mandate_check ─► backtest / performance (holdout, costs)
                 ─► analysis.py decision rule ─► output/
```

## Data sources

Yahoo Finance monthly Adj Close, downloaded 2026-10-22. See `data/DATA-SOURCE.md` for the full lineage. No credentials, API keys or private data are used, so no `.env` file is needed.

## Known limitations

- Return estimates come from a five-year window that includes the 2022 energy spike. Standard errors are ±8 to ±13 points, so they are **not forecasts**.
- Volatility is the risk measure used to choose the mix. Drawdowns are reported but not optimized.
- Out of sample (Oct 2023–Sep 2026), the "lowest-risk" mix had **higher** volatility and a deeper drawdown than equal weight. That is why the decision is PILOT, not ADOPT.
- Three of the five funds are oil-linked (pairwise correlation 0.79–0.93), so diversification is limited.
- Taxes, capacity and intramonth liquidity are not modelled. Costs are a flat assumption.
- The 8% objective and 40% cap are working assumptions, not a real client's confirmed IPS.

## AI use

Built with AI assistance (Claude). The complete named record, with what was accepted, modified or rejected and how each item was checked, is in `docs/validation-and-ai-use.md`.
