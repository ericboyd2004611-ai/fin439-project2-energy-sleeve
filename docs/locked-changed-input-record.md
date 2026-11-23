# Locked Changed-Input Record

**Course rule:** the prediction below must be written by the student, **with AI off, before the run**. The run itself is AI-closed. Claude prepared this template and the runner (`changed_input.py`) but did **not** write or see the prediction.

## Step 1 — the input you will change (also set in `docs/locked-changed-input.json`)

| Field | Value |
|---|---|
| Input | Single-fund cap, `MAX_WEIGHT` (suggested; any supported input in `changed_input.py` works) |
| Old value (units) | 0.40 (40% of the sleeve) |
| New value (units) | 0.30 (30% of the sleeve) |
| Why this input is material | The cap is binding: AMLP sits at exactly 40% in every window and in the 10th–90th percentile of the bootstrap. A tighter cap tests the highest-risk claim, that the cap-constrained mix is a stable, lower-risk answer. |

If you choose a different input, edit both this table and the JSON before you commit.

## Step 2 — your prediction (AI off, before running)

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

## Step 3 — lock it

```sh
git add docs/locked-changed-input-record.md docs/locked-changed-input.json
git commit -m "Lock changed-input prediction (AI off)"
git push
```

Lock commit: `89ab3f9b056eea3e2e45621f5b5966b6225b9ae5`   Timestamp: `2026-11-23T16:36:36-05:00` (committed on GitHub)

## Step 4 — run (AI closed)

```sh
python changed_input.py
```

The script refuses to run if the prediction is still this placeholder, or if the prediction, config, `portfolio.py` or `data/prices.csv` differ from a commit. It writes `output/changed-input-result.json` and prints a table.

## Step 5 — actual results (paste the printed table here)

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

## Step 6 — reconciliation and diagnosis (your words)

- Prediction vs actual for each item in Step 2: matched / partly / missed.
- Actual decision effect.
- If something diverged: why? (Example: a binding cap redistributes weight to the next-lowest-risk funds, which changes volatility nonlinearly through the correlations.)
- What this means for the committee recommendation.

Then commit the filled-in record and `output/changed-input-result.json`, and copy this section into `docs/validation-and-ai-use.md` before making the PDF.
