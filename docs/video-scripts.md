# Video Scripts — Project 2 (Energy Satellite Sleeve)

**How to use these:**
- These are **speaking guides, not something to read word for word.** Graders are checking that *you* own the decisions and the code. Say it in your own words, and practise once with the code open.
- At about 140 words a minute, each script fits inside its limit with roughly 20 seconds spare.
- **Graders stop at the limit:** Video 1 at 3:00, Video 2 at 5:00, Video 3 at 5:00.

**Recording setup:**
- Small webcam view on, with clear audio. Polish isn't graded.
- Upload each video to YouTube as **Unlisted** (never Private), with a descriptive title.
- After uploading, download the auto-captions. Correct the tickers (XLE, XOP, AMLP, ICLN, NLR), the finance terms and the numbers, then save them as `docs/transcript-video-1.txt`, `-2.txt` and `-3.txt`. **The transcript must be what you actually said, not this script.**
- Write the real timestamps into the manifest's `timestamp_index` column.

AI disclosure: Claude drafted these scripts (see Validation-and-AI-Use §11). You own every claim you say on camera.

---

## Video 1 — Research evolution and AI-output check (≤ 3:00)

**Title:** `FIN439 Project 2 – Video 1 – Research Evolution and AI Check – Eric Boyd`

**Have open:** your Edition A PDF, `docs/research-evolution.md` (the change table), and `output/visible-output.md` (holdout table).

| Time | On screen | What to say (in your own words) |
|---|---|---|
| 0:00–0:20 | Edition A, page 1 | "This is my Project 2 Edition A, submitted [date] before any project-specific AI. My decision was whether a committee should fund an energy ETF sleeve. In Edition A my position was [your Edition A thesis]." |
| 0:20–1:00 | Change table, first row | "Edition B's position is a **no-capital pilot**. The consequential change came from **mixed** drivers: my own analysis plus a holdout test that AI helped build. What moved me was the out-of-sample result. I chose the mix using only October 2021 to September 2023, then tested it on the next 36 months." |
| 1:00–1:50 | Holdout table in `visible-output.md` | **AI-output check:** "The AI described this capped mix as the 'lowest-risk' portfolio. I didn't accept that label. I checked it against the naive equal-weight baseline out of sample. The strategy's volatility was **18.55%** against equal weight's **15.97%**, and its drawdown was **−15.0%** against **−12.9%**. So I **rejected** 'lowest risk' as a reason to adopt. It earned more, 15.86% a year, but that wasn't its job." |
| 1:50–2:20 | Validation §11, row "survives every one-point change" | "A second AI claim from Lab 15 was that the mix 'survives every one-point return change.' I **qualified** it. The objective sweep shows the 8% target never binds until 15.5%. So it's stable only because returns don't matter to this search, and the uncapped version broke my 40% cap." |
| 2:20–2:50 | Change table, remaining rows | "What stayed the same: [anything marked No material change, and the evidence for it]. Why that evidence is enough: the decision rule was written into the code before I ran the holdout, so I couldn't tune the result to the rule." |
| 2:50–3:00 | — | "So Edition B moved from [A] to pilot, because the risk claim failed a test it could have passed." |

**Timestamp index for the manifest:** Edition A 0:00 · change and driver 0:20 · AI-output check 1:00 · second AI check 1:50 · why the evidence is sufficient 2:20.

---

## Video 2 — Codebase walkthrough and validation (≤ 5:00)

**Title:** `FIN439 Project 2 – Video 2 – Codebase Walkthrough – Eric Boyd`

**Have open:** your code editor with the repo, a terminal in the project folder, and the GitHub repo page.

| Time | On screen | What to say / do |
|---|---|---|
| 0:00–0:25 | GitHub repo page, then README "Repository map" | "This is my Project 2 repo. Four Python files: `portfolio.py` holds all the finance math, `analysis.py` runs the study, `changed_input.py` runs the locked test, and `app.py` is the Streamlit front end. The app and analysis import the math. Neither copies it." |
| 0:25–0:55 | README "Data flow" diagram, then `data/DATA-SOURCE.md` | "Data flow: `prices.csv` is 61 month-ends of Yahoo adjusted close, downloaded October 22, 2026. The SHA-256 is pinned here. The file is never edited. Everything is as of September 30, 2026." |
| 0:55–1:30 | `portfolio.py` line 35 `read_prices`, then line 89 `estimate` | "`read_prices` refuses bad files: out-of-order dates, zero or negative prices, ragged rows. `monthly_returns` is price over previous price minus one. `estimate` annualizes: mean times 12, standard deviation times root 12, plus correlations. It also refuses a zero-volatility fund, because the correlation would be undefined." |
| 1:30–2:15 | `portfolio.py` line 175 `long_only_mixes` (point at `cap_units`, lines 182–189) | "This is the fix for my Lab 15 failure. The old app found 70% AMLP, which broke my 40% cap. Now the cap is applied **while the mixes are generated**: `cap_units` limits each slot, so a capped mix can never be produced. Five funds in 5-point steps is 10,626 mixes. The cap cuts that to 3,951, and every one of those clears 8%, so the return objective never constrains this answer." |
| 2:15–2:40 | Line 197 `lowest_risk_mix`, line 144 `covariance_matrix` | "`lowest_risk_mix` keeps mixes with expected return at least 8%, and picks the lowest volatility. Volatility is the square root of w-transpose times the covariance matrix times w. Covariance is correlation times the two volatilities." |
| 2:40–3:05 | `analysis.py` lines 24–36, then line 209–225 | "`analysis.py` freezes the holdout: the first 24 months choose, the last 36 test. The decision rule is written here as comments and code, **before** the holdout was run. Lines 209 to 225 apply it mechanically. The result is pilot." |
| 3:05–3:35 | Terminal: `python -m unittest discover -s tests -v` | "Sixteen tests. Known answers: a two-asset volatility of root 0.0175, the 10,626 grid count, and a closed-form 80/20 minimum variance. Line 96 reproduces Lab 15's 17.1383% volatility. Line 105 proves the holdout choice can't see the test months." |
| 3:35–4:15 | Terminal: `python changed_input.py` (only after you have locked your prediction) | **Highest-risk test.** "This is my Locked Changed-Input Record. I changed [input] from [old] to [new]. My prediction was committed at [commit] before the run. The script refuses to run otherwise. [Show the refusal by editing one character, then undo.] The result: [before → after]. That [matched / didn't match] my prediction because [your reason]." |
| 4:15–4:45 | Terminal: `python analysis.py`, then `streamlit run app.py`, moving the cap slider to 100% | "To reproduce from a clean machine: venv, pip install, then `python analysis.py`. The output hash matched in my cold run. In the app, if I set the cap to 100% the old 70% AMLP answer comes back and the cap check turns red. That's the failure the code now prevents." |
| 4:45–5:00 | `docs/validation-and-ai-use.md` §8 | "**Unresolved risk:** the minimum-volatility search depends on volatility estimates that didn't hold out of sample. The code is correct, but its input isn't stable. That's why the decision is a pilot." |

**Timestamp index:** architecture 0:00 · data lineage 0:25 · cap logic 1:30 · decision rule 2:40 · tests 3:05 · changed-input test 3:35 · reproduce 4:15 · failure mode 4:45.

---

## Video 3 — Investment-committee presentation (≤ 5:00)

**Title:** `FIN439 Project 2 – Video 3 – Investment Committee: Energy Sleeve Pilot – Eric Boyd`

**Have open:** `docs/decision-memo.pdf`. Present to camera. Lead with the decision, not the build.

| Time | On screen | What to say |
|---|---|---|
| 0:00–0:30 | Memo §1 | "My recommendation is to **pilot**: run a 12-month paper portfolio in an energy satellite sleeve, with **no capital**. Target mix: XLE 15, AMLP 40, ICLN 25, NLR 20, XOP zero. I'm asking the committee for three things: approve the pilot, confirm the 8% objective and 40% cap, and agree the adopt/reject triggers now." |
| 0:30–1:15 | Memo §2 table | "Why not adopt? The strategy's purpose is lower risk. Out of sample, from October 2023 to September 2026, it earned 15.9% a year net of costs, which beats the 8% objective. But volatility was 18.6% against 16.0% for a simple equal-weight portfolio, and the drawdown was worse: −15.0% against −12.9%. I fixed the decision rule before running that test. It passed two conditions and failed two." |
| 1:15–1:50 | Memo §3 | "Why not reject? In sample, the capped mix is about 2 points less volatile than equal weight, it passes every mandate check, and it has 7 points of return slack over 8%. The cap costs about one point of volatility. The uncapped answer, 70% AMLP, isn't eligible." |
| 1:50–2:40 | Memo §4 | "Give it a range, not a point. Return estimates are noisy: XLE's 24% has a standard error of about 12 points. That's why my range comes from 200 bootstrap re-estimates: XLE 5–25%, ICLN 15–35%, NLR 10–30%, and AMLP pinned at 40% in nearly every case. The good news is that the mix doesn't depend on those return guesses. The objective doesn't bind until 15.5%, and every return could fall 13.5 points before 8% becomes unreachable. Costs don't matter at annual rebalancing: even 50 basis points only moves the return from 15.9 to 15.7." |
| 2:40–3:30 | Memo §5 risks | "Principal risks: three of the five funds are oil-linked, with 0.8 to 0.9 correlation, and AMLP always hits the cap. The history includes the 2022 oil spike and a nuclear rally. Risk estimates didn't hold out of sample. Taxes on the MLP exposure and capacity aren't modelled." |
| 3:30–4:30 | Memo §5 triggers | "Here's what reverses this. **Reject** if the paper portfolio draws down more than 25%, or if the re-estimated mix can't reach 8%. **Rebalance early** if any fund drifts above 45%. **Review** if trailing volatility goes above 25%. At 12 months, **adopt** at the target mix only if both volatility and drawdown are no worse than equal weight's. Otherwise reject, or use plain equal weight." |
| 4:30–4:55 | Memo §1 | "So the ask: approve a no-capital 12-month pilot, confirm the 8% and 40% mandate, and pre-commit to those triggers. The analysis, tests and AI-use record are in the validation document." |

**Timestamp index:** decision and ask 0:00 · evidence against adoption 0:30 · evidence against rejection 1:15 · range and sensitivities 1:50 · risks 2:40 · reversal triggers 3:30 · committee ask 4:30.

**Practise one skeptical question:** *"If it beat equal weight on return, why not just adopt?"* Answer: "Return wasn't the claim. Lower risk was, and it failed. A 36-month return edge in one energy regime is inside the noise: the standard errors are about 8 to 13 points."
