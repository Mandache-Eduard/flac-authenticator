

<!-- AUTO-GENERATED:BEGIN -->
## External Dependencies (auto)
### Imports
- `dataclasses.dataclass`
- `numpy`

## Module-level Constants and Variables (auto)
- `CUTOFF_HZ: float = 20500.0`
- `NYQUIST_SAFETY_BAND_HZ: float = 200.0`

## Module Workflow (auto: call graph)
```mermaid
flowchart TD
    classDef ok fill:#d4f4dd,stroke:#2e7d32;
    classDef err fill:#fde0e0,stroke:#c62828;

    M["audio_frame_analysis.py"]:::ok
    F_analyze_frame["analyze_frame()"]:::ok
    M --> F_analyze_frame
    F_calculate_effective_cutoff["calculate_effective_cutoff()"]:::ok
    M --> F_calculate_effective_cutoff
    F_calculate_nyquist_frequency["calculate_nyquist_frequency()"]:::ok
    M --> F_calculate_nyquist_frequency
    F_divide_into_frames["divide_into_frames()"]:::ok
    M --> F_divide_into_frames
```

## Function Inventory (auto)
- `analyze_frame(frame, samplerate, effective_cutoff, fft_cache_list)`
- `calculate_effective_cutoff(nyquist_frequency)`
- `calculate_nyquist_frequency(samplerate)`
- `divide_into_frames(data, frame_size, step)`
<!-- AUTO-GENERATED:END -->
