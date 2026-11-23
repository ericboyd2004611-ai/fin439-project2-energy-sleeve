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

[WRITE YOUR PREDICTION HERE — replace this whole bracket. In your own words, answer each item:
 1. Expected direction of the weights: which funds gain and which lose, and roughly how much?
 2. Expected direction of the portfolio's expected return and volatility, and why, in finance terms.
 3. Will the mandate still pass? Will the holdout return go up or down?
 4. Expected decision effect: does PILOT stay PILOT? What would make it change?
 5. Date and time you wrote this.]

## Step 3 — lock it

```sh
git add docs/locked-changed-input-record.md docs/locked-changed-input.json
git commit -m "Lock changed-input prediction (AI off)"
git push
```

Lock commit (fill in after committing): `__________________`   Timestamp: `__________________`

## Step 4 — run (AI closed)

```sh
python changed_input.py
```

The script refuses to run if the prediction is still this placeholder, or if the prediction, config, `portfolio.py` or `data/prices.csv` differ from a commit. It writes `output/changed-input-result.json` and prints a table.

## Step 5 — actual results (paste the printed table here)

| Result | Before | After |
|---|---|---|
| | | |

## Step 6 — reconciliation and diagnosis (your words)

- Prediction vs actual for each item in Step 2: matched / partly / missed.
- Actual decision effect.
- If something diverged: why? (Example: a binding cap redistributes weight to the next-lowest-risk funds, which changes volatility nonlinearly through the correlations.)
- What this means for the committee recommendation.

Then commit the filled-in record and `output/changed-input-result.json`, and copy this section into `docs/validation-and-ai-use.md` before making the PDF.
