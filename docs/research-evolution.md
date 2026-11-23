# Research Evolution — Energy Satellite Sleeve (Project 2)

**Student:** Eric Boyd · FIN 43900 Fall 2026

## Part 1 — Edition A (unchanged)

> **Insert your original Edition A PDF here, exactly as submitted to the Brightspace Project 2 Edition A checkpoint.** Do not retype or edit it. When you make the final PDF, put your Edition A pages first (see `submission/HOW-TO-ASSEMBLE.md`).
>
> Receipt / attempt ID: ________ · Submitted (timestamp): ________
>
> **Dated addendum (only if needed):** if a fact in Edition A was wrong, add a dated correction here. Example: *"2026-11-23: Edition A listed … ; the correct value is …"* If project-specific AI was used before your receipt, disclose it here (tool, approximate date, affected part), per the AI Boundary Card.

## Part 2 — Edition B (after project-specific research and AI assistance)

**Decision and intended user.** The investment committee of a client deciding whether to fund an energy satellite sleeve must choose: **adopt, pilot or reject** a long-only mix of XLE, XOP, AMLP, ICLN and NLR. I'm the portfolio analyst.

**Current position: PILOT.** Run a 12-month paper portfolio with no capital, at XLE 15 / XOP 0 / AMLP 40 / ICLN 25 / NLR 20. The tolerance range is XLE 5–25 / AMLP 40 / ICLN 15–35 / NLR 10–30. The decision follows a rule written into the code before the out-of-sample test was run.

**Mandate:**
- expected return ≥ 8%
- no fund above 40%
- long-only and fully invested
- annual rebalancing
- 10 bps one-way cost (assumption)

The 8% target and the cap are working assumptions that the committee must confirm.

**Evidence now (data as of 2026-09-30, 60 monthly returns):**
- **In sample:** the capped mix has 17.14% volatility, versus 19.25% for equal weight. All four mandate checks pass.
- **Out of sample** (mix chosen on Oct 2021–Sep 2023, tested Oct 2023–Sep 2026, net of costs): the strategy earned 15.86% a year, but its volatility was 18.55% versus 15.97% for equal weight, and its maximum drawdown was −15.02% versus −12.88%.
- The "lowest-risk" method was **not** lower-risk out of sample.

**Most consequential assumptions:**
1. Historical means are usable as expected returns. They have standard errors of ±8 to ±13 points.
2. Five years of volatility and correlations describe the future. This failed in the holdout.
3. The 40% cap is binding: AMLP sits at the cap in every window and bootstrap draw.

**What remains unknown:**
- whether the risk advantage reappears outside the 2022–2026 energy regime
- taxes on MLP exposure
- capacity and liquidity
- the client's real loss tolerance

**Validation plan from here:** the 12-month paper pilot, with the triggers in the memo. Adoption requires the paper portfolio's volatility *and* drawdown to be no worse than equal weight's.

### A-to-B change table

Fill the **Edition A** column from your actual Edition A. If Edition A already said the same thing, write **"No material change"** in the Edition B column and keep the evidence cell.

| Changed item | Edition A | Edition B | Primary driver of change | Evidence or test that justified the change |
|---|---|---|---|---|
| Thesis / recommendation | [your Edition A position] | PILOT (no capital, 12 months); adopt only if out-of-sample risk ≤ equal weight | Mixed: own analysis + AI-built holdout | Holdout: volatility 18.55% vs 15.97%, drawdown −15.02% vs −12.88% (Validation §4); rule fixed before the run (§9) |
| Data / source choice | [your Edition A data plan] | Yahoo monthly Adj Close, 60 returns, SHA-256-pinned; first 24 months to choose, last 36 to test | Course instruction (point-in-time, holdout: Weeks 10–12) + AI | `data/DATA-SOURCE.md`; holdout-isolation unit test |
| Assumption / model design | [your Edition A method] | The 40% cap is enforced inside the search; annual rebalancing and costs are modelled | Own analysis (Lab 15 found the 70% AMLP breach) | Uncapped mix fails the mandate check; capped mix reproduces Lab 15 to 6 decimals |
| Risk, limitation or uncertainty | [your Edition A risks] | Return estimates are ±8 to ±13 points; risk estimates unstable out of sample; oil concentration (ρ 0.79–0.93) | AI-proposed tests, independently checked | Standard errors, bootstrap (8% reproduce the target), window sensitivity (Validation §6) |

### What changed from Edition A to Edition B, and why?

[Write 3–5 sentences in your own words, built from the table above. Name the single most consequential change, what drove it (course, own analysis, peer, AI or mixed), and the specific test that justified it. Suggested anchor: *"The strategy's selling point was lower risk, and the out-of-sample test showed it was riskier than equal weight (18.55% vs 15.97% volatility). That evidence moved me from ___ to a no-capital pilot."*]
