# Finish and submit — Project 2 checklist (updated 2026-11-23)

**Project 2 has no Edition A or B** (course owner ruling 2026-10-14). The Research-Evolution row is marked "not required" in the manifest.

## Done ✅
- [x] Repo on GitHub (private): https://github.com/ericboyd2004611-ai/fin439-project2-energy-sleeve
- [x] Locked Changed-Input Record: prediction committed 16:36:36, run 16:37:13, reconciliation written
- [x] Decision memo, validation record, README, visible output, tests

## Left to do
1. **Give the instructors repo access.** GitHub → Settings → Collaborators → add the instructional team's GitHub username (from the Brightspace Project 2 page).
2. **Fill the remaining `____` blanks** in `docs/validation-and-ai-use.md`:
   - §7: your own Mac cold run (`python3 analysis.py`, `python3 -m unittest discover -s tests`)
   - §11: the "Student edits" and "Student review" lines
3. **Record the 3 videos** using `docs/video-scripts.md`. Upload each as **Unlisted** on YouTube.
4. **Transcripts.** Download each video's YouTube captions, correct the tickers, terms and numbers, and save them over `docs/transcript-video-1.txt`, `-2.txt` and `-3.txt`.
5. **Manifest** (`submission/project2-manifest.csv`): fill in the YouTube URLs, real durations and timestamps, `access_checked`, and `frozen_or_commit_id` (final `git rev-parse HEAD`, or the YouTube video ID). Check it with `python3 submission/project2_audit.py`.
6. **Commit and push everything.**

## Upload to Brightspace (6 files)
1. `submission/project2-manifest.csv`
2. `submission/Decision-Memo.pdf`
3. `submission/Validation-and-AI-Use.pdf`
4. `docs/transcript-video-1.txt`
5. `docs/transcript-video-2.txt`
6. `docs/transcript-video-3.txt`

The repo URL and the 3 video links go **inside** the manifest. The Brightspace assignment page is the final authority if it lists anything different.
