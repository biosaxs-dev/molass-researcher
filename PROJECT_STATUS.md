# Project Status

**Last Updated**: March 12, 2026 (evening)

> **For repo overview**: See [README.md](README.md)  
> **For working conventions**: See [COPILOT-INIT.md](COPILOT-INIT.md)  
> **This document**: Tracks current task and chronological research progress

---

## 🎯 Current Task

**Experiment 02 in progress** — Buffit vs LPM comparison documented; LPM calibration bug fixed.  
→ Next: decide on Experiment 03 or further LPM analysis (table coverage for narrow peaks).

---

## 🎯 Latest Achievements

### March 12, 2026 (evening): Experiment 02b/02d — Buffit vs LPM documented; LPM calibration fixed

**02b — Buffit vs LPM comparison** (`02b_buffit_explanation.ipynb`):

Comparison of Buffit (Otsu threshold) vs LPM (adaptive p_final, issue #4 fix) on SAMPLE1 and MY.

| Dataset | LPM (adaptive) | Buffit (Otsu) | Ideal |
|---------|:-:|:-:|:-:|
| SAMPLE1 | 0.645 | 0.519 | 0.5 |
| MY      | 0.854 | 0.496 | 0.5 |

**molass-library — `_compute_adaptive_p_final` calibration fix** (`LpmBaseline.py`):

Two bugs discovered and fixed in the adaptive p_final computation:
1. **Wrong knot range**: `np.linspace(0, n, ...)` used instead of `np.linspace(x[0], x[-1], ...)` — caused silent `LSQUnivariateSpline` failure for frame-indexed data (MY's `jv` starts at 673), falling back to uncalibrated absolute noisiness.
2. **Absolute instead of relative noisiness**: spline residual std was passed directly to the table, but the table was built with *relative* noisiness (noise/signal amplitude). Fix: divide by `np.abs(y).max()`.

Effect: SAMPLE1 improved 0.716 → 0.645; MY improved 0.987 → 0.854. MY still trails Buffit because `size_sigma` ≈ 2.24 falls below the table's minimum (3), clamping p_final.

**02d — Otsu threshold explanation** (`02d_otsu_explanation.ipynb`, new notebook):

Explains the Otsu criterion, why it includes protein-tail frames for MY (bimodal histogram valley at ≈0.41), and why this does not degrade baseline quality. Three figures:
- Fig 1: σ_B²(k) criterion + elution coloured by threshold
- Fig 2: tail frame quantification
- Fig 3 (new): per-row polyfit baselines for low-q and high-q rows, showing Otsu and fixed-0.10 baselines are nearly identical

**Conclusion**: Buffit (Otsu + polyfit) clearly outperforms LPM even after calibration fix. The Otsu threshold is robust for general use.


**02a — Multi-dataset verification** (Issue [#1](https://github.com/biosaxs-dev/molass-researcher/issues/1), closed):

Added new cells to `02a_score_comparison.ipynb` looping over SAMPLE1–SAMPLE4. Results:

| Sample | Label | ratio_linear | ratio_bufmask | improvement |
|--------|-------|-------------|--------------|-------------|
| SAMPLE1 | Apo  | 0.716 | 0.578 | +0.138 ✅ |
| SAMPLE2 | ATP  | 0.639 | 0.546 | +0.092 ✅ |
| SAMPLE3 | MY   | 0.702 | 0.561 | +0.140 ✅ |
| SAMPLE4 | Apo2 | 0.702 | 0.600 | +0.103 ✅ |

`bufmask < linear` for all 4 samples. Acceptance criterion met. Issue #1 closed.

**02a — Positive score comparison** (`02a_score_comparison.ipynb`):

- **Exact legacy match confirmed** (cell 23): fixed library (adaptive p_final) mean positive_ratio = 0.716, matches legacy simulation exactly to 3 decimal places.
- **Buffer-mask polyfit proposed** (cell 24): new idea from GitHub Copilot (Claude Sonnet 4.5) — classify buffer frames once from high-SNR summed elution (`M.sum(axis=0)`), then fit linear baseline through those frames only per q-row. Much more direct than iterative LPM percentile descent.
- **Results on SAMPLE1**:

  | Method | mean positive_ratio |
  |---|---|
  | Old library (p_final 10%) | 0.899 |
  | Adaptive p_final / legacy | 0.716 |
  | **Bufmask (thr=0.10)** | **0.578** |
  | Ideal | ~0.5 |

- Threshold insensitive: thr=0.05–0.20 all cluster within 0.551–0.598.

**molass-library — Issue [#23](https://github.com/biosaxs-dev/molass-library/issues/23) (stdout suppression)**:
- `get_baseline2d()` printed `recognize_num_peaks` / `peak_width=` on every call
- Fix: `contextlib.redirect_stdout(io.StringIO())` wrapper; test added; committed 71f1228.

**molass-library — Issue [#24](https://github.com/biosaxs-dev/molass-library/issues/24) (bufmask method)**:
- New `baseline_method='bufmask'` implemented in `molass/Baseline/BufmaskBaseline.py`
- Wired into `Baseline2D.py` (`_bufmask_individual_axes_impl`, `CUSTOM_IMPL_DICT`)
- Wired into `SsMatrixData.get_baseline2d()` (buffer_mask pre-computed from summed elution)
- Test added: `test_09_bufmask_baseline` (ratio_bufmask < ratio_linear ✓)
- Docstring includes concept explanation and Copilot attribution (commit c80f70e)
- Committed 047403d, closed.

**Next**: Issue [#1](https://github.com/biosaxs-dev/molass-researcher/issues/1) — verify bufmask superiority on SAMPLE2–4.



**01f — MY/MY2 baseline investigation** (`01f_my_my2_baseline_investigation.ipynb`):
- Used untrimmed data throughout; `plot_compact(baseline=True)`, UV channel comparison (290 nm vs 400 nm), and 3D UV surface plots
- Observed localised negative UV dip at 270–300 nm, frames 1190–1340 (after the minor aggregate peak)
- Distinguished from dc/dt baseline fluctuation (baseline-fluctuation-mystery): wavelength-selective, temporally localised, not derivative-shaped → UV-specific phenomenon (inner filter / RI artifact hypothesis)
- **Conclusion**: Default trimming removes this anomaly without affecting baseline determination. Safe to proceed with default trim + linear baseline.
- Observations recorded in notebook cell 9.

**molass-library AI-friendliness improvement — Issue #15**:
- Identified friction during notebook work: `uv.iv` / `uv.jv` opaque names
- Fix: added `uv.wavelengths` and `uv.frames` properties to `UvData`; updated docstring with matrix orientation `M: (wavelengths × frames)`
- Test added: `test_02_uv_friendly_aliases` in `tests/generic/010_DataObjects/test_010_SSD.py`. All 3 tests pass.
- GitHub Issue [#15](https://github.com/biosaxs-dev/molass-library/issues/15) created via `gh` CLI.

**Workflow infrastructure**:
- `molass-review` repo added to workspace file (`molass-researcher.code-workspace`)
- AI Improvement Feedback Loop documented in `molass-library/Copilot/copilot-guidelines.md` (Rule 11) and `API_IMPROVEMENTS.md` (GitHub Issue Status table)
- Paper suggestions (Software Design section) recorded in `molass-review/review-discussions/paper-software-design-suggestions.md`
- Practice workflow saved to persistent user memory (`/memories/molass_library_workflow.md`)

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
