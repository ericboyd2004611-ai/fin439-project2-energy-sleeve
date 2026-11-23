# Validation and AI-Use Record — Energy Satellite Sleeve (Project 2)

**Student:** Eric Boyd · **Course:** FIN 43900, Fall 2026 · **Record date:** 2026-11-23 · **Data as-of:** 2026-09-30

This is the single authoritative record of validation and AI use. The memo, README and videos point here rather than repeating it.

## 1. Sources and as-of boundary

| Input | Source | As-of / timing | Lineage |
|---|---|---|---|
| Monthly Adj Close, XLE / XOP / AMLP / ICLN / NLR | Yahoo Finance chart data (<https://finance.yahoo.com/quote/XLE/history/>, same endpoint for each ticker) | 61 month-ends, 2021-09 to 2026-09; downloaded 2026-10-22; October 2026 excluded as incomplete | `data/prices.csv`, SHA-256 `c7c39b97894fe0cfa4074cfbbbd68de0edb84fb6d983a884fff3d7c6a784313e`; unchanged since Lab 15; never edited. Full details in `data/DATA-SOURCE.md` |
| Mandate (8% objective, 40% cap, long-only, annual rebalance) | Working assumptions (Section 2) | Set in Lab 15 (2026-10-22); rebalance and cost added 2026-11-23 | `portfolio.py` constants |
| Trading cost, 10 bps one-way | **Assumption**, not sourced; 0–50 bps tested | — | `portfolio.COST_BPS` |
| Point-in-time risk signal: trailing 12-month volatility of the mix | Computed from the same price file | Value "as of" month *t* uses only prices dated ≤ *t*; used for month *t+1* decisions | `portfolio.risk_signal`; data card `data/SIGNAL-DATA-CARD.md` |

**Point-in-time:** all estimates use only data through 2026-09-30. The holdout chooses its mix from the first 24 returns (2021-10 to 2023-09) and is scored on the next 36 (2023-10 to 2026-09). A unit test proves the chosen mix cannot see the test months.

**Not used:** the Lab 17 BAA macro signal. It stayed quarantined, because each decision date did not have an eligible data vintage. The project's required point-in-time signal is the price-based risk signal above, which has no publication lag or revisions to audit (see its data card).

## 2. Mandate provenance — what is assumed, not given

The mandate follows the fields from Lab 13:

| Field | Value |
|---|---|
| Universe | XLE, XOP, AMLP, ICLN, NLR |
| Benchmark | Equal weight of the five funds (also baseline 1) |
| Risk measure | Annualized volatility; max drawdown is the stop limit (−25%) |
| Objective | Expected annual return ≥ 8% |
| Limits | No fund above 40%; long-only, fully invested; annual rebalancing |


The 8% objective and the 40% single-fund cap were **proposed by AI at my request in Lab 15** and adopted as working assumptions. They are not a real client's confirmed investment policy statement.

- 8% is an equity-like long-run growth target, set independently of the price history.
- The 40% cap carries Lab 13's concentration idea over to funds.

**Limitation → action:** the memo asks the committee to confirm both before the pilot starts.

## 3. Tests and results

`python -m unittest discover -s tests -v` → **20 tests, all pass** (Python 3.13.18 and 3.10.12, 2026-11-23).

| Test | Known answer | Result |
|---|---|---|
| Two-asset volatility by hand | 50/50, vols 10%/20%, ρ = 0.5 → √0.0175 = 13.229% | Pass (12 decimal places) |
| Grid size | 5 funds in 5% steps = C(24,4) = 10,626 mixes, each summing to 100% | Pass |
| Cap enforced inside the search | No generated mix above 40%; a 2-fund 40% cap gives no mixes | Pass |
| Minimum-variance closed form | Uncorrelated 10%/20% vols → 80/20 | Pass |
| Infeasible objective | Returns `None`, not a fake answer | Pass |
| Max feasible return under cap | 40%×10% + 40%×8% + 20%×6% = 8.4% | Pass |
| Estimate known answer | +2%/0% alternating → 12%/yr; sd 1%×√(12/11)×√12; ρ = −1 | Pass |
| Backtest compounding / costs reduce value / drawdown | 1.10×0.95; paid < free; 0.9/1.2 − 1 | Pass |
| Refusals | Out-of-order dates, zero price, ragged row, |ρ| > 1, asymmetric ρ, zero-volatility fund | All raise `ValueError` |
| Reproduces Lab 15 / Lab 20 | Capped 15/0/40/25/20 at 17.138330% volatility; uncapped 0/0/70/20/10 | Pass |
| Inverse-volatility known answer | Vols 10%/20% → weights 2/3, 1/3 | Pass |
| Verdict names the failed rule | 70/30 mix → FAIL "no fund above 40%" | Pass |
| **Signal is point-in-time** | Tripling every price after 2023-09 leaves the 2023-09 signal unchanged | Pass |
| Signal needs a full window | `None` with 11 returns; a value with 12 | Pass |
| Signal vs independent pandas calculation | 2022-10 / 2023-09 / 2026-09: 26.0594% / 15.4622% / 17.7593%, matching to 4 decimals | Pass (`data/SIGNAL-DATA-CARD.md`) |
| Holdout isolation | Scrambling the 36 test months leaves the chosen mix unchanged | Pass |
| App (Streamlit AppTest, 2026-11-23) | Default: portfolio and both baselines show PASS. Search cap 100% → 70% AMLP shows "FAIL: no fund above 40%" (verdicts judge the written mandate). Signal slider at 2022-10 → 26.06% REVIEW. Window switch and objective 30% (no feasible mix) run with no errors | Pass |

## 4. Highest-risk claim, baseline and holdout

**Highest-risk claim:** the capped minimum-volatility mix gives the committee *lower risk* than a naive alternative.

**Naive baseline:** equal weight (20% each), rebalanced on the same schedule and charged the same costs. XLE-only is a sector proxy, used for context.

| Holdout, Oct 2023–Sep 2026, net of 10 bps | Annual return | Volatility | Max drawdown | Worst month |
|---|---:|---:|---:|---:|
| Strategy (chosen on first 24 months: AMLP 40 / ICLN 20 / NLR 40) | 15.86% | **18.55%** | **−15.02%** | −9.71% |
| Equal weight | 14.11% | 15.97% | −12.88% | −9.22% |
| Inverse volatility (baseline 2, weights from the first 24 months' volatilities) | 15.28% | 17.05% | −12.64% | −9.77% |
| XLE only | 14.33% | 20.49% | −14.36% | −13.86% |

**Result:** the highest-risk claim **failed** out of sample. The strategy was riskier than equal weight on both risk measures, even though it earned more. This failure is what produces the PILOT decision (Section 9).

For contrast only: backtesting the 60-month mix on the same 60 months shows 14.51% a year. That figure uses look-ahead and is **not evidence**.

## 5. Selection ledger — every design choice, and when it was made

| # | Choice | Alternatives considered | Made before or after seeing the related result? |
|---|---|---|---|
| 1 | Five-ETF energy universe | — (AI proposal, Lab 15) | Before any results |
| 2 | 60-month estimation window | 36 months | Both run in Lab 15. Both reported here; neither hidden |
| 3 | Add 40% cap to the search | Uncapped | **After** Lab 15 showed a 70% AMLP breach. A mandate-driven fix, not a performance choice |
| 4 | 5-point grid | 2.5-point | Before. 2.5-point reported (Section 6) |
| 5 | 24/36 holdout split | — | Before the holdout was run (2026-11-23) |
| 6 | Decision rule (ADOPT / PILOT / REJECT) | — | Written into `analysis.py` before the holdout was run |
| 7 | 10 bps cost, annual rebalance | 0 / 25 / 50 bps | Before. All reported |
| 8 | Bootstrap: 200 draws, seed 43900 | — | Before. Not re-run with other seeds to find a better answer |
| 9 | Second baseline: inverse volatility (Lab 14's transparent baseline) | XLE-only (kept for context) | Added 2026-11-23 **after** the holdout, to meet the brief's two-baseline requirement. It does not enter the decision rule, which was fixed earlier |
| 10 | Point-in-time signal: trailing 12-month volatility, 25% threshold | BAA yield (quarantined in Lab 17) | Added 2026-11-23 after the holdout. The 25% threshold is the memo's existing review trigger, not tuned to the signal's history |
| 11 | Constraint stress: caps 30/35/40/50/100% | — | Added 2026-11-23, after the locked 30% run (which it reproduces) |

No other windows, universes, objectives or seeds were tried and discarded.

## 6. Robustness, costs and capacity

| Test | Result | Effect on decision |
|---|---|---|
| Standard error of return estimates | ±8.25 (AMLP) to ±13.46 (XOP) points | Return inputs are too noisy to adopt on |
| Objective sweep | All 3,951 capped mixes clear 8%. Mix unchanged until a 15.5% objective; maximum capped return 21.48% | The mix is driven by risk estimates, not return guesses |
| Uniform return haircut | 13.48 points before no capped mix reaches 8%; 7.20 points of slack for the recommended mix | The 8% objective is safe for now; it is a trigger to watch |
| Bootstrap, 200 draws | 190 feasible; 8% identical to target; AMLP at 40% at the 10th, 50th and 90th percentiles; XLE 5–25%, ICLN 15–35%, NLR 10–30% | Defines the tolerance range in the memo |
| Window 60 / 36 / first 24 months | AMLP 40 in all three; XLE 15/30/0; NLR 20/0/40 | Weights outside AMLP are unstable |
| 2.5-point grid | 15 / 0 / 40 / 27.5 / 17.5; volatility 17.13% vs 17.14% | Grid resolution is immaterial |
| Oil-trio correlation 0.95 | Volatility 17.14% → 17.36%; mix unchanged | Low sensitivity, because XOP is 0% |
| **Constraint stress: caps 30 / 35 / 40 / 50 / 100%** | Holdout volatility 17.45 / 18.60 / 18.55 / 20.77 / 28.95%; drawdown −13.93 / −16.08 / −15.02 / −16.92 / −23.88% | The cap protects against concentration; no cap level beats equal weight on risk |
| **Point-in-time risk signal** | Current (2026-09) 17.76% OK; max 26.06% (2022-10); at or above 25% in 7 of 49 months (2022-09 to 2023-04) | Monitoring trigger; part of the stop condition |

**Stop condition:** the process stops (reject) if the paper portfolio's drawdown is worse than −25%, or if the re-estimated capped mix cannot reach 8%. It pauses for review whenever the signal is at or above 25%.
| Costs 0 / 10 / 25 / 50 bps | Holdout 15.91% / 15.86% / 15.79% / 15.67% | Costs are not decision-relevant at annual rebalancing |

**Turnover:** about one rebalance a year back to target. Holdout one-way turnover is reported in `output/results.json`.

**Capacity:** not measured. No volume or bid-ask data was collected. **Limitation → action:** the pilot is paper-only, so capacity carries no risk until a capital decision is made. Check ADV and spreads before any adoption.

## 7. Cold-run evidence

| Item | Result |
|---|---|
| Setup | Fresh copy of the repository files (without `output/`) into an empty folder, a new `venv`, README commands only (Linux, Python 3.13.18, 2026-11-23, after the live-brief update) |
| `python analysis.py` | Ran first time. Output hashes are **identical** to the committed output: `visible-output.md` `d587d5a4…49308a8a`, `results.json` `3ced69a0…97dd33da8` |
| `python -m unittest discover -s tests -v` | 20 / 20 pass |
| `pip install -r requirements.txt` → `streamlit run app.py` | Installed Streamlit 1.67.0; server health check returned `ok` |
| Elapsed | 20 seconds, including the venv and the Streamlit install |
| Second environment | Python 3.10.12 (the Linux VM linked to my Mac): 20 / 20 pass, identical output hashes |
| First failure found (earlier build) | On Python 3.10, `test_zero_volatility_refused` failed and `results.json` differed in the 17th digit, because Python 3.12 changed how `sum()` adds floats. Fix: every sum uses `math.fsum`, the zero-volatility check uses a 1e-12 tolerance, and the JSON is rounded to 10 decimals. Earlier, tests were not discovered without `tests/__init__.py`; also fixed |
| Still to do (student) | Repeat the README-only run on your own Mac and record the result here: ________ |

## 8. Limitations that drive the action

1. **Risk estimates did not hold out of sample** (Section 4) → PILOT, not ADOPT.
2. **Return history comes from one energy regime**, with standard errors of ±8 to ±13 points → no capital.
3. **The mandate is not client-confirmed** (Section 2) → committee confirmation is part of the ask.
4. **Concentration:** three oil-linked funds, 0.79–0.93 correlated, with AMLP always at the cap → the drawdown kill trigger.
5. **Not modelled:** taxes (MLP exposure), capacity, intramonth liquidity → required before adoption.

## 9. Decision rule and outcome

The rule was fixed in `analysis.py` before the holdout was run:

- **ADOPT** if all four conditions pass: mandate on full sample; holdout net return ≥ 8%; holdout volatility ≤ equal weight; holdout drawdown no worse than equal weight.
- **REJECT** if the mandate fails, or if holdout return is below 0 *and* volatility is above equal weight.
- **PILOT** otherwise.

**Outcome: PILOT.** Pass, pass, fail, fail.

## 10. Locked Changed-Input Record

Copied from `docs/locked-changed-input-record.md` (the committed record; lock commit `89ab3f9`).
**Course rule:** the prediction below must be written by the student, **with AI off, before the run**. The run itself is AI-closed. Claude prepared this template and the runner (`changed_input.py`). Claude did **not** write the prediction and did not see it before the run.

### Step 1 — the input you will change (also set in `docs/locked-changed-input.json`)

| Field | Value |
|---|---|
| Input | Single-fund cap, `MAX_WEIGHT` (suggested; any supported input in `changed_input.py` works) |
| Old value (units) | 0.40 (40% of the sleeve) |
| New value (units) | 0.30 (30% of the sleeve) |
| Why this input is material | The cap is binding: AMLP sits at exactly 40% in every window and in the 10th–90th percentile of the bootstrap. A tighter cap tests the highest-risk claim, that the cap-constrained mix is a stable, lower-risk answer. |

If you choose a different input, edit both this table and the JSON before you commit.

### Step 2 — your prediction (AI off, before running)

1. Expected direction of the weights

AMLP should decrease from 40% to 30%. The freed-up 10% will likely shift toward XLE and NLR because they have relatively strong expected returns. XOP may also gain some weight, while ICLN will likely remain unchanged or decrease because of its low expected return.

2. Expected return and volatility

The portfolio's expected return will likely increase slightly because AMLP's weight is being redistributed toward funds with higher expected returns, especially XLE and NLR. However, volatility will likely increase because AMLP has the lowest volatility (18.4%), while the other funds are riskier. The portfolio may lose some diversification benefits.

3. Mandate and holdout return

The portfolio may still pass the mandate, but this depends on the updated return and risk calculations. The holdout return is uncertain because it depends on actual performance during the holdout period, not just estimated returns. I would expect a potentially higher return but also greater risk.

4. Expected decision effect

I expect the decision to remain PILOT because the portfolio still has exposure to multiple energy sectors. However, if the tighter cap causes volatility to exceed the mandate's limit or holdout performance to weaken significantly, the decision could change. A stronger holdout result with acceptable risk could support a more favorable decision.

5. Date and time

November 23, 2026, at 4:35 PM EST.

### Step 3 — lock it

```sh
git add docs/locked-changed-input-record.md docs/locked-changed-input.json
git commit -m "Lock changed-input prediction (AI off)"
git push
```

Lock commit: `89ab3f9b056eea3e2e45621f5b5966b6225b9ae5`   Timestamp: `2026-11-23T16:36:36-05:00` (committed on GitHub)

### Step 4 — run (AI closed)

```sh
python changed_input.py
```

The script refuses to run if the prediction is still this placeholder, or if the prediction, config, `portfolio.py` or `data/prices.csv` differ from a commit. It writes `output/changed-input-result.json` and prints a table.

### Step 5 — actual results (paste the printed table here)

Run: `python3 changed_input.py` at `2026-11-23T16:37:13-05:00`, against locked commit `89ab3f9`. Run with AI closed. Full output: `output/changed-input-result.json`.

| Result | Before (cap 40%) | After (cap 30%) |
|---|---|---|
| Weights (XLE / XOP / AMLP / ICLN / NLR) | 15 / 0 / 40 / 25 / 20 | 25 / 0 / 30 / 25 / 20 |
| Expected return | 15.20% | 15.75% |
| Volatility | 17.14% | 17.71% |
| Mandate passes | True | True |
| Holdout annual return (net) | 15.86% | 14.72% |
| Holdout volatility | 18.55% | 17.45% |
| Holdout max drawdown | −15.02% | −13.93% |
| Decision (rule in analysis.py) | PILOT | PILOT |

Equal-weight holdout for comparison (unchanged by the cap): volatility 15.97%, max drawdown −12.88%.

### Step 6 — reconciliation and diagnosis (your words)


| Item | Prediction vs. Actual | Assessment |
|---|---|---|
| 1. Portfolio Weights | Predicted AMLP would decrease to 30%, with XLE or other funds gaining weight. AMLP dropped 10% and XLE gained the full 10%. All other weights stayed the same. | Partly Matched |
| 2. Expected Return & Volatility | Predicted both would increase slightly. Expected return increased from 15.20% to 15.75%, and volatility increased from 17.14% to 17.71%. | Matched |
| 3. Mandate & Holdout | Predicted the mandate would still pass and holdout returns might increase. The mandate passed, but holdout return decreased from 15.86% to 14.72%. | Partly matched |
| 4. Decision | Predicted PILOT would remain PILOT. The actual decision stayed PILOT. | Matched |

### Actual decision effect

The decision remained PILOT after reducing the maximum weight from 40% to 30%. The portfolio still passes the mandate, but the holdout return decreased by 1.14 percentage points.

### Why results differed

The higher expected return did not translate into better holdout performance. Moving 10% from AMLP to XLE increased estimated return and volatility, but actual holdout volatility decreased from 18.55% to 17.45%. This difference occurred because historical performance and correlations during the holdout period can differ from the estimates used in the model.

### Committee recommendation

I recommend keeping the **PILOT** decision. The tighter 30% cap reduces concentration in AMLP while maintaining compliance with the mandate. Although expected return increased, holdout return decreased, showing that higher projected returns do not guarantee better performance. However, lower holdout volatility and a smaller maximum drawdown suggest improved downside risk during the test period. The committee should continue monitoring performance before approving a larger allocation.


## 11. Named AI-tool record

**Tool:** Claude (Anthropic), in the Claude desktop app with access to my `Fin 439` folder and its built-in browser. **Model:** configured `claude-opus-5-5` (Claude Opus 5.5). The serving model may differ.

**Interaction dates:**
- 2026-10-22 (Lab 15)
- 2026-11-17 (Lab 20)
- 2026-11-23 (Project 2 build)

**Edition A / B:** not applicable. Project 2 has no Edition A or Edition B checkpoint (course owner ruling 2026-10-14; editions ruling 2026-11-10, per the course `PROJECT-SUBMISSION-ARCHITECTURE.md`). The AI-off evidence for this project is the Locked Changed-Input prediction (§10), committed at 16:36:36 on 2026-11-23, before the run at 16:37:13.

| Date | AI task and material output | Check performed | Disposition and reason |
|---|---|---|---|
| 10-22 | Proposed the five energy ETFs, the 8% objective and the 40% cap | Fund names and exposures checked against each ticker's Yahoo page (Lab 15) | **Modified.** Kept as *working* assumptions only; the committee must confirm them (Section 2) |
| 10-22 | Downloaded monthly prices through the browser | SHA-256 of the downloaded text matches the saved file | **Accepted** |
| 10-22 | Wrote the grid search and price estimation in `portfolio.py` and the Lab 15 app | Output matched direct function calls; found and fixed a bug where all-month returns were mixed with 36-month volatilities | **Modified** (bug fixed) |
| 10-22 | Claimed the energy mix "survives every one-point return change" | Objective sweep shows it survives only because the 8% objective never binds (until 15.5%). The uncapped answer also breaks the cap | **Qualified.** Stable for the wrong reason, and non-compliant |
| 11-17 | Drafted the Lab 20 readiness audit and an AI-simulated partner challenge | Disclosed there as simulated, not a real partner exchange | **Accepted as a gap list only**; not used as evidence |
| 11-23 | Wrote the Project 2 engine extensions (cap inside the search, backtest, costs, drawdown), `analysis.py`, `changed_input.py`, the rebuilt `app.py` and 16 tests | Hand-calculated known answers; reproduction of Lab 15/20 numbers to 6 decimals; cold run with identical output hashes; AppTest | **Accepted after checks** |
| 11-23 | Proposed the holdout design, decision rule, bootstrap and stress tests | Rule written into code before the holdout ran; holdout isolation unit test | **Accepted** |
| 11-23 | Labelled the capped mix "lowest-risk" | Out-of-sample volatility 18.55% vs equal weight's 15.97% | **Rejected** as a basis for adoption. This is the main AI-output check (Video 1) |
| 11-23 | Added the inverse-volatility baseline, verdicts naming the failed rule, the point-in-time signal and its data card, the cap stress, and the stop condition. Rebuilt the app to show them, after reading the live Project 2 brief | 4 new unit tests (20 total); signal recomputed independently in pandas; AppTest; all earlier numbers unchanged | **Accepted after checks** |
| 11-23 | Drafted the README, memo, this record and the three video scripts | I checked every number against `output/visible-output.md` | **Modified** — student edits: ________ |

**Not done by AI:** the Locked Changed-Input prediction and its reconciliation, recording the videos, and correcting the transcripts.

**Student review:** ________ (list what you re-checked yourself and any edits).
