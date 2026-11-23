# Data source and lineage — `prices.csv`

| Field | Value |
|---|---|
| Content | Monthly **Adj Close** (adjusted for dividends and splits) for XLE, XOP, AMLP, ICLN, NLR |
| Layout | `Date` first, oldest month first, one column per ticker; 61 month-ends, 2021-09 to 2026-09 |
| Source | Yahoo Finance chart data (`query1.finance.yahoo.com/v8/finance/chart/<TICKER>`, interval `1mo`), the same data behind each ticker's Historical Data page, e.g. <https://finance.yahoo.com/quote/XLE/history/> |
| Downloaded | 2026-10-22, through the Claude desktop app's built-in browser (Lab 15) |
| SHA-256 | `c7c39b97894fe0cfa4074cfbbbd68de0edb84fb6d983a884fff3d7c6a784313e` (matches the Lab 15 download record and the Lab 20 audit) |
| Date convention | Yahoo labels each monthly bar by its first day; the value is that month's last close. `2021-09` = the September 2021 month-end. |
| Exclusions | October 2026 left out because the month was not complete on the download date |
| Transformations | Simple monthly return = price / previous price − 1 (60 returns). Annualized: arithmetic mean × 12, sample standard deviation × √12, Pearson correlation. Done in `portfolio.py`; the CSV itself is never edited. |
| As-of boundary | Every result uses only information through **2026-09-30**. The holdout chooses its mix using only 2021-10 to 2023-09 returns. |

## The funds (descriptions from the Lab 15 record)

| Ticker | Fund | Energy exposure |
|---|---|---|
| XLE | State Street Energy Select Sector SPDR ETF | Large integrated oil & gas (S&P 500 energy sector) |
| XOP | State Street SPDR S&P Oil & Gas Exploration & Production ETF | Oil & gas producers (equal-weighted, more volatile) |
| AMLP | Alerian MLP ETF | Midstream pipelines and storage (MLPs) |
| ICLN | iShares Global Clean Energy ETF | Solar, wind and other clean-energy companies |
| NLR | VanEck Uranium and Nuclear ETF | Uranium miners and nuclear utilities/suppliers |

## Known limitations of this data

- **Adjusted close is a total-return proxy.** It assumes distributions are reinvested, and it is net of fund expenses, because those reduce NAV. It does not include taxes. AMLP's MLP-related tax treatment is not modelled.
- **Revisions.** Yahoo can re-adjust historical prices after new distributions. A re-download later could differ slightly. The SHA-256 above pins the exact file used.
- **No intraday liquidity or volume data.** Capacity is not measured (see the validation record).
- **Licensing.** Yahoo Finance data is provided under Yahoo's terms of service. Keep the repository private, or remove `prices.csv` before making it public, unless you have confirmed redistribution is permitted.
- **No credentials** are needed. Nothing here is private data.
