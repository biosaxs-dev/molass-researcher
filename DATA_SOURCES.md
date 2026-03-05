# Data Sources

**Purpose**: Document where experimental data lives and how to access it

> ⚠️ Raw experimental data is NOT committed to this repository.  
> Data files are large, may be sensitive, and are managed separately in Dropbox.

---

## Experiment 01: Shimizu 20260305 dataset

**Location**: `Dropbox\MOLASS\DATA\20260305`  
**Access**: Shared Dropbox folder (contact Shimizu or Takahashi)  
**Datasets**:

| Folder | Sample | UV λ (signal) | UV λ (baseline) | Notes |
|--------|--------|--------------|-----------------|-------|
| `Apo`  | Apo    | 280 nm       | 400 nm          | Original, high S/N |
| `ATP`  | ATP    | 290 nm       | 400 nm          | Original, high S/N |
| `MY`   | MY     | 290 nm       | 400 nm          | Original, high S/N |
| `Apo2` | Apo    | 280 nm       | 400 nm          | Pre-averaged (19 frames) |
| `ATP2` | ATP    | 290 nm       | 400 nm          | Pre-averaged (19 frames) |
| `MY2`  | MY     | 290 nm       | 400 nm          | Pre-averaged (19 frames) |

**Data path in notebooks**: Set `DATA_ROOT` at the top of each notebook, e.g.:
```python
DATA_ROOT = r"C:\Users\takahashi\Dropbox\MOLASS\DATA\20260305"
```

---

## How to add new data sources

When adding a new experiment, document here:
- Dataset identifier and date
- Dropbox (or other) path
- Sample descriptions
- Special wavelength or instrument settings
- Who provided the data
