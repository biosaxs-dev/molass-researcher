# AI Assistant Initialization Guide

**Purpose**: Initialize AI context for the molass-researcher repository  
**Created**: March 6, 2026  
**Magic phrase**: **"Please read COPILOT-INIT.md to initialize"**

---

## What this repository is about

`molass-researcher` is a repository for **AI-augmented experimental SEC-SAXS research**. Each experiment here starts from a real question by a real collaborator, analyzed with real data, with the AI reasoning process visible and reproducible.

This is the experimental-data counterpart to `modeling-vs-model_free` (which does mathematical/theoretical research with the same workflow).

**Connection to Paper (2)** ("Notebook-Driven Science — A New Literacy for the AI Era"):  
This repo is one of the concrete cases demonstrating that the VS Code + Agent mode + Jupyter workflow applies to experimental data science, not just theoretical work.

---

## Key documents

1. **[README.md](README.md)** — Repo overview, experiment list, and how to use this repo
2. **[EXPERIMENT_LOG.md](EXPERIMENT_LOG.md)** — Chronological log of all experiments and findings
3. **[DATA_SOURCES.md](DATA_SOURCES.md)** — Where data lives and how to access it (data is NOT in git)

---

## Working conventions

### Notation
- $M = PC$ (data = scattering profiles × elution curves) — same as `modeling-vs-model_free`
- Experiments are numbered sequentially: `01_`, `02_`, ...

### Data policy
- Raw experimental data lives in Dropbox (not committed to git)
- Each experiment's README documents the data path and access instructions
- Notebooks specify data paths at the top — change `DATA_ROOT` to your local path

### Status symbols
- ✅ Complete, finding documented
- 🔬 Analysis in progress
- ⏳ Planned, not started
- ⚠️ Needs verification

### Experiment structure
Each experiment lives in `experiments/NN_name/`:
```
experiments/01_name/
  README.md          ← question, background, data description, findings
  01a_*.ipynb        ← data exploration / QC
  01b_*.ipynb        ← main analysis
  01c_*.ipynb        ← interpretation and comparison
```

---

## Current experiment

**01: Shimizu averaging order question** (March 2026)  
🔬 In progress  
→ See `experiments/01_shimizu_averaging/README.md`  
→ Planning document: `../modeling-vs-model_free/MOLASS_RESEARCHER_PLAN.md`

---

## Relationship to other repos

| Repo | Role |
|------|------|
| `molass-library` | The Python library used for analysis |
| `modeling-vs-model_free` | Mathematical theory behind decomposition |
| `molass-tutorial` | Teaching how to use molass-library |
| `molass-technical` | Theory exposition |
| **`molass-researcher`** | **This repo: experimental research with real data** |
| `baseline-fluctuation-mystery` | A specific open experimental mystery |
