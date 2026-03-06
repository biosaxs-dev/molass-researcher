# Project Status

**Last Updated**: March 6, 2026

> **For repo overview**: See [README.md](README.md)  
> **For working conventions**: See [COPILOT-INIT.md](COPILOT-INIT.md)  
> **This document**: Tracks current task and chronological research progress

---

## 🎯 Current Task

**Experiment 01 complete.** Ready for review and next experiment.

---

## 🎯 Latest Achievements

### March 6, 2026: Experiment 01 complete — all notebooks run, findings documented

**01a — Data exploration**: All 6 datasets QC'd. UV identical between pairs (SAXS-only averaging confirmed). MY has lowest S/N (~91 vs ~215 for Apo/ATP).

**01b — MOLASS runs**: All 6 decompositions run with default settings.  
Key finding: MY → 2 spurious components (both Rg ≈ 32.3 Å); MY2 → 3 genuine components (Rg = 97, 54, 32.4 Å). Apo/ATP: 1 component each, Rg unchanged.

**01c — Pairwise comparison**: Quantitative analysis complete.
- Apo/Apo2: ΔRg = 0.06 Å, r_P(q) = 0.99999 — no meaningful effect
- ATP/ATP2: ΔRg = 0.11 Å, r_P(q) = 0.99999 — no meaningful effect
- MY monomer (all 3 analysis modes): Rg ≈ 32.4 Å, r ≥ 0.99994 — identical
- MY forced-3c: no large-Rg components found; extra components are noise artifacts
- Conclusion: pre-averaging reveals aggregates below noise floor in MY; no effect for clean single-component samples

**Documentation updated**: EXPERIMENT_LOG.md, MEMO_FOR_SHIMIZU.md

### March 6, 2026: Repository created, Experiment 01 scaffolded

**Trigger**: Shimizu (collaborator) provided new SEC-SAXS dataset with question about pre-averaging effect.

**Achievements**:
- Created `molass-researcher` repo on GitHub (`biosaxs-dev/molass-researcher`)
- Scaffolded: COPILOT-INIT.md, README, EXPERIMENT_LOG, DATA_SOURCES, RESEARCH_PLAN, shared/utils.py
- Created 2-repo workspace file (`molass-researcher.code-workspace`) with `molass-library`
- Created `experiments/01_shimizu_averaging/`: README + `01a_data_exploration.ipynb`
- Complied with AI Context Standard v0.5

**Experiment 01 setup**:
- 6 datasets: Apo, ATP, MY (original) + Apo2, ATP2, MY2 (19-frame pre-averaged)
- UV: 280 nm (Apo) / 290 nm (ATP, MY) / 400 nm baseline
- Research question: Does pre-averaging before MOLASS change decomposition results decisively?

**Status**: ✅ Experiment 01 complete. Results confirmed. Ready to communicate to Shimizu.
