import numpy as np

def divide_into_frames(data, frame_size=32768, step=2048):
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