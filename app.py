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

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")

uploaded = st.file_uploader("Upload CSV", type=["csv"])
show_preview = st.checkbox("Show preview", value=True)

if "report" not in st.session_state:
    st.session_state["report"] = None

if "show_json_table" not in st.session_state:
    st.session_state["show_json_table"] = False

if uploaded is not None:
    text = uploaded.getvalue().decode("utf-8-sig")
    rows = list(csv.DictReader(StringIO(text)))
    df = pd.DataFrame(rows)

    st.markdown(f"**Filename:** {uploaded.name}")
    st.markdown(f"**Rows loaded:** {len(df)}")

    if st.button("Generate report"):
        st.session_state["report"] = profile_rows(rows)
        st.session_state["show_json_table"] = False

    if st.session_state["report"] is not None:
        if show_preview:
            st.subheader("Data Preview")
            st.dataframe(df)

        if st.button("Show .json"):
            st.session_state["show_json_table"] = True

        if st.session_state["show_json_table"]:
            st.subheader("Report (Table)")

            report = st.session_state["report"]
            table_df = pd.DataFrame.from_dict(report["columns"], orient="index")
            table_df = table_df.reset_index().rename(columns={"index": "column"})

            st.dataframe(table_df)

        report = st.session_state["report"]
        json_text = json.dumps(report, indent=2, ensure_ascii=False)
        md_text = render_markdown(report)

        l, r = st.columns(2)
        l.download_button("Download JSON", data=json_text, file_name="report.json")
        r.download_button("Download Markdown", data=md_text, file_name="report.md")
else:
    st.info("Upload a CSV to begin.")