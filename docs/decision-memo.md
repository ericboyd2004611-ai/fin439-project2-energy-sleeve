# Investment Committee Memo — Energy Satellite Sleeve

> **AI use:** I used Claude (Anthropic), Claude Opus 5.5, to write the code, run the tests and draft this memo at my direction (record: `docs/validation-and-ai-use.md`). **The analysis and the decision are mine.** **Education, not investment advice.**

**To:** Investment Committee · **From:** Eric Boyd, Portfolio Analyst · **Date:** November 23, 2026 · **Data as of:** September 30, 2026

## 1. Recommendation and committee ask

**PILOT: approve a 12-month paper portfolio with no capital.** Do not adopt now, and do not reject outright.

- **Target mix:** XLE 15% / XOP 0% / AMLP 40% / ICLN 25% / NLR 20%.
- **Tolerance range** (10th–90th percentile of 200 bootstrap re-estimates): XLE 5–25%, XOP 0%, AMLP 40%, ICLN 15–35%, NLR 10–30%.
- **Intended user:** the investment committee deciding whether to fund an energy satellite sleeve.
- **Horizon:** a 5+ year holding horizon, matching the 5-year data window. This is a working assumption for the committee to confirm. The 12-month paper pilot is a gate *before* any capital is committed.
- **Mandate:**
    - **Universe:** XLE, XOP, AMLP, ICLN, NLR
    - **Benchmark:** equal weight
    - **Risk measure:** annualized volatility, with max drawdown as the stop limit
    - **Objective:** expected return ≥ 8%
    - **Limits:** no fund above 40%; long-only and fully invested; annual rebalancing

**The committee is asked to:**

1. Approve the paper pilot.
2. Confirm the 8% return objective and 40% single-fund cap as the sleeve's mandate.
3. Agree that the adopt/reject triggers in Section 5 decide the outcome at the 12-month review.

## 2. Why pilot and not adopt

The decision rule was fixed in code before the holdout was run (`analysis.py`). It passed two of its four conditions.

| Condition (rule fixed before holdout) | Result | Evidence |
|---|---|---|
| Mandate passes on full sample (≥ 8% expected return, no fund > 40%, long-only) | **PASS** | 15.20% expected return, max weight 40% |
| Holdout net return ≥ 8% | **PASS** | 15.86% a year, Oct 2023–Sep 2026, net of 10 bps costs |
| Holdout volatility ≤ equal weight | **FAIL** | 18.55% vs 15.97% |
| Holdout max drawdown no worse than equal weight | **FAIL** | −15.02% vs −12.88% |

The strategy's purpose is *lowest risk*, and that is the claim that failed. Out of sample it earned more than equal weight, but it was **riskier** on both risk measures. A minimum-volatility method that doesn't deliver lower volatility out of sample hasn't earned capital. The return edge rests on one 36-month energy regime.

**How this recommendation changed:**

| Stage | Answer | What changed it |
|---|---|---|
| Lab 15 starting point | AMLP 70 / ICLN 20 / NLR 10, described as "stable" to one-point return changes | — |
| Cap enforced in the search | XLE 15 / AMLP 40 / ICLN 25 / NLR 20 | The 70% AMLP answer broke the 40% mandate cap. "Stable" only because the 8% objective never binds |
| Out-of-sample holdout | Riskier than equal weight (18.55% vs 15.97% volatility) | The minimum-volatility claim failed out of sample: **adopt → pilot** |
| Locked changed-input test (cap 40% → 30%) | XLE 25 / AMLP 30 / ICLN 25 / NLR 20; still PILOT | A tighter cap cuts holdout risk, but not below equal weight's |

## 3. Evidence (Yahoo Finance monthly Adj Close, Sep 2021–Sep 2026, 60 returns)

| Portfolio | Expected return (60 mo) | Volatility (60 mo) | Mandate verdict | Holdout vol / max drawdown |
|---|---:|---:|---|---:|
| **Recommended, 40% cap** | **15.20%** | **17.14%** | PASS | 18.55% / −15.02% |
| Baseline 1: equal weight (benchmark) | 16.50% | 19.25% | PASS | 15.97% / −12.88% |
| Baseline 2: inverse volatility | 16.84% | 18.80% | PASS | **17.05% / −12.64%** |
| Uncapped search (AMLP 70 / ICLN 20 / NLR 10) | 15.14% | 16.11% | **FAIL**: no fund above 40% | 28.95% / −23.88% |

Out of sample, both simple baselines were less risky than the optimized mix. **Inverse volatility** had the shallowest drawdown and earned 15.28% a year, against 15.86% for the strategy. If the pilot fails, it is the obvious fallback.

*Conventions:* expected return = arithmetic monthly mean × 12; volatility = monthly sd × √12; holdout returns are compound and net of 10 bps costs; adjusted close includes reinvested distributions.

## 4. Material assumptions and sensitivities

| Assumption | Test | What happened |
|---|---|---|
| Historical means stand in for expected returns | Standard errors | ±8 to ±13 points per fund. XLE's 24.13% has a two-standard-error range of roughly 0.9% to 47.4%. |
| The 8% objective | Objective sweep; uniform haircut | The objective doesn't bind until 15.5%, so the mix is driven by volatility and correlation, not return guesses. Every fund's return can fall 13.5 points before *no* capped mix reaches 8%. The recommended mix has 7.2 points of slack. |
| Estimation window | 60 vs 36 vs first 24 months | AMLP stays at the 40% cap. XLE moves 0–30% and NLR 0–40%. |
| Return-estimate noise | 200 bootstrap re-estimates | Only 8% of draws reproduce the exact target. In 5% of draws (10 of 200) no capped mix reaches 8%. |
| Trading cost | 0 / 10 / 25 / 50 bps one-way | Holdout return 15.91% / 15.86% / 15.79% / 15.67%. Costs aren't decision-relevant at annual rebalancing. |
| Single-fund cap (constraint) | Caps of 30 / 35 / 40 / 50 / 100% | Holdout volatility 17.45 / 18.60 / 18.55 / 20.77 / 28.95%. Loosening the cap sharply raises out-of-sample risk, so **the 40% limit protects the committee**. No cap level beats equal weight. |

## 5. Risks, monitoring and reversal triggers

**Principal risks:**

- **Concentration in oil.** XLE, XOP and AMLP are 0.79–0.93 correlated, and AMLP always sits at the cap.
- **Regime dependence.** The 2022 oil spike and the nuclear rally inflate the return history.
- **Risk-estimate instability.** Volatility didn't hold up out of sample.
- **Not modelled:** taxes (AMLP's MLP exposure), capacity, and intramonth liquidity.

**Monitoring during the pilot.** These thresholds are my proposals for the committee to confirm:

| Trigger | Action |
|---|---|
| Paper drawdown worse than −25% (holdout worst was −15.0%) | **Reject** |
| **Point-in-time risk signal** (trailing 12-month volatility) ≥ 25%. Now 17.8%; ≥ 25% in 7 months of 2022–23 | **Pause** and review |
| Any fund above 45% between rebalances | Rebalance early (cap breach) |
| Re-estimated capped mix can't reach 8% | **Reject** |
| At 12 months, volatility *and* drawdown ≤ equal weight's | **Adopt** at the target mix |
| At 12 months, either is worse than equal weight's | **Reject**, or replace with the inverse-volatility baseline |

**Stop condition:** the process stops (reject) if the paper drawdown is worse than −25%, or if the re-estimated capped mix cannot reach 8%. Signal data card: `data/SIGNAL-DATA-CARD.md`.

## 6. Data, validation and AI use

Lineage: `data/DATA-SOURCE.md`. Tests (20 pass), holdout, selection ledger, Locked Changed-Input Record and AI disclosure: `docs/validation-and-ai-use.md`.
