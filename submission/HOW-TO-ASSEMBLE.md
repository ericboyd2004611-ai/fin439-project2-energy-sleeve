# Finish and submit — Project 2 (matches the live Project 2 brief, updated 2026-11-23)

Source: `projects/project-2-investment-management-application.md` in the course repo. The Brightspace assignment page is the final word on the due time.

## Base requirements (all 8) ✅
1. The app runs from the README (`streamlit run app.py`)
2. The mandate: universe, benchmark, risk measure, objective, limits (README, memo, app sidebar)
3. Two baselines (equal weight and inverse volatility) beside the constrained portfolio, each with a pass/fail mandate verdict and the failed rule, **in the app**
4. One point-in-time signal with its data card (`data/SIGNAL-DATA-CARD.md`)
5. A stress run on estimates, window, costs and constraints, plus the stop condition
6. Locked Changed-Input Record: AI-off prediction committed before the run (commit `89ab3f9`)
7. Recommendation with an allocation range and triggers
8. The two opening statements (AI use; education, not advice) on the README, the memo and **each video**

## Left to do
1. **Commit and push** the latest changes.
2. **Instructor access:** GitHub → Settings → Collaborators → add the instructional team's username (from Brightspace).
3. **Fill the last blanks** in `docs/validation-and-ai-use.md`:
   - §7: your own Mac cold run
   - §11: "student edits" and "student review"
4. **Record the 3 videos** using `docs/video-scripts.md`:
   - Each video opens with the two statements.
   - Video 3 opens with the app running live.
   - Upload each as **Unlisted** with captions on.
5. **Transcripts:** correct each video's YouTube captions and save them as `docs/transcript-video-1.txt`, `-2.txt` and `-3.txt`. Push.
6. **Manifest:** paste the 3 YouTube links, actual durations and timestamps, `access_checked`, and the final commit ID into `submission/project2-manifest.csv`. Check it with `python3 submission/project2_audit.py`. Push.

## Upload to Brightspace (`.md` files, not PDFs)
1. `submission/project2-manifest.csv`
2. `docs/decision-memo.md`
3. `docs/validation-and-ai-use.md`
4. The 3 transcripts (`docs/transcript-video-1.txt`, `-2.txt` and `-3.txt`). Alternatively, the brief allows linking them from the repo; the manifest already links them.

The repo URL and the 3 YouTube links go inside the manifest.
