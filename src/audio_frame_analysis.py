# audio_frame_analysis.py
import numpy as np

from dataclasses import dataclass

CUTOFF_HZ: float = 20_500.0              # Probe frequency (Hz) - in this case, usual 320 kbps MP3 file cutoff
NYQUIST_SAFETY_BAND_HZ: float = 100.0    # Keeps test well below Nyquist

@dataclass
class FrameFFT:                          # Post-window, post-rFFT cache for one frame
    freqs_hz: np.ndarray
    spectrum_abs: np.ndarray
    total_energy: float

def divide_into_frames(data, frame_size=32768, step=16384):
    frames = []
    for start in range(0, len(data) - frame_size + 1, step):    # Divides audio data into overlapping frames for analysis.
        frames.append(data[start:start+frame_size])
    return frames

def calculate_effective_cutoff(samplerate):
    nyquist_frequency = samplerate / 2.0
    effective_cutoff = min(CUTOFF_HZ, max(0.0, nyquist_frequency - NYQUIST_SAFETY_BAND_HZ))
    return effective_cutoff

def analyze_frame(single_frame, samplerate, effective_cutoff, fft_cache_list=None):
    if single_frame.ndim > 1:
        single_frame = single_frame[:, 0]

    if np.max(np.abs(single_frame)) < 1e-4:
        if fft_cache_list is not None:
            fft_cache_list.append(FrameFFT(np.array([]), np.array([]), 0.0))
        return 0.0

    windowed = single_frame * np.hanning(len(single_frame))
    spectrum = np.abs(np.fft.rfft(windowed))
    freqs = np.fft.rfftfreq(len(single_frame), d=1 / samplerate)
    total_energy = float(np.sum(spectrum))

    if total_energy <= 0.0 or not np.isfinite(total_energy):
        if fft_cache_list is not None:
            fft_cache_list.append(FrameFFT(freqs, spectrum, 0.0))
        return 0.0

    if fft_cache_list is not None:
        fft_cache_list.append(FrameFFT(freqs_hz=freqs, spectrum_abs=spectrum, total_energy=total_energy))

    high_band_energy = np.sum(spectrum[freqs > effective_cutoff])
    ratio = high_band_energy / total_energy

    if __debug__:
        assert np.isfinite(ratio), "Non-finite ratio produced in analyze_frame()"

    return ratio