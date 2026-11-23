"""Mechanical Project 2 package audit (course starter, Week 12), pointed at this repo's manifest.
Run:  python submission/project2_audit.py      -> prints required rows still missing fields.
Needs pandas (pip install pandas). Completeness only; it cannot judge quality or authorship."""
from __future__ import annotations
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {"item", "required", "location_or_url", "title", "duration_or_as_of",
                    "timestamp_index", "access_checked", "frozen_or_commit_id", "notes"}
VIDEO_ITEMS = {"Video 1", "Video 2", "Video 3"}


def load(path):
    frame = pd.read_csv(path, keep_default_na=False)
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if len(frame) != 12:
        raise ValueError(f"Expected 12 manifest rows; received {len(frame)}")
    return frame


def gaps(frame):
    out = []
    for row in frame.to_dict(orient="records"):
        if row["required"].lower() != "yes":
            continue
        base = all(row[f].strip() and "<" not in row[f] for f in ("location_or_url", "access_checked", "frozen_or_commit_id"))
        video = row["item"] not in VIDEO_ITEMS or all(row[f].strip() for f in ("title", "duration_or_as_of", "timestamp_index"))
        if not (base and video):
            out.append(row["item"])
    return out


if __name__ == "__main__":
    missing = gaps(load(Path(__file__).with_name("project2-manifest.csv")))
    print("All required rows complete." if not missing else "Still missing:\n- " + "\n- ".join(missing))
