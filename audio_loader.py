import soundfile as sf

def load_flac(file_path):
    """Loads a FLAC file and returns the audio data and sample rate."""
    try:
        data, samplerate = sf.read(file_path)
        return data, samplerate
    except Exception as e:
        print(f"Error loading file: {e}")
        return None, None