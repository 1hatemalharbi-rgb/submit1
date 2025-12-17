from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime


def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")


def render_markdown(report: dict) -> str:
    lines: list[str] = []

    lines.append("# CSV Profiling Report\n")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n")

    lines.append("## Summary\n")
    lines.append(f"- Rows: **{report.get('rows', 0)}**")
    lines.append(f"- Columns: **{report.get('n_cols', 0)}**\n")

    lines.append("## Columns\n")
    lines.append("| name | type | missing | missing_pct | unique |")
    lines.append("|---|---|---:|---:|---:|")

    n_rows = report.get("rows", 0) or 0
    for name, col in report.get("columns", {}).items():
        missing = col.get("missing", 0)
        missing_pct = (missing / n_rows * 100) if n_rows else 0.0
        unique = col.get("unique", 0)
        lines.append(
            f"| {name} | {col.get('type','')} | {missing} | {missing_pct:.1f}% | {unique} |"
        )

    lines.append("\n## Notes\n")
    lines.append("- Missing values are: `''`, `na`, `n/a`, `null`, `none`, `nan` (case-insensitive)")

    return "\n".join(lines)


def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(report))
