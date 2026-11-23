# Validation and AI-Use Record — Energy Satellite Sleeve (Project 2)

**Student:** Eric Boyd · **Course:** FIN 43900, Fall 2026 · **Record date:** 2026-11-23 · **Data as-of:** 2026-09-30

This is the single authoritative record of validation and AI use. The memo, README and videos point here rather than repeating it.

## 1. Sources and as-of boundary

| Input | Source | As-of / timing | Lineage |
|---|---|---|---|
| Monthly Adj Close, XLE / XOP / AMLP / ICLN / NLR | Yahoo Finance chart data (<https://finance.yahoo.com/quote/XLE/history/>, same endpoint for each ticker) | 61 month-ends, 2021-09 to 2026-09; downloaded 2026-10-22; October 2026 excluded as incomplete | `data/prices.csv`, SHA-256 `c7c39b97894fe0cfa4074cfbbbd68de0edb84fb6d983a884fff3d7c6a784313e`; unchanged since Lab 15; never edited. Full details in `data/DATA-SOURCE.md` |
| Mandate (8% objective, 40% cap, long-only, annual rebalance) | Working assumptions (Section 2) | Set in Lab 15 (2026-10-22); rebalance and cost added 2026-11-23 | `portfolio.py` constants |
| Trading cost, 10 bps one-way | **Assumption**, not sourced; 0–50 bps tested | — | `portfolio.COST_BPS` |

**Point-in-time:** all estimates use only data through 2026-09-30. The holdout chooses its mix from the first 24 returns (2021-10 to 2023-09) and is scored on the next 36 (2023-10 to 2026-09). A unit test proves the chosen mix cannot see the test months.

**Not used:** the Lab 17 BAA macro signal. It stayed quarantined, because each decision date did not have an eligible data vintage.

## 2. Mandate provenance — what is assumed, not given

The 8% objective and the 40% single-fund cap were **proposed by AI at my request in Lab 15** and adopted as working assumptions. They are not a real client's confirmed investment policy statement.

- 8% is an equity-like long-run growth target, set independently of the price history.
- The 40% cap carries Lab 13's concentration idea over to funds.

**Limitation → action:** the memo asks the committee to confirm both before the pilot starts.

## 3. Tests and results

`python -m unittest discover -s tests -v` → **16 tests, all pass** (Python 3.13.18, 2026-11-23).

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
| Holdout isolation | Scrambling the 36 test months leaves the chosen mix unchanged | Pass |
| App (Streamlit AppTest, 2026-11-23) | Default view 15/0/40/25/20 with 4 passing checks; cap slider 100% → 70% AMLP; window switch and edits run with no errors | Pass |

## 4. Highest-risk claim, baseline and holdout

**Highest-risk claim:** the capped minimum-volatility mix gives the committee *lower risk* than a naive alternative.

**Naive baseline:** equal weight (20% each), rebalanced on the same schedule and charged the same costs. XLE-only is a sector proxy, used for context.

| Holdout, Oct 2023–Sep 2026, net of 10 bps | Annual return | Volatility | Max drawdown | Worst month |
|---|---:|---:|---:|---:|
| Strategy (chosen on first 24 months: AMLP 40 / ICLN 20 / NLR 40) | 15.86% | **18.55%** | **−15.02%** | −9.71% |
| Equal weight | 14.11% | 15.97% | −12.88% | −9.22% |
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
| Costs 0 / 10 / 25 / 50 bps | Holdout 15.91% / 15.86% / 15.79% / 15.67% | Costs are not decision-relevant at annual rebalancing |

**Turnover:** about one rebalance a year back to target. Holdout one-way turnover is reported in `output/results.json`.

**Capacity:** not measured. No volume or bid-ask data was collected. **Limitation → action:** the pilot is paper-only, so capacity carries no risk until a capital decision is made. Check ADV and spreads before any adoption.

## 7. Cold-run evidence

| Item | Result |
|---|---|
| Setup | Fresh copy of the repository files into an empty folder, a new `venv`, README commands only (Linux, Python 3.13.18, 2026-11-23) |
| `python analysis.py` | Ran first time. Output hashes are **identical** to the committed output: `visible-output.md` `63d2baad…21b7c855`, `results.json` `9d3b8f8f…8de298f2` |
| `python -m unittest discover -s tests -v` | 16 / 16 pass |
| `pip install -r requirements.txt` → `streamlit run app.py` | Installed Streamlit 1.67.0; server health check returned `ok` |
| Elapsed | 14 seconds, including the venv and the Streamlit install |
| First failure | None in the cold run. During development the tests were not discovered without `tests/__init__.py`; fixed and documented in the README command |
| Still to do (student) | Repeat the README-only run on your own Mac, and record the result here: ________ |

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

[Paste the completed `docs/locked-changed-input-record.md` here before making the PDF: input, old/new values with units, your AI-off prediction with its timestamp and lock commit, the before/after table from `python changed_input.py`, the actual decision effect, and your reconciliation and diagnosis.]

## 11. Named AI-tool record

**Tool:** Claude (Anthropic), in the Claude desktop app with access to my `Fin 439` folder and its built-in browser. **Model:** configured `claude-opus-5-5` (Claude Opus 5.5). The serving model may differ.

**Interaction dates:**
- 2026-10-22 (Lab 15)
- 2026-11-17 (Lab 20)
- 2026-11-23 (Project 2 build)

**Edition A boundary:** Edition A was submitted to Brightspace on ________ (receipt ________). Project-specific AI use in Lab 15 on 2026-10-22 was ☐ after / ☐ before that receipt. If before, see the disclosure in Research-Evolution.pdf.

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
| 11-23 | Drafted the README, memo, this record, Edition B and the three video scripts | I checked every number against `output/visible-output.md` | **Modified** — student edits: ________ |

**Not done by AI:** the Edition A baseline, the Locked Changed-Input prediction, recording the videos, and correcting the transcripts.

**Student review:** ________ (list what you re-checked yourself and any edits).
