from __future__ import annotations
import json
from pathlib import Path

def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []

    lines.append("# CSV Profile Report\n")
    lines.append(f"- Rows: **{report.get('rows', 0)}**")
    lines.append(f"- Columns: **{report.get('n_cols', 0)}**\n")
    lines.append("## Columns\n")

    for name, col in report.get("columns", {}).items():
        lines.append(f"### {name}")
        lines.append(f"- Type: `{col['type']}`")
        lines.append(f"- Missing: {col['missing']}")

        # Numeric columns
        if col['type'] == "number":
            lines.append(f"- Count: {col['count']}")
            lines.append(f"- Unique: {col['unique']}")
            lines.append(f"- Min: {col['min']}")
            lines.append(f"- Max: {col['max']}")
            lines.append(f"- Mean: {col['mean']:.2f}" if col['mean'] is not None else "- Mean: None")

        # Text columns
        if col['type'] == "text":
            lines.append(f"- Count: {col['count']}")
            lines.append(f"- Unique: {col['unique']}")
            if col.get("top"):
                lines.append("- Top values:")
                for item in col["top"]:
                    lines.append(f"  - {item['value']}: {item['count']}")

        lines.append("")

    path.write_text("\n".join(lines))