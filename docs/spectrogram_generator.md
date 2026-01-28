

<!-- AUTO-GENERATED:BEGIN -->
## External Dependencies (auto)
### Imports
- `pathlib.Path`
- `shutil`
- `subprocess`

## Module-level Constants and Variables (auto)
- (none detected)

## Module Workflow (auto: call graph)
```mermaid
flowchart TD
    classDef ok fill:#d4f4dd,stroke:#2e7d32;
    classDef err fill:#fde0e0,stroke:#c62828;

    M["spectrogram_generator.py"]:::ok
    F_ffmpeg_works["ffmpeg_works()"]:::ok
    M --> F_ffmpeg_works
    F_spectrogram_for_flac["spectrogram_for_flac()"]:::ok
    M --> F_spectrogram_for_flac
    F_spectrogram_for_flac --> F_ffmpeg_works
```

## Function Inventory (auto)
- `ffmpeg_works()` -> `bool`
- `spectrogram_for_flac(file_path)`
<!-- AUTO-GENERATED:END -->
