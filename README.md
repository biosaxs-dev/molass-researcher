# molass-researcher

**AI-augmented experimental SEC-SAXS research**

> Each notebook here documents a real question from a real collaborator, answered with real data, with the AI reasoning process visible.

> **For AI assistants**: To initialize context, say **"Please read COPILOT-INIT.md to initialize"**

---

## What is this?

This repository documents **experimental research** using [molass-library](https://github.com/biosaxs-dev/molass-library) to analyze SEC-SAXS (Size-Exclusion Chromatography combined with Small-Angle X-ray Scattering) data.

Unlike `molass-tutorial` (teaching) or `molass-technical` (theory), this repo shows the *process* of doing research — including questions, dead ends, and unexpected findings. An AI assistant (GitHub Copilot) participates as an active collaborator in experimental design, analysis, and interpretation.

**Part of a broader research program**:  
This repo is one of several demonstrating AI-augmented scientific research — see [PAPER_VISION_DISCUSSION.md](../modeling-vs-model_free/PAPER_VISION_DISCUSSION.md) for how it connects to ongoing theoretical work.

---

## Experiments

| # | Title | Collaborator | Date | Status |
|---|-------|-------------|------|--------|
| 01 | [Averaging order effect on MOLASS decomposition](experiments/01_shimizu_averaging/README.md) | Shimizu | March 2026 | 🔬 In progress |

---

## How to use this repo

### Prerequisites
```bash
pip install molass
# or: pip install -e path/to/molass-library
```

### Data access
Raw experimental data is **not in this repository** (stored in Dropbox).  
See [DATA_SOURCES.md](DATA_SOURCES.md) for access instructions.

### Running notebooks
1. Set `DATA_ROOT` at the top of each notebook to your local data path
2. Run cells in order
3. Results and figures are saved in the notebook output

### For AI assistants
Say **"Please read COPILOT-INIT.md to initialize"** to load context.

---

## Repository structure

```
molass-researcher/
├── COPILOT-INIT.md        ← AI initialization guide
├── README.md              ← this file
├── EXPERIMENT_LOG.md      ← chronological research log
├── DATA_SOURCES.md        ← data locations and access
├── experiments/
│   ├── 01_shimizu_averaging/
│   │   ├── README.md
│   │   ├── 01a_data_exploration.ipynb
│   │   ├── 01b_molass_runs.ipynb
│   │   └── 01c_comparison_analysis.ipynb
│   └── ...
└── shared/
    └── utils.py           ← shared plotting / analysis helpers
```

---

## License

MIT
