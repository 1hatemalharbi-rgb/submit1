import requests
import csv
from io import StringIO
import pandas as pd
import streamlit as st

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "csv-profiler" / "src"))
from csv_profiler.profile import basic_profile as profile_rows

import json
from csv_profiler.render import render_markdown
import zipfile
import io

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")

# ---- backend API address (FastAPI) ----
API_URL = "http://127.0.0.1:8000/profile"

uploaded = st.file_uploader("Upload CSV", type=["csv"])

if "report" not in st.session_state:
    st.session_state["report"] = None

if "show_json" not in st.session_state:
    st.session_state["show_json"] = False

# store markdown returned by backend (optional)
if "md_text" not in st.session_state:
    st.session_state["md_text"] = None

if uploaded is not None:
    # --- basic file checks (common crash attempts) ---
    try:
        file_bytes = uploaded.getvalue()
    except Exception:
        st.error("Could not read the uploaded file.")
        st.stop()

    if len(file_bytes) == 0:
        st.error("This file is empty (0 bytes). Please upload a valid CSV.")
        st.stop()

    if len(file_bytes) > 5 * 1024 * 1024:  # 5 MB limit
        st.error("File is too large. Please upload a smaller CSV.")
        st.stop()

    # --- decode safely ---
    try:
        text = file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        st.error("Could not decode this file as UTF-8. Please re-save it as UTF-8 CSV.")
        st.stop()

    # --- parse safely ---
    try:
        reader = csv.DictReader(StringIO(text))
        if not reader.fieldnames or all(h.strip() == "" for h in reader.fieldnames if h is not None):
            st.error("No header row found. Your CSV needs column names in the first row.")
            st.stop()

        rows = list(reader)
    except Exception:
        st.error("CSV file looks invalid or is formatted incorrectly.")
        st.stop()

    # --- dataframe safely ---
    try:
        df = pd.DataFrame(rows)
    except Exception:
        st.error("Could not load this CSV into a table.")
        st.stop()

    st.markdown(f"**Filename:** {uploaded.name}")
    st.markdown(f"**Rows loaded:** {len(df)}")

    if st.button("Generate report"):
        # try backend first
        try:
            r = requests.post(API_URL, json={"text": text}, timeout=30)
            if r.status_code != 200:
                # backend returned a friendly error
                try:
                    st.error(r.json().get("detail", "Backend error"))
                except Exception:
                    st.error("Backend error")
                st.session_state["report"] = None
                st.session_state["md_text"] = None
            else:
                data = r.json()
                st.session_state["report"] = data.get("report")
                st.session_state["md_text"] = data.get("markdown")
                st.session_state["show_json"] = False

        except Exception:
            # backend not running -> fall back to your original local code
            try:
                st.session_state["report"] = profile_rows(rows)
                st.session_state["md_text"] = None
                st.session_state["show_json"] = False
            except Exception:
                st.error("Could not generate the report for this CSV.")
                st.session_state["report"] = None
                st.session_state["md_text"] = None

    if st.session_state["report"] is not None:
        report = st.session_state["report"]
        md_text = st.session_state.get("md_text")

        # ---- MARKDOWN DISPLAY (FIRST) ----
        st.subheader("Report (Markdown)")
        try:
            if md_text:
                st.markdown(md_text)
            else:
                st.markdown(render_markdown(report))
        except Exception:
            st.error("Could not render the report preview.")

        # ---- BUTTON TO SHOW RAW JSON ----
        if st.button("Show .json"):
            st.session_state["show_json"] = True

        if st.session_state["show_json"]:
            st.subheader("Report (JSON)")
            st.json(report)

        # ---- SINGLE DOWNLOAD BUTTON (ZIP) ----
        try:
            json_text = json.dumps(report, indent=2, ensure_ascii=False)

            if not md_text:
                md_text = render_markdown(report)

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as z:
                z.writestr("report.json", json_text)
                z.writestr("report.md", md_text)

            st.download_button(
                "Download Report (.zip)",
                data=zip_buffer.getvalue(),
                file_name="csv_profile_report.zip",
                mime="application/zip"
            )
        except Exception:
            st.error("Could not prepare the download file.")
else:
    st.info("Upload a CSV to begin.")