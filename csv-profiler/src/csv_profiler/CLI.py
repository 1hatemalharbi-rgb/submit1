import typer
from csv_profiler.main import run as run_profiler

app = typer.Typer(help="CSV Profiler CLI")

@app.command()
def run(csv_path: str = "csv-profiler/data/sample.csv"):

    run_profiler(csv_path)

if __name__ == "__main__":
    app()