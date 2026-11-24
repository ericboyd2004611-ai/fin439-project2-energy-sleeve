# Video Scripts — Project 2 (Energy Satellite Sleeve)

**How to use these:**
- These are **speaking guides, not something to read word for word.** Graders are checking that *you* own the decisions and the code. Say it in your own words, and practise once with the code open.
- At about 140 words a minute, each script fits inside its limit with roughly 15–20 seconds spare.
- **Graders stop at the limit:** Video 1 at 3:00, Video 2 at 5:00, Video 3 at 5:00.

**Required by the Project 2 brief: every video opens with two statements.** Say them in your own words, in about 10 seconds:

> "I used Claude, from Anthropic, to write the code, run tests and draft documents at my direction. The analysis and the decision are mine. This is education, not investment advice."

**Recording setup:**
- Small webcam view on, with clear audio. Polish isn't graded.
- Upload each video to YouTube as **Unlisted** (never Private), with a descriptive title and **captions/transcripts enabled**.
- After uploading, download the auto-captions. Correct the tickers (XLE, XOP, AMLP, ICLN, NLR), the finance terms and the numbers, then save them as `docs/transcript-video-1.txt`, `-2.txt` and `-3.txt`. **The transcript must be what you actually said, not this script.**
- Write the real timestamps into the manifest.

AI disclosure: Claude drafted these scripts (see Validation-and-AI-Use §11). You own every claim you say on camera.

---

## Video 1 — How the system and my thinking changed, plus an AI-output check (≤ 3:00)

Project 2 has no Edition A or B. Per the brief, this video shows **how your system and your thinking changed, plus one AI output you checked**.

**Title:** `FIN439 Project 2 – Video 1 – How the System Changed and AI Check – Eric Boyd`

**Have open:** `Lab 15/Lab 15.md` (your starting point), `output/visible-output.md`, `docs/locked-changed-input-record.md`, and `docs/validation-and-ai-use.md` §11.

| Time | On screen | What to say (in your own words) |
|---|---|---|
| 0:00–0:10 | Webcam / README top | **The two statements** (AI use, the analysis and decision are mine, education not advice). |
| 0:10–0:30 | `Lab 15.md`, the "Answer" section | "In Lab 15 my starting point was: the lowest-risk energy mix is 70% AMLP, 20% ICLN, 10% NLR, and it survives every one-point return change. I took that as a stable answer." |
| 0:30–1:00 | `Lab 15.md`, "Mandate check the app does not do" | "**First change, to the system:** that answer broke my own 40% single-fund cap, because the app never checked it. So I moved the cap *inside* the search, and the app now gives every portfolio a pass/fail verdict against the mandate. The mix became 15 / 0 / 40 / 25 / 20. **Driver:** my own analysis of the Lab 15 output." |
| 1:00–1:45 | `visible-output.md`, holdout table | "**Second change, to my thinking:** I'd been treating it as a lower-risk portfolio. So I tested it on data it hadn't seen: chosen on 2021–2023, tested on Oct 2023 to Sep 2026. It earned 15.86% a year, but volatility was **18.55% vs 15.97%** for equal weight, and the drawdown was worse. Even the simple inverse-volatility baseline was less risky. My position moved from 'adopt the lowest-risk mix' to a **no-capital pilot**. **Driver:** mixed — course instruction on holdouts, plus a test that AI helped build." |
| 1:45–2:25 | Validation §11, the "lowest-risk" and "survives every change" rows | **AI-output check:** "The AI's Lab 15 claim was that the mix 'survives every one-point return change.' I checked it with an objective sweep. It survives only because the 8% target never binds until 15.5%: all 3,951 capped mixes clear 8%. So I **qualified** it: stable, but for the wrong reason. Its 'lowest-risk' label I **rejected** as a basis for adoption, based on the holdout." |
| 2:25–2:55 | `locked-changed-input-record.md`, Steps 2 and 6 | "My own AI-off check: I predicted the cap going from 40 to 30 would move weight to XLE *and* NLR. It all went to XLE. I'd reasoned from returns, but the search minimizes volatility. That's partly matched, and the decision stayed PILOT." |
| 2:55–3:00 | — | "So the system now enforces the mandate, and my recommendation follows the out-of-sample evidence, not the in-sample label." |

**Timestamp index:** statements 0:00 · starting point 0:10 · system change 0:30 · thinking change and driver 1:00 · AI-output check 1:45 · own AI-off check 2:25.

---

## Video 2 — Codebase walkthrough and validation (≤ 5:00)

**Title:** `FIN439 Project 2 – Video 2 – Codebase Walkthrough – Eric Boyd`

**Have open:** your code editor with the repo, a terminal in the project folder, and the GitHub repo page.

| Time | On screen | What to say / do |
|---|---|---|
| 0:00–0:10 | Webcam / README top | **The two statements.** |
| 0:10–0:30 | GitHub repo, README "Repository map" | "This is my Project 2 repo. `portfolio.py` holds all the finance math, `analysis.py` runs the study, `changed_input.py` runs the locked test, and `app.py` is the Streamlit app. The app and analysis import the math. Neither copies it." |
| 0:30–0:50 | `data/DATA-SOURCE.md` | "Data: `prices.csv` is 61 month-ends of Yahoo adjusted close, downloaded October 22, 2026, SHA-256 pinned, never edited. Everything is as of September 30, 2026." |
| 0:50–1:15 | `portfolio.py` line 36 `read_prices`, line 90 `estimate` | "`read_prices` refuses bad files: out-of-order dates, zero prices, ragged rows. `estimate` annualizes: mean times 12, standard deviation times root 12, plus correlations." |
| 1:15–1:50 | Line 177 `long_only_mixes` (point at `cap_units`, line 184) | "This is the fix for my Lab 15 failure. The cap is applied **while the mixes are generated**, so a capped mix can never be produced. Five funds in 5-point steps is 10,626 mixes. The cap cuts that to 3,951, and every one of them clears 8%, so the return objective never constrains this answer." |
| 1:50–2:10 | Line 199 `lowest_risk_mix`, line 164 `mandate_check` | "`lowest_risk_mix` picks the lowest volatility among mixes that meet the objective. `mandate_check` returns every rule as pass or fail, and names the rule that failed. That's what the app shows beside each portfolio." |
| 2:10–2:35 | Line 231 `equal_weights`, line 236 `inverse_volatility_weights`, line 250 `risk_signal` | "Two baselines: equal weight, which is also my benchmark, and inverse volatility. Then my point-in-time signal: trailing 12-month volatility of the mix. It only uses prices dated on or before the as-of month, so it can't see the future." |
| 2:35–2:55 | `analysis.py` lines 24–36, then lines 258–278 | "`analysis.py` freezes the holdout: the first 24 months choose, the last 36 test. The decision rule is written here before the holdout ran. Lines 258 to 278 apply it mechanically. The result is pilot." |
| 2:55–3:25 | Terminal: `python3 -m unittest discover -s tests -v` | "Twenty tests. Known answers: a two-asset volatility of root 0.0175, the 10,626 grid count, a closed-form 80/20 minimum variance. Line 84 proves the signal is point-in-time: I triple every later price and the signal doesn't move. Line 132 proves the holdout choice can't see the test months." |
| 3:25–4:10 | `docs/locked-changed-input-record.md`, then terminal `python3 changed_input.py` | **Highest-risk test.** "My Locked Changed-Input Record: cap 40 to 30%. My prediction was committed at 4:36 PM, commit 89ab3f9, before the run." [Run `python changed_input.py`. It shows the saved locked result without overwriting it.] "The result: AMLP 40 to 30, and all 10 points went to XLE, not NLR as I predicted. Volatility went up in sample but down in the holdout. Still PILOT." |
| 4:10–4:40 | Terminal: `python3 analysis.py` | "To reproduce from a clean machine: venv, pip install, `python analysis.py`. The output file hash matched in my cold runs on two Python versions." |
| 4:40–4:58 | `docs/validation-and-ai-use.md` §8 | "**Unresolved risk:** the minimum-volatility search depends on volatility estimates that didn't hold out of sample. The code is correct, but its input isn't stable. That's why it's a pilot." |

**Timestamp index:** statements 0:00 · architecture 0:10 · data 0:30 · cap logic 1:15 · baselines and signal 2:10 · decision rule 2:35 · tests 2:55 · changed-input test 3:25 · reproduce 4:10 · failure mode 4:40.

---

## Video 3 — Live app demo, then investment-committee presentation (≤ 5:00)

**Required by the brief:** Video 3 **opens with your app running live**.

**Title:** `FIN439 Project 2 – Video 3 – Live Demo and Investment Committee: Energy Sleeve Pilot – Eric Boyd`

**Before recording:** in Terminal, run `cd ~/"Fin 439/Project 2"` and then `streamlit run app.py`. Have the app open in your browser, and `docs/decision-memo.md` (on GitHub, or the PDF) in a second window. Share your screen with the webcam on.

| Time | On screen | What to say / do |
|---|---|---|
| 0:00–0:10 | App, the blue box at the top | **The two statements.** They're shown on the app's banner. |
| 0:10–0:35 | App: sidebar "Mandate (as written)", then the verdict table | "This is the committee app. My mandate: five energy ETFs, equal-weight benchmark, volatility as the risk measure, 8% objective, no fund above 40%. Here's my constrained portfolio, **XLE 15, AMLP 40, ICLN 25, NLR 20**, beside two baselines, equal weight and inverse volatility. All three **pass** the mandate." |
| 0:35–0:55 | Drag **Search cap to 100%** | "Remove the cap from the search and it puts **70% in AMLP**, and the verdict turns to **FAIL: no fund above 40%**. That was my original Lab 15 answer." Drag it back to 40%. |
| 0:55–1:15 | **Signal slider** → 2022-10, then back to 2026-09 | "My point-in-time risk signal: trailing 12-month volatility, using only prices known at that month-end. In October 2022 it read 26%, which is REVIEW. Today it's 17.8%, OK." |
| 1:15–1:35 | Memo §1 | "**My recommendation: PILOT.** Run a 12-month paper portfolio with **no capital**. I'm asking the committee to approve the pilot, confirm the mandate, and agree the adopt/reject triggers now." |
| 1:35–2:15 | Memo §2 and §3 tables | "Why not adopt? This strategy's job is lower risk. Out of sample it earned 15.9% a year, but volatility was 18.6% against 16.0% for equal weight, and the drawdown was worse: −15.0% against −12.9%. Even inverse volatility was less risky. I fixed the decision rule before that test. It failed both risk conditions. My locked 30%-cap test didn't fix it either." |
| 2:15–2:40 | Memo §3 | "Why not reject? In sample it's about 2 points less volatile than equal weight, it passes every mandate check, and it has 7 points of slack over 8%." |
| 2:40–3:25 | Memo §4 | "Treat this as a range: XLE 5–25%, ICLN 15–35%, NLR 10–30%, with AMLP pinned at 40%, from 200 bootstrap re-estimates. Return estimates are noisy: about 12 points of standard error on XLE. The stress run says **the cap matters**: without it, out-of-sample volatility hits 29%. Costs don't matter at annual rebalancing." |
| 3:25–4:00 | Memo §5, risks | "Risks: three oil-linked funds with 0.8 to 0.9 correlation, a history dominated by the 2022 spike, risk estimates that didn't hold out of sample, and taxes and capacity not modelled." |
| 4:00–4:35 | Memo §5, triggers and stop condition | "**Stop condition:** reject if the paper portfolio draws down more than 25%, or the re-estimated mix can't reach 8%. **Pause** if the risk signal hits 25%. At 12 months, **adopt** only if volatility and drawdown are both no worse than equal weight's. Otherwise reject, or switch to the inverse-volatility baseline." |
| 4:35–4:55 | Memo §1 | "So the ask: approve a no-capital 12-month pilot, confirm the mandate, and pre-commit to those triggers." |

**Timestamp index:** statements 0:00 · live demo and verdicts 0:10 · cap stress in app 0:35 · signal 0:55 · decision and ask 1:15 · vs adopt 1:35 · vs reject 2:15 · range and stress 2:40 · risks 3:25 · stop condition and triggers 4:00 · ask 4:35.

**Practise one skeptical question:** *"If it beat equal weight on return, why not just adopt?"* Answer: "Return wasn't the claim. Lower risk was, and it failed. A 36-month return edge in one energy regime is inside the noise: the standard errors are about 8 to 13 points."
