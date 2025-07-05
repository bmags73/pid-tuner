import os
import shutil
import json
from pathlib import Path

import typer

from .compare import compare_logs
from .config import parse_bf_dump

app = typer.Typer(
    help="PID-Tuner: extract, compare, and plot Blackbox logs, and parse Betaflight configs."
)

@app.command()
def compare(
    directory: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        help="Path to folder of .bbl files",
    ),
    axes: list[str] = typer.Option(
        ["roll", "pitch"],
        "--axes", "-a",
        help="Which axes to analyze (comma-separated)",
    ),
    window: int = typer.Option(
        50, "--window", "-w",
        help="Window size for spike detection",
    ),
    threshold: float = typer.Option(
        2.0, "--threshold", "-t",
        help="Spike detection threshold factor",
    ),
    out_dir: Path = typer.Option(
        Path("pid_tune"), "--out-dir", "-o",
        help="Where to put decoded CSVs, graphs, summary",
    ),
    clean: bool = typer.Option(
        False, "--clean",
        help="Remove intermediate decoded/ folder after running",
    ),
):
    """
    1) Decode all .bbl → .csv/.event under out_dir/decoded  
    2) Compute spikes & metrics → graphs + compare_summary.csv in out_dir  
    3) If --clean: delete that entire decoded/ subfolder  
    """
    # Ensure the output directory exists
    os.makedirs(out_dir, exist_ok=True)

    # Run the core compare logic
    compare_logs(
        directory=str(directory),
        axes=axes,
        window=window,
        threshold=threshold,
        out_dir=str(out_dir),
    )

    # Optionally clean up intermediate files
    decoded_dir = out_dir / "decoded"
    if clean and decoded_dir.exists():
        shutil.rmtree(decoded_dir)
        typer.echo(f"🧹 Removed intermediate files: {decoded_dir}")

@app.command()
def config(
    bf_dump: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Betaflight CLI dump file",
    ),
    out: Path = typer.Option(
        Path("config.json"),
        "--out", "-o",
        help="Where to save extracted config JSON",
    ),
):
    """
    Parse a Betaflight CLI dump and extract PID, rates, and filter settings.
    """
    # Parse the dump into a Python dict
    cfg = parse_bf_dump(bf_dump)

    # Write the dict out as nicely formatted JSON
    with open(out, "w") as f:
        json.dump(cfg, f, indent=2)

    typer.echo(f"⚙️  Saved Betaflight config to {out}")

if __name__ == "__main__":
    app()
