import os
import sys
import time

from audio_frame_analysis import analyze_frame, divide_into_frames, calculate_nyquist_frequency, calculate_effective_cutoff
from audio_loader import load_flac
from file_status_determination import determine_file_status
from file_status_determination import debug_energy_ratios
from external_tools import call_spek


def main():
    # 1. Get file path from command-line argument
    if len(sys.argv) < 2:
        print("Usage: py main.py <path_to_flac_file>")
        return

    file_path = sys.argv[1]
    if not os.path.isfile(file_path) or not file_path.lower().endswith(".flac"):
        print("Invalid file path or not a FLAC file.")
        return

    # 2. Load audio
    start_time = time.time()

    data, samplerate = load_flac(file_path)
    if data is None:
        return
    print(f"Loaded '{file_path}' with sample rate {samplerate} Hz, {len(data)} samples.")

    # 3. Divide into frames
    frames = divide_into_frames(data)
    print(f"Divided audio into {len(frames)} frames for analysis.")

    # 4. Calculate (once per file, then reuse everywhere)
    nyquist_frequency = calculate_nyquist_frequency(samplerate)
    effective_cutoff = calculate_effective_cutoff(nyquist_frequency)

    # 5. Analyze each frame — use the same 'effective_cutoff' for all frames; also collect FFT cache for later reuse
    fft_cache = []
    ratios = [analyze_frame(frame, samplerate, effective_cutoff, fft_cache_list=fft_cache) for frame in frames]
    print(f"Analyzed {len(frames)} frames ({sum(r > 0 for r in ratios)} active).")

    # 6. Print results and spectrogram
    status, confidence = determine_file_status(ratios, effective_cutoff, frame_ffts=fft_cache)  # CHANGED: pass cache
    print(f"Result: {status} (Confidence: {confidence * 100:.1f}%)")

    elapsed = time.time() - start_time
    print(f"Processing time: {elapsed:.2f} seconds")

    summary = debug_energy_ratios(ratios)
    from pprint import pprint
    print("Energy-above-cutoff summary:")
    pprint(summary)

    call_spek(file_path)

if __name__ == "__main__":
    main()
