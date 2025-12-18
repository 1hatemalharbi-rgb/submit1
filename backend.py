from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import csv
from io import StringIO
from pathlib import Path
import sys

# ---- FIXED PATH FOR YOUR STRUCTURE ----
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR / "csv-profiler" / "src"))

from csv_profiler.profile import basic_profile as profile_rows
from csv_profiler.render import render_markdown

app = FastAPI()

class CSVIn(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "backend running"}

@app.post("/profile")
def profile_csv(data: CSVIn):
    if data.text is None or data.text.strip() == "":
        raise HTTPException(status_code=400, detail="Empty CSV")

    try:
        reader = csv.DictReader(StringIO(data.text))
        if not reader.fieldnames:
            raise HTTPException(status_code=400, detail="No header row found")
        rows = list(reader)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV format")

    if len(rows) == 0:
        raise HTTPException(status_code=400, detail="No data rows")

    try:
        report = profile_rows(rows)
        md = render_markdown(report)
    except Exception:
        raise HTTPException(status_code=500, detail="Profiler failed")

    return {
        "report": report,
        "markdown": md
    }
