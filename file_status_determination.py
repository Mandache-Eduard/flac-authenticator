import numpy as np

BITRATE_CUTOFFS_DESC = {
    320: 20500,
    256: 20000,
    192: 19000,
    160: 17000,
    128: 16000,
    96: 13000,
    64: 11000
}

def determine_file_status(ratios):
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