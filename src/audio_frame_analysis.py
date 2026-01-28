# audio_frame_analysis.py
import numpy as np

from dataclasses import dataclass

CUTOFF_HZ: float = 20_500.0              # probe frequency (Hz) - in this case, usual 320 kbps MP3 file cutoff
NYQUIST_SAFETY_BAND_HZ: float = 200.0    # keep test well below Nyquist

@dataclass
class FrameFFT:
    """Post-window, post-rFFT cache for one frame."""
    freqs_hz: np.ndarray
    spectrum_abs: np.ndarray
    total_energy: float

def divide_into_frames(data, frame_size=32768, step=16384):
    """Divides audio data into overlapping frames for analysis."""
    frames = []
    for start in range(0, len(data) - frame_size, step):
        frames.append(data[start:start+frame_size])
    return frames

def calculate_nyquist_frequency(samplerate):
    nyquist_frequency = samplerate / 2.0
    # Returns the Nyquist frequency (half the samplerate). The safety-band adjustment
    # is applied in calculate_effective_cutoff, not here.
    return nyquist_frequency

def calculate_effective_cutoff(nyquist_frequency):
    # Keep the test frequency meaningfully below Nyquist
    effective_cutoff = min(CUTOFF_HZ, max(0.0, nyquist_frequency - NYQUIST_SAFETY_BAND_HZ))
    return effective_cutoff

def analyze_frame(frame, samplerate, effective_cutoff, fft_cache_list=None):
    """
    Analyze a frame to compute the ratio of spectral energy above 'effective_cutoff' (Hz).
    Returns a float ratio in [0, 1].

    Notes:
    - 'effective_cutoff' should be computed once per file (e.g., via calculate_effective_cutoff)
      and passed in so the same cutoff is used for all frames.
    - If 'fft_cache_list' is provided (list), the function will append a cache entry per frame
      containing freqs, magnitude spectrum, and total_energy for later reuse.
    """
    if frame.ndim > 1:
        frame = frame[:, 0]

    # Guarantee finite frame samples (prevents NaN max/fft propagation)
    if not np.all(np.isfinite(frame)):
        if fft_cache_list is not None:
            fft_cache_list.append(FrameFFT(np.array([]), np.array([]), 0.0))
        return 0.0

    if np.max(np.abs(frame)) < 1e-5:
        if fft_cache_list is not None:
            fft_cache_list.append(FrameFFT(np.array([]), np.array([]), 0.0))
        return 0.0

    windowed = frame * np.hanning(len(frame))
    spectrum = np.abs(np.fft.rfft(windowed))
    freqs = np.fft.rfftfreq(len(frame), d=1 / samplerate)

    total_energy = float(np.sum(spectrum))
    if total_energy <= 0.0 or not np.isfinite(total_energy):
        if fft_cache_list is not None:
            fft_cache_list.append(FrameFFT(freqs, spectrum, 0.0))
        return 0.0

    if fft_cache_list is not None:
        fft_cache_list.append(FrameFFT(freqs_hz=freqs, spectrum_abs=spectrum, total_energy=total_energy))

    high_band_energy = np.sum(spectrum[freqs > effective_cutoff])
    ratio = high_band_energy / total_energy

    if not np.isfinite(ratio):
        return 0.0

    return ratio