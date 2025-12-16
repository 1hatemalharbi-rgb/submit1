from __future__ import annotations

from csv import DictReader
from pathlib import Path
from typing import List, Dict


def read_csv_rows(file_path: str | Path) -> List[Dict[str, str]]:
    """Read a CSV file and return a list of row dictionaries.

    Normalizes each row to a plain `dict` with string values.
    """
    path = Path(file_path)
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = DictReader(f)
        return [dict(row) for row in reader]