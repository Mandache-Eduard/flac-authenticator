import os
import shutil
import subprocess
import sys
import time

from audio_frame_analysis import analyze_frame, divide_into_frames
from audio_loader import load_flac

def main():
    # 1. Get file path from command-line argument
    if len(sys.argv) < 2:
        print("Usage: python flac_authenticator.py <path_to_flac_file>")
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

    # 4. Analyze each frame
    ratios = [analyze_frame(frame, samplerate) for frame in frames]
    print(f"Analyzed {len(frames)} frames ({sum(r > 0 for r in ratios)} active).")

    # 5. Determine file status
    status, confidence = determine_file_status(ratios)

    # 6. Print results and spectrogram
    print(f"Result: {status} (Confidence: {confidence*100:.1f}%)")
    elapsed = time.time() - start_time
    print(f"Processing time: {elapsed:.2f} seconds")

    if not shutil.which("spek"):
        print("Spek not detected. Please install it from https://spek.cc and ensure it's in your PATH.")

    # Run Spek via command line
    try:
        subprocess.run(["spek", file_path], check=True)
    except FileNotFoundError:
        print("Spek is not installed or not in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Spek exited with an error: {e}")

    #spectrogram, freqs = compute_spectrogram(data, samplerate)
    #plot_spectrogram(spectrogram, freqs, samplerate)


if __name__ == "__main__":
    main()