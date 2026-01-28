

<!-- AUTO-GENERATED:BEGIN -->
## External Dependencies (auto)
### Imports
- `csv`
- `os`
- `typing.Any`
- `typing.Dict`
- `typing.Iterable`

## Module-level Constants and Variables (auto)
- `RESULT_FIELDNAMES = ['path', 'status', 'confidence', 'elapsed_s', 'samplerate_hz', 'num_samples', 'num_frames', 'nyquist_frequency_hz', 'effective_cutoff_hz', 'per_cutoff_active_fraction']`

## Module Workflow (auto: call graph)
```mermaid
flowchart TD
    classDef ok fill:#d4f4dd,stroke:#2e7d32;
    classDef err fill:#fde0e0,stroke:#c62828;

    M["data_and_error_logging.py"]:::ok
    F_append_result_to_csv["append_result_to_csv()"]:::ok
    M --> F_append_result_to_csv
```

## Function Inventory (auto)
- `append_result_to_csv(csv_path, result, fieldnames)` -> `None`
<!-- AUTO-GENERATED:END -->
