"""Rebuild the Brightspace PDFs from the Markdown sources.   Run:  python3 submission/build_pdfs.py
Needs pandoc and wkhtmltopdf on PATH. Writes submission/*.pdf and copies them into docs/."""
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = """body{font-family:Helvetica,Arial,sans-serif;font-size:11pt;line-height:1.35;color:#111}
h1{font-size:16pt;margin:0 0 6px}h2{font-size:12.5pt;margin:12px 0 4px;border-bottom:1px solid #ccc}
h3{font-size:11.5pt;margin:10px 0 4px}table{border-collapse:collapse;width:100%;margin:6px 0;font-size:9.5pt}
th,td{border:1px solid #bbb;padding:3px 5px;vertical-align:top}th{background:#f0efec}
code{font-size:9pt;background:#f4f4f4}pre{font-size:8.5pt;background:#f4f4f4;padding:6px}
blockquote{border-left:3px solid #ccc;margin:6px 0;padding:2px 10px;color:#333}p,li{margin:3px 0}"""
JOBS = [("docs/decision-memo.md", "Decision-Memo.pdf", "decision-memo.pdf"),
        ("docs/validation-and-ai-use.md", "Validation-and-AI-Use.pdf", "validation-and-ai-use.pdf"),
        ("docs/research-evolution.md", "Research-Evolution-EditionB-only.pdf", None),
        ("output/visible-output.md", "Visible-Output.pdf", None)]


LOCKED_MARKER = "[Paste the completed `docs/locked-changed-input-record.md` here"


def source_text(src):
    """Validation record: insert the Locked Changed-Input Record into section 10 so they always match."""
    text = (ROOT / src).read_text()
    if src.endswith("validation-and-ai-use.md") and LOCKED_MARKER in text:
        record = (ROOT / "docs" / "locked-changed-input-record.md").read_text()
        record = "\n".join(l for l in record.splitlines() if not l.startswith("# "))
        record = record.replace("\n## ", "\n### ")
        start = text.index(LOCKED_MARKER)
        end = text.index("]", text.index("reconciliation and diagnosis", start)) + 1
        text = text[:start] + "Full record from `docs/locked-changed-input-record.md` (inserted at PDF build):\n" + record + text[end:]
    return text


def main():
    with tempfile.TemporaryDirectory() as tmp:
        css = Path(tmp) / "style.css"
        css.write_text(CSS)
        for src, out, docs_copy in JOBS:
            html = Path(tmp) / "page.html"
            md = Path(tmp) / "page.md"
            md.write_text(source_text(src))
            subprocess.run(["pandoc", str(md), "-s", "--metadata", f"title={Path(src).stem}",
                            "-V", "title=", "--css", str(css), "--embed-resources", "-o", str(html)], check=True)
            pdf = ROOT / "submission" / out
            subprocess.run(["wkhtmltopdf", "--quiet", "--enable-local-file-access", "-s", "Letter",
                            "-T", "14mm", "-B", "14mm", "-L", "16mm", "-R", "16mm", str(html), str(pdf)], check=True)
            if docs_copy:
                shutil.copy(pdf, ROOT / "docs" / docs_copy)
            print("wrote", pdf.relative_to(ROOT))


if __name__ == "__main__":
    main()
