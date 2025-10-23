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

def determine_file_status(ratios, samplerate):
    """
    Determines if the FLAC is likely original or upscaled,
    and if upscaled, estimates the source bitrate.
    Uses max frequency across significant frames and match-case.
    """
    cutoff = 0
    ratios = np.array(ratios)
    if len(ratios) == 0:
        return "No audio data.", 0.0

    # Filter out near-silent frames
    ratio_threshold = 0.0000001  # % of total energy above cutoff
    significant_ratios = ratios[ratios > ratio_threshold]

    if len(significant_ratios) == 0:
        return "Likely UPSCALED (no significant frames)", 0.0

    # Nyquist frequency based on actual sample rate
    nyquist = samplerate / 2

    # Maximum frequency across significant frames
    max_ratio = significant_ratios.max()
    max_freq = max_ratio * nyquist

    # Determine upscaled source using descending cutoff order
    status = "Likely ORIGINAL"  # default if max_freq exceeds all cutoffs
    for kbps, cutoff in sorted(BITRATE_CUTOFFS_DESC.items()):
        match max_freq:
            case f if f < cutoff:
                status = f"Likely UPSCALED from ≤{kbps} kbps"
                break

    # Confidence: fraction of significant frames below the same cutoff
    confidence = np.sum(significant_ratios * nyquist < cutoff) / len(significant_ratios)

    return status, confidence
