# Finish and submit — what's left (all of it yours to do)

Everything else is built and tested. Approximate time for each step is in brackets; these are estimates.

## 1. Put the repo on GitHub [10 min]

Run in Terminal on your Mac:

```sh
cd ~/"Fin 439/Project 2"
git log --oneline        # the initial commit is already here
```

Then:
1. On github.com create a **private** repo, e.g. `fin439-project2-energy-sleeve`. Don't add a README; it's already in the folder.
2. Connect and push:
   ```sh
   git remote add origin https://github.com/ericboyd2004611-ai/fin439-project2-energy-sleeve.git
   git push -u origin main
   ```
3. Repo → Settings → Collaborators → add the instructional-team GitHub username from the Brightspace assignment page.
4. Open the repo URL in a private or incognito window to confirm the access setting.

## 2. Edition A [5 min]

1. Download your Edition A PDF and receipt from the Brightspace checkpoint.
2. Fill the Edition A column of the change table in `docs/research-evolution.md`, and write the closing "What changed…and why?" paragraph **in your own words**.
3. If you used project-specific AI (for example in Lab 15 on Oct 22) **before** your Edition A receipt, disclose it in the addendum. Don't hide it.

## 3. Locked Changed-Input Record [15 min, AI OFF]

1. Close Claude and any other AI tools.
2. Open `docs/locked-changed-input-record.md`. Replace the bracketed placeholder with your own prediction.
3. Run:
   ```sh
   git add docs/locked-changed-input-record.md docs/locked-changed-input.json
   git commit -m "Lock changed-input prediction (AI off)" && git push
   python3 changed_input.py
   ```
4. Paste the printed table into Step 5 of the record and write your reconciliation (Step 6).
5. Copy the completed record into `docs/validation-and-ai-use.md` §10.
6. Commit again.

## 4. Fill the remaining blanks [10 min]

- `docs/validation-and-ai-use.md`:
  - §7: your own Mac cold run
  - §11: Edition A date and receipt, your edits, your review
- Read the memo once. Change anything you wouldn't say yourself.

## 5. Rebuild the PDFs [2 min]

```sh
python3 submission/build_pdfs.py
```

This needs `pandoc` and `wkhtmltopdf`. If you don't have them, open each `.md` in VS Code or Typora and use Export to PDF.

For **Research-Evolution.pdf**, put the Edition A PDF pages **first**, then the Edition B PDF. On a Mac: open both in Preview, drag the pages together, and save. Save a copy as `docs/research-evolution.pdf`.

## 6. Record the 3 videos [45–60 min]

1. Follow `docs/video-scripts.md`. Upload each video as **Unlisted**.
2. Download each video's captions, correct them, and save them over `docs/transcript-video-1.txt`, `-2.txt` and `-3.txt`.
3. Commit and push.

## 7. Manifest and upload [10 min]

1. Fill `submission/project2-manifest.csv`:
   - URLs, real durations and timestamps
   - `access_checked` (e.g. "logged-out 11/23 9pm OK")
   - `frozen_or_commit_id`: the final `git rev-parse HEAD`, or the YouTube video ID
2. Run `python3 submission/project2_audit.py` until it says complete.
3. Upload to Brightspace:
   - the manifest
   - `Research-Evolution.pdf`
   - `Decision-Memo.pdf`
   - `Validation-and-AI-Use.pdf`
   - the 3 transcript `.txt` files
4. Save the receipt.

## Cold-check list (from the course checklist)

- [ ] A clean user can follow the README
- [ ] Repo and every video open logged-out
- [ ] Visible output shows the inputs, as-of date and decision
- [ ] Memo, output, transcripts and validation record use the same numbers
- [ ] No `.env`, keys or private data committed
- [ ] Every recommendation has a condition, a reversal trigger and a committee ask
