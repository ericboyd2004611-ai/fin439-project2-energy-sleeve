# Investment Committee Memo — Energy Satellite Sleeve

**To:** Investment Committee · **From:** Eric Boyd, Portfolio Analyst · **Date:** November 23, 2026 · **Data as of:** September 30, 2026

## 1. Recommendation and committee ask

**PILOT: approve a 12-month paper portfolio with no capital.** Do not adopt now, and do not reject outright.

- **Target mix:** XLE 15% / XOP 0% / AMLP 40% / ICLN 25% / NLR 20%.
- **Tolerance range** (10th–90th percentile of 200 bootstrap re-estimates): XLE 5–25%, XOP 0%, AMLP 40%, ICLN 15–35%, NLR 10–30%.

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

The strategy's purpose is *lowest risk*, and that is the claim that failed. The mix chosen on the first 24 months (AMLP 40 / ICLN 20 / NLR 40) earned more than equal weight out of sample. But it was **riskier** than equal weight on both risk measures. A minimum-volatility method that doesn't deliver lower volatility out of sample hasn't earned capital. The return result is not enough to adopt, because it rests on one 36-month energy regime.

## 3. Evidence (Yahoo Finance monthly Adj Close, Sep 2021–Sep 2026, 60 returns)

| Portfolio (60-month estimates) | Expected return | Volatility |
|---|---:|---:|
| **Recommended, 40% cap** | **15.20%** | **17.14%** |
| Equal weight (naive baseline) | 16.50% | 19.25% |
| XLE only (sector proxy) | 24.13% | 26.02% |
| Uncapped search (AMLP 70 / ICLN 20 / NLR 10) — **breaches cap** | 15.14% | 16.11% |

- **On estimated risk:** in-sample, the capped mix is about 2.1 points less volatile than equal weight.
- **What the cap costs:** about 1.0 point of volatility versus the uncapped answer. The uncapped answer breaks the mandate, so it isn't eligible.
- **Conventions:**
    - Expected return is the arithmetic monthly mean × 12. Volatility is the monthly standard deviation × √12.
    - Holdout returns are geometric (compound) and net of costs.
    - Adjusted close includes reinvested distributions and is net of fund expenses.

## 4. Material assumptions and sensitivities

| Assumption | Test | What happened |
|---|---|---|
| Historical means stand in for expected returns | Standard errors | ±8 to ±13 points per fund. XLE's 24.13% has a two-standard-error range of roughly 0.9% to 47.4%. |
| The 8% objective | Objective sweep; uniform haircut | The objective doesn't bind until 15.5%, so the mix is driven by volatility and correlation, not return guesses. Every fund's return can fall 13.5 points before *no* capped mix reaches 8%. The recommended mix has 7.2 points of slack. |
| Estimation window | 60 vs 36 vs first 24 months | AMLP stays at the 40% cap. XLE moves 0–30% and NLR 0–40%. |
| Return-estimate noise | 200 bootstrap re-estimates | Only 8% of draws reproduce the exact target. In 5% of draws (10 of 200) no capped mix reaches 8%. |
| Grid resolution | 2.5-point grid | 15 / 0 / 40 / 27.5 / 17.5. Volatility differs by 0.01 point. |
| Trading cost | 0 / 10 / 25 / 50 bps one-way | Holdout return 15.91% / 15.86% / 15.79% / 15.67%. Costs aren't decision-relevant at annual rebalancing. |
| Correlation regime | Oil trio (XLE/XOP/AMLP) set to 0.95 | Volatility rises 17.14% → 17.36%. The mix is unchanged. |

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
| Trailing-12-month volatility above 25% | Review the mix |
| Any fund above 45% between rebalances | Rebalance early (cap breach) |
| Re-estimated capped mix can't reach 8% | **Reject** |
| At 12 months, volatility *and* drawdown ≤ equal weight's | **Adopt** at the target mix |
| At 12 months, either is worse than equal weight's | **Reject**, or replace with an equal-weight sleeve |

## 6. Data, validation and AI use

- **Data and lineage:** `data/DATA-SOURCE.md`. File SHA-256 `c7c39b97…784313e`.
- **Tests:** 16 automated known-answer and failure tests pass. The tests, holdout design, selection ledger, Locked Changed-Input Record and named AI-tool disclosure are all in **Validation-and-AI-Use.pdf**.
- **Reproduce:** run `python analysis.py` (README).
