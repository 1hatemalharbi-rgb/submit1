from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_json, write_markdown
from pathlib import Path

def main() -> None:
    csv_path = Path("csv-profiler/data/sample.csv")
    rows = read_csv_rows(csv_path)
    report = basic_profile(rows)
    write_json(report, "outputs/report.json")
    write_markdown(report, "outputs/report.md")
    print("Wrote outputs/report.json and outputs/report.md")

if __name__ == "__main__":
    main()