# run_modes.py
import time
import os

from audio_frame_analysis import analyze_frame, divide_into_frames, calculate_nyquist_frequency, \
    calculate_effective_cutoff
from audio_loader import load_flac
from external_tools import call_spek
from file_status_determination import determine_file_status, debug_energy_ratios
from pprint import pprint

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

    # 5. Print results and spectrogram
    status, confidence = determine_file_status(ratios, effective_cutoff_hz, frame_ffts=fft_cache)  # CHANGED: pass cache
    #summary = debug_energy_ratios(ratios)
    elapsed = time.time() - start_time

    if verbose:
        print(f"Loaded '{file_path}' with sample rate {samplerate} Hz, {len(data)} samples.")
        print(f"Divided audio into {len(frames)} frames for analysis.")
        print(f"Analyzed {len(frames)} frames ({sum(r > 0 for r in ratios)} active).")
        print(f"Result: {status} (Confidence: {confidence * 100:.1f}%)")
        print(f"Processing time: {elapsed:.2f} seconds")
        print("Energy-above-cutoff summary:")
        #pprint(summary)

    if open_spek:
        call_spek(file_path)

    result = {
        "path": file_path,
        "status": status,
        "confidence": confidence,
        "elapsed_s": elapsed,
        "samplerate_hz": samplerate,
        "num_samples": len(data),
        "num_frames": len(frames),
        "nyquist_frequency_hz": nyquist_frequency_hz,
        "effective_cutoff_hz": effective_cutoff_hz,
    }

    return result

def run_folder_batch(folder_path):
    for dirpath, dirnames, filenames in os.walk(folder_path, topdown=False, onerror=None, followlinks=False):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if not full_path.lower().endswith(".flac"):
                continue
            else:
                result = run_single_file(full_path, verbose=False, open_spek=False)
                path = result["path"]
                status = result["status"]
                confidence = result["confidence"]
                elapsed_s = result["elapsed_s"]
                samplerate_hz = result["samplerate_hz"]
                num_samples = result["num_samples"]
                num_frames = result["num_frames"]
                nyquist_frequency_hz = result["nyquist_frequency_hz"]
                effective_cutoff_hz = result["effective_cutoff_hz"]
