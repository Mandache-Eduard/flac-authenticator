# data_and_error_logging.py
import csv
import os
from typing import Any, Dict, Iterable

RESULT_FIELDNAMES = [
    "path",
    "status",
    "confidence",
    "elapsed_s",
    "samplerate_hz",
    "num_samples",
    "num_frames",
    "nyquist_frequency_hz",
    "effective_cutoff_hz",
    "per_cutoff_active_fraction",
]

def append_result_to_csv(
    csv_path: str,
    result: Dict[str, Any],
    fieldnames: Iterable[str] = RESULT_FIELDNAMES,
) -> None:
    # Create parent dir only if a directory is actually present in the path
    parent_dir = os.path.dirname(os.path.abspath(csv_path))
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    file_exists = os.path.isfile(csv_path)

    # Build a stable, flat row
    row = {k: result.get(k, "") for k in fieldnames}

    # Optional: normalize numeric formatting for nicer CSV
    conf = row.get("confidence")
    if isinstance(conf, (float, int)):
        row["confidence"] = f"{float(conf):.6f}"

    elapsed = row.get("elapsed_s")
    if isinstance(elapsed, (float, int)):
        row["elapsed_s"] = f"{float(elapsed):.6f}"

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=list(fieldnames),
            extrasaction="ignore",
            quoting=csv.QUOTE_MINIMAL,
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
