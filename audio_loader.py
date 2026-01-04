# audio_loader.py
import os
import numpy as np
import soundfile as sf

def load_flac(file_path):
    """Loads a FLAC file and returns the audio data and sample rate."""
    try:
        data, samplerate = sf.read(file_path, always_2d=False)

        # Ensure numpy array
        data = np.asarray(data)

        # Convert to float32 (optional, but consistent and faster)
        if data.dtype.kind != "f":
            data = data.astype(np.float32)
        else:
            data = data.astype(np.float32, copy=False)

        # If any non-finite samples exist, replace them with 0.0
        if not np.all(np.isfinite(data)):
            data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)

        return data, samplerate
    except Exception as e:
        print(f"Error loading file: {e}")
        return None, None
