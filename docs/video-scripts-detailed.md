# Detailed Video Scripts — Project 2 (word for word, with every click)

**How to use this:**
- **[Brackets] = what to do on screen. Plain text = what to say.**
- Read it through twice, then speak it **in your own words, glancing at it**. Graders are checking that you understand it. Reading word for word in a flat voice works against you.
- Bracketed times are approximate. Spoken text is about 4:00 for Video 2, 4:25 for Video 3 and 2:45 for Video 1 at a normal pace, which leaves room for clicking. If you run long, cut the lines marked *(optional)*.
- **Webcam bubble on in every video.** Upload as **YouTube → Unlisted**, with captions on.

**Setup before any recording** (Terminal):

```sh
cd ~/"Fin 439/Project 2"
source .venv/bin/activate
```

Your prompt should show `(.venv)`.

---

# VIDEO 2 — Codebase walkthrough (limit 5:00; target about 4:40)

**Have open before you hit record:**
1. GitHub repo page: https://github.com/ericboyd2004611-ai/fin439-project2-energy-sleeve
2. Your code editor (VS Code) with the `Project 2` folder open
3. Terminal in the `Project 2` folder, with `(.venv)` showing

**Title:** `FIN439 Project 2 – Video 2 – Codebase Walkthrough – Eric Boyd`

---

**[0:00 — Webcam, GitHub repo page showing]**

> "Hi, I'm Eric Boyd, and this is Video 2 for my FIN 439 Project 2, the code walkthrough. Two statements first. I used Claude, from Anthropic, to write the code, run tests and draft documents at my direction, and the analysis and the decision are mine. And this is education, not investment advice."

**[0:20 — Scroll the GitHub README down to the "Repository map" table]**

> "Four Python files. `portfolio.py` holds all the finance math. `analysis.py` runs the study. `changed_input.py` runs my locked prediction test. `app.py` is the Streamlit app. The app and analysis import the math, so there's only one version of every calculation."

**[0:45 — Open `data/DATA-SOURCE.md` in the editor]**

> "The data: 61 month-end adjusted prices for five energy ETFs from Yahoo Finance, downloaded October 22nd, with the file's hash recorded so anyone can confirm it. Everything is as of September 30th, 2026."

**[1:05 — Open `portfolio.py`. Scroll to line 23]**

> "At the top of `portfolio.py` is the mandate: an 8% minimum expected return on line 23, and a 40% maximum in any one fund on line 24."

**[1:15 — Scroll to line 36, `read_prices`, then line 90, `estimate`]**

> "`read_prices` refuses bad data, like out-of-order dates or zero prices. `estimate` annualizes: average monthly return times 12, standard deviation times root 12, plus correlations."

**[1:35 — Scroll to line 177, `long_only_mixes`. Highlight line 184, `cap_units`]**

> "This is the fix for my Lab 15 mistake, where the app recommended 70% AMLP and broke my 40% cap. Now the cap is applied **while portfolios are generated**. Line 184 turns 40% into a maximum number of 5-point steps, so an over-cap portfolio can't even be created. That cuts 10,626 portfolios to 3,951, and every one clears 8%, so the return target never constrains the answer."

**[2:05 — Scroll to line 199, `lowest_risk_mix`, then line 164, `mandate_check`]**

> "`lowest_risk_mix` keeps the allowed portfolio with the lowest volatility. `mandate_check` tests each rule and names any that failed. That's the verdict in the app."

**[2:25 — Scroll to line 231 `equal_weights`, line 236 `inverse_volatility_weights`, then line 250 `risk_signal`]**

> "Two baselines: equal weight, which is also my benchmark, and inverse volatility. Then `risk_signal`, my point-in-time signal: trailing 12-month volatility. It only uses prices dated on or before the as-of month, so it can't see the future."

**[2:50 — Open `analysis.py`. Show lines 24–36, then scroll to lines 265–277]**

> "`analysis.py` sets up the out-of-sample test. The first 24 months choose the portfolio, and the last 36 months test it. The decision rule is written here, before I ran that test. Lines 265 to 277 apply it: adopt only if the portfolio beats equal weight on both volatility and drawdown out of sample. It didn't, so the output says PILOT."

**[3:10 — Switch to Terminal. Type and run:]**

```sh
python -m unittest discover -s tests -v
```

> "Twenty tests, including known answers I can do by hand, like a two-asset volatility and the 10,626 portfolio count. The test on line 84 triples every price after September 2023, and the September 2023 signal doesn't move, so it's truly point-in-time. All 20 pass."

**[3:40 — Open `docs/locked-changed-input-record.md` in the editor. Scroll to Step 2, then Step 5]**

> "This is my Locked Changed-Input Record, testing my highest-risk assumption, the 40% cap. With AI off, I predicted what would happen if the cap dropped to 30%. I committed that prediction at 4:36 PM, commit 89ab3f9, and only then ran the test. In the results, AMLP fell from 40 to 30, and all ten points went to XLE. I'd predicted XLE *and* NLR, because I reasoned from returns, but the search minimizes volatility. Volatility rose in sample but fell out of sample, and the decision stayed PILOT."

**[4:05 — In Terminal run:]**

```sh
python changed_input.py
```

> "Running it again just shows the saved, locked result. It never overwrites the evidence."

**[*(optional, cut if long)* In the editor, add one letter to the record and save. In Terminal run `python changed_input.py --rerun`. It prints "Refusing to run… uncommitted edits". Then undo the edit:]**

```sh
git checkout docs/locked-changed-input-record.md
```

> "And it refuses to recompute if the prediction has been touched since it was committed."

**[4:20 — Open `docs/validation-and-ai-use.md`, section 8]**

> "To reproduce: create a virtual environment, install the requirements, run `python analysis.py`. My clean runs produced identical outputs. The main unresolved risk: the volatility estimates the search depends on didn't hold up out of sample. That's why this is a pilot, not an adoption."

**[4:40 — Stop recording]**

---

# VIDEO 3 — Live demo, then investment committee (limit 5:00; target about 4:45)

**Have open before you hit record:**
1. Terminal: `streamlit run app.py`, with the app open in your browser at the top of the page
2. `docs/decision-memo.md` on GitHub, in a second browser tab
3. In the app: search cap at **40**, signal slider at **2026-09**, window **All 60 months**

**Title:** `FIN439 Project 2 – Video 3 – Live Demo and Investment Committee: Energy Sleeve Pilot – Eric Boyd`

---

**[0:00 — Webcam, app showing with the blue banner at the top]**

> "Hi, I'm Eric Boyd, presenting my energy-sleeve recommendation to the investment committee. Two statements, which are also on the app's banner: I used Claude, from Anthropic, to build this at my direction, and the analysis and the decision are mine. This is education, not investment advice. I'll start with the app running live."

**[0:15 — Point at the left sidebar, "Mandate (as written)"]**

> "Here's the mandate. The universe is five energy ETFs: XLE, XOP, AMLP, ICLN and NLR. The benchmark is equal weight, the risk measure is volatility, and the objective is at least 8% expected return, with no fund above 40%."

**[0:30 — Point at the verdict table]**

> "This table is the core of the app. My constrained portfolio is XLE 15%, AMLP 40%, ICLN 25% and NLR 20%, the lowest-volatility mix that meets the mandate. Beside it are two baselines, equal weight and inverse volatility. All three pass the mandate."

**[0:45 — Drag "Search cap" in the sidebar to 100. Wait for the table to update. Point at the FAIL]**

> "Watch what happens if I remove the cap from the search. It puts 70% in AMLP, and the verdict turns to **FAIL: no fund above 40%**. That was my original answer in Lab 15. The app now catches it."

**[1:00 — Drag "Search cap" back to 40. Scroll to "Point-in-time risk signal". Move the slider to 2022-10]**

> "This is my point-in-time risk signal: the portfolio's volatility over the last 12 months, using only prices known at that month-end. In October 2022, during the energy spike, it read 26%, which flags REVIEW."

**[1:12 — Move the slider back to 2026-09]**

> "Today it reads 17.8%, which is OK."

**[1:20 — Switch to the memo tab, section 1]**

> "**My recommendation is PILOT.** Run this as a 12-month paper portfolio with no capital. I'm asking the committee for three things: approve the pilot, confirm the mandate, and agree now on the triggers that decide adopt or reject."

**[1:35 — Scroll to section 2, the four-condition table]**

> "Why not adopt? This strategy's whole purpose is lower risk. I tested it out of sample: I chose the mix using 2021 to 2023 only, then measured October 2023 to September 2026. It earned 15.9% a year after costs, which beats the 8% target. But its volatility was 18.6% against 16.0% for simple equal weight, and its worst drawdown was minus 15.0% against minus 12.9%. I wrote the decision rule before running that test, and it failed both risk conditions."

**[2:05 — Scroll to section 3, the portfolio and baselines table]**

> "Even the inverse-volatility baseline was less risky out of sample than my optimized mix. That makes it the natural fallback if the pilot fails."

**[2:15]**

> "Why not reject outright? In sample it's about two points less volatile than equal weight, it passes every mandate rule, and it has seven points of slack over the 8% target."

**[2:30 — Scroll to section 4, the assumptions table]**

> "I'm giving a range, not a single answer. From 200 bootstrap re-estimates: XLE 5 to 25%, ICLN 15 to 35%, NLR 10 to 30%, with AMLP pinned at 40%. The return estimates are noisy: XLE's 24% has a standard error of about 12 points. The stress test shows the cap really matters. Without it, out-of-sample volatility hits 29%. Trading costs don't matter at annual rebalancing: even 50 basis points barely moves the return."

**[3:10 — Scroll to section 5, Principal risks]**

> "The main risks: three of the five funds are oil-linked and move together, with correlations around 0.8 to 0.9. The history is dominated by the 2022 oil spike. The risk estimates didn't hold up out of sample. And taxes on the MLP exposure and capacity aren't modelled yet."

**[3:35 — Scroll to the triggers table and the Stop condition]**

> "Here's what would change my recommendation. The stop condition: reject if the paper portfolio falls more than 25% from its peak, or if the re-estimated mix can no longer reach 8%. Pause and review if the risk signal hits 25%. Rebalance early if any fund drifts above 45%. And at 12 months, adopt only if the pilot's volatility *and* drawdown are both no worse than equal weight's. Otherwise reject, or switch to the inverse-volatility baseline."

**[4:15 — Scroll back to section 1]**

> "So my ask to the committee: approve a no-capital, 12-month pilot, confirm the 8% objective and 40% cap, and pre-commit to these triggers today, so the decision in twelve months is already made by the evidence. Thank you."

**[4:35 — Stop recording]**

---

# VIDEO 1 — How the system and my thinking changed, plus an AI check (limit 3:00; target about 2:50)

**Have open before you hit record:**
1. `Fin 439/Lab 15/Lab 15.md` (your old Lab 15 write-up), at the top
2. `output/visible-output.md` on GitHub, scrolled to "Out-of-sample holdout"
3. `docs/validation-and-ai-use.md` on GitHub, section 11 (the AI table)
4. `docs/locked-changed-input-record.md` on GitHub

**Title:** `FIN439 Project 2 – Video 1 – How the System Changed and AI Check – Eric Boyd`

---

**[0:00 — Webcam, Lab 15.md showing]**

> "Hi, I'm Eric Boyd. This is Video 1 for Project 2: how my system and my thinking changed, plus one AI output I checked. I used Claude, from Anthropic, to write code and draft documents at my direction, and the analysis and the decision are mine. This is education, not investment advice."

**[0:15 — Point at the Lab 15 "Answer" section]**

> "Here's where I started, in Lab 15. My app said the lowest-risk energy portfolio was 70% AMLP, 20% ICLN and 10% NLR. It said that answer survived every one-point change in the return estimates, so I treated it as stable."

**[0:30 — Scroll to "Mandate check the app does not do"]**

> "**The first change was to the system.** That 70% AMLP answer broke my own rule of no fund above 40%, because the app never checked it. So I moved the cap inside the search, and now every portfolio gets a pass or fail verdict. The answer became XLE 15, AMLP 40, ICLN 25, NLR 20. That change came from my own analysis of the Lab 15 output."

**[0:55 — Switch to `visible-output.md`, the holdout table]**

> "**The second change was to my thinking.** I'd been calling this the lower-risk portfolio, so I tested it on data it had never seen. I chose the mix using 2021 to 2023, then tested it on the next three years. It earned 15.9% a year, but it was **riskier** than equal weight: 18.6% volatility versus 16.0%, and a worse drawdown. So I moved from 'adopt' to 'pilot with no money.' The driver was mixed: the course taught the holdout, and AI helped build the test."

**[1:35 — Switch to `validation-and-ai-use.md` §11. Point at the row "Claimed the energy mix survives every one-point return change"]**

> "Now the AI output I checked. In Lab 15 the AI told me this mix 'survives every one-point return change.' I ran an objective sweep and found it survives only because the 8% target never binds: all 3,951 allowed portfolios clear 8%. I **qualified** that claim: stable, but for the wrong reason. And the AI's label of 'lowest-risk' I **rejected** as a reason to invest, because the out-of-sample test contradicted it."

**[2:15 — Switch to `locked-changed-input-record.md`, Steps 2 and 6]**

> "I also tested myself with AI off. I predicted that tightening the cap from 40 to 30% would move weight to XLE *and* NLR. It all went to XLE. I was thinking about returns, but the search minimizes volatility. So that was partly right, and the decision stayed PILOT."

**[2:40]**

> "So the system now enforces the mandate, and my recommendation follows the out-of-sample evidence instead of the in-sample label."

**[2:50 — Stop recording]**

---

## After each video
1. Upload to YouTube as **Unlisted** with the title above.
2. YouTube Studio → Subtitles → let the auto-captions generate (this can take a few minutes) → download the `.txt` or `.srt` → correct tickers, numbers and names → save as `docs/transcript-video-N.txt`.
3. Send me the link and the actual length. I'll update the manifest timestamps.
