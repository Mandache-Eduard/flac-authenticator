import sys
import os
import numpy as np
import soundfile as sf
import time

BITRATE_CUTOFFS_DESC = {
    320: 20500,
    256: 20000,
    192: 19000,
    160: 17000,
    128: 16000,
    96: 13000,
    64: 11000
}

def load_flac(file_path):
    """Loads a FLAC file and returns the audio data and sample rate."""
    try:
        data, samplerate = sf.read(file_path)
        return data, samplerate
    except Exception as e:
        print(f"Error loading file: {e}")
        return None, None


def divide_into_frames(data, frame_size=16384, step=4096):
    """Divides audio data into overlapping frames for analysis."""
    frames = []
    for start in range(0, len(data) - frame_size, step):
        frames.append(data[start:start+frame_size])
    return frames


def analyze_frame(frame, samplerate, cutoff_freq=19000):
    """
    Analyze a frame to compute the ratio of spectral energy above cutoff_freq.
    Returns a float ratio between 0 and 1.
    """
    if frame.ndim > 1:
        frame = frame[:, 0]

    if np.max(np.abs(frame)) < 1e-5:
        return 0.0

    windowed = frame * np.hanning(len(frame))
    spectrum = np.abs(np.fft.rfft(windowed))
    freqs = np.fft.rfftfreq(len(frame), d=1 / samplerate)

    total_energy = np.sum(spectrum)
    if total_energy == 0:
        return 0.0

    high_band_energy = np.sum(spectrum[freqs > cutoff_freq])
    ratio = high_band_energy / total_energy
    return ratio


def determine_file_status(ratios, frames, samplerate, cutoff_freq=19000):
    """
    Determines if the FLAC is likely original or upscaled
    based on the fraction of frames with meaningful energy above cutoff_freq.
    """
    ratios = np.array(ratios)
    if len(ratios) == 0:
        return "No audio data.", 0.0

    ratio_threshold = 0.001  # 0.1% of total energy above cutoff
    active_frames = np.sum(ratios > ratio_threshold)
    active_fraction = active_frames / len(ratios)

    if active_fraction > 0.05:
        return "Likely ORIGINAL", active_fraction
    else:
        return "Likely UPSCALED", 1 - active_fraction


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
    status, confidence = determine_file_status(ratios, frames, samplerate)

    # 6. Print results
    print(f"Result: {status} (Confidence: {confidence*100:.1f}%)")
    elapsed = time.time() - start_time
    print(f"Processing time: {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()
