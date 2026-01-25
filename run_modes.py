# run_modes.py
import time
import os
from typing import Any, Dict, Final, List, Optional
from tqdm import tqdm
from datetime import datetime
from audio_frame_analysis import analyze_frame, divide_into_frames, calculate_nyquist_frequency, \
    calculate_effective_cutoff
from audio_loader import load_flac
from external_tools import call_spek
from file_status_determination import determine_file_status
from data_and_error_logging import append_result_to_csv


RESULT_FIELDNAMES: Final[List[str]] = [
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

def _format_fractions_for_csv(fractions: Optional[Dict[float, float]]) -> str:
    """
    Format {cutoff_hz: active_fraction} into a single CSV-friendly string.
    Example: "13000=0.8123;16000=0.4550;20500=0.0123"
    """
    if not fractions:
        return ""
    return ";".join(f"{int(k)}={v:.4f}" for k, v in sorted(fractions.items()))

def run_single_file(file_path, verbose, open_spek):
    # 1. Load audio
    start_time = time.time()
    data, samplerate = load_flac(file_path)

    # 2. Divide into frames
    frames = divide_into_frames(data)

    # 3. Calculate (once per file, then reuse everywhere)
    nyquist_frequency_hz = calculate_nyquist_frequency(samplerate)
    effective_cutoff_hz = calculate_effective_cutoff(nyquist_frequency_hz)

    # 4. Analyze each frame — use the same 'effective_cutoff' for all frames; also collect FFT cache for later reuse
    fft_cache = []
    ratios = [analyze_frame(frame, samplerate, effective_cutoff_hz, fft_cache_list=fft_cache) for frame in frames]

    # 5. Determine status + confidence + fractions + elapsed time
    status, confidence, fractions = determine_file_status(ratios, effective_cutoff_hz, frame_ffts=fft_cache)  # CHANGED: pass cache
    #summary = debug_energy_ratios(ratios)
    elapsed = time.time() - start_time

    # 6. Build result using the single schema list (prevents key drift)
    result: Dict[str, Any] = {k: "" for k in RESULT_FIELDNAMES}
    result.update(
        {
            "path": file_path,
            "status": status,
            "confidence": confidence,
            "elapsed_s": elapsed,
            "samplerate_hz": samplerate,
            "num_samples": len(data),
            "num_frames": len(frames),
            "nyquist_frequency_hz": nyquist_frequency_hz,
            "effective_cutoff_hz": effective_cutoff_hz,
            "per_cutoff_active_fraction": _format_fractions_for_csv(fractions),
        }
    )

    if verbose:
        print(f"Loaded '{file_path}' with sample rate {samplerate} Hz, {len(data)} samples.")
        print(f"Divided audio into {len(frames)} frames for analysis.")
        print(f"Analyzed {len(frames)} frames ({sum(r > 0 for r in ratios)} active).")
        print(f"Result: {status} (Confidence: {confidence * 100:.1f}%)")
        print(f"Processing time: {elapsed:.2f} seconds")
        print("Energy-above-cutoff summary:")
        #pprint(summary)

        if fractions:
            print("[bitrate-debug] per_cutoff_active_fraction:")
            for k, v in sorted(fractions.items()):
                print(f"  {int(k)}: {v:.4f}")

    if open_spek:
        call_spek(file_path)

    return result

def run_folder_batch(folder_path):
    current_datetime = datetime.now()
    current_daytime_formatted = current_datetime.strftime('%Y-%B-%d__%H-%M-%S')
    csv_path = os.path.join(folder_path, current_daytime_formatted + ".csv")
    flac_file_paths = []

    print("Discovering files...")
    for dirpath, dirnames, filenames in os.walk(folder_path, topdown=True, onerror=None, followlinks=False):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if full_path.lower().endswith(".flac"):
                flac_file_paths.append(full_path)

    print("Discovered {} files.".format(len(flac_file_paths)))
    print("Processing files and saving results...")
    for flac_file_path in tqdm(flac_file_paths):
        try:
            result = run_single_file(flac_file_path, verbose=False, open_spek=False)
        except Exception:
            result = {"path": flac_file_path, "status": "ERROR"}
        append_result_to_csv(csv_path, result)
