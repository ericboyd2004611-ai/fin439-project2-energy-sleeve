# Data card: point-in-time risk signal

| Field | Value |
|---|---|
| **Signal** | Trailing 12-month realized volatility of the recommended mix (XLE 15 / XOP 0 / AMLP 40 / ICLN 25 / NLR 20), annualized |
| **What it measures** | How volatile the mix has actually been over the last 12 months. It is a risk-regime gauge, not a return forecast |
| **Source** | Yahoo Finance monthly Adj Close for XLE, XOP, AMLP, ICLN, NLR (<https://finance.yahoo.com/quote/XLE/history/>, same page for each ticker), in `data/prices.csv`. Lineage: `data/DATA-SOURCE.md` |
| **Formula** | For each of the last 12 months: mix return = Σ weight × fund return. Signal = sample standard deviation of those 12 returns × √12. Code: `portfolio.risk_signal` |
| **Units** | Percent per year (annualized standard deviation) |
| **Point-in-time rule** | The value "as of" month *t* uses only prices dated on or before *t*. A unit test (`test_signal_is_point_in_time`) changes every later price and confirms the value doesn't move |
| **Publication lag** | None for the inputs: an ETF's closing price is public at the close of the month's last trading day. **Rule:** the signal computed at month-end *t* is used only for decisions in month *t+1*, never to trade on the same close |
| **Revisions** | Market closing prices are not revised. **Adjusted** close is re-scaled backwards when a fund pays a distribution, so a later download can differ slightly. The file is pinned by SHA-256 (`c7c39b97…784313e`); the signal uses only returns, which adjustment leaves nearly unchanged |
| **Download date** | 2026-10-22 (Lab 15) |
| **Threshold and use** | At or above **25%** → status REVIEW: the pilot pauses, and the committee reviews the mix before the next rebalance. Below 25% → OK. The threshold is a working assumption for the committee to confirm |
| **Licensing** | Yahoo Finance terms of service. Keep the repository private |

## Three values checked independently

Recomputed with pandas (`DataFrame.pct_change`, `std(ddof=1)`), separately from `portfolio.py`. They match to 4 decimal places:

| As of month-end | 12 returns used | Signal (engine) | Signal (pandas) | Status |
|---|---|---:|---:|---|
| 2022-10 | 2021-11 to 2022-10 | 26.0594% | 26.0594% | REVIEW |
| 2023-09 | 2022-10 to 2023-09 | 15.4622% | 15.4622% | OK |
| 2026-09 | 2025-10 to 2026-09 | 17.7593% | 17.7593% | OK (current) |

Over the full history (49 month-ends with 12 returns available, 2022-09 to 2026-09), the signal was at or above 25% in **7 months**: 2022-09, 2022-10, 2022-12 and 2023-01 to 2023-04, the period around the 2022 energy-price spike.

## Why this signal and not BAA

Lab 17's BAA corporate-bond yield stayed **quarantined**. Each month's value is published after the month it measures, and admitting it would need an ALFRED vintage for every decision date. This price-based signal has no publication lag and no revisions to audit, so it can be admitted now.

**Your check (student):** open two or three of the fund pages above and compare a month-end Adj Close with `data/prices.csv`. Small differences can come from later distribution adjustments; note any you find.
