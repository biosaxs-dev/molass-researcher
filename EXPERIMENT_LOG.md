# Experiment Log

**Purpose**: Chronological record of all experiments — questions asked, findings, and status

---

## 2026-03-06: Experiment 01 — 01c pairwise comparison complete

**Notebook**: `01c_comparison_analysis.ipynb`

**Findings**:

**Apo/Apo2 and ATP/ATP2 (simple pairs)**:
- ΔRg = 0.06 Å (Apo) and 0.11 Å (ATP) — both within fitting uncertainty
- Pearson r of P(q) = 0.99999 for both pairs; elution r > 0.999
- **Verdict**: Pre-averaging has no measurable effect for clean single-component samples

**MY / MY2 (multi-component case)**:
- MY forced to 3 components: finds Rg ≈ 32.4 Å, Guinier-failed, 29.3 Å — no large-Rg species. The extra components are noise artifacts.
- MY2 (default 3c): Rg = 97.0, 53.6, 32.4 Å — genuine aggregate + monomer
- Monomer P(q) comparison across all 3 analysis modes: r ≥ 0.99994 (essentially identical)
- **Verdict**: pre-averaging reveals aggregate populations below the noise floor in the original data; the monomer itself is unchanged

**Debugging notes during 01c**:
- *q-axis mismatch*: `get_xr_matrices()` returns P(q) arrays of different lengths for different datasets (trimming differences). Fixed by interpolating onto a common `np.linspace(q_lo, q_hi, 500)` grid before `pearsonr`.
- *None Rg*: `quick_decomposition(num_components=3)` on a noisy sample can return `None` from `get_rgs()` for spurious components where Guinier fit fails. Guard with `f"{rg:.2f}" if rg is not None else "N/A"`.

**Outputs saved**: `01c_simple_pairs.png`, `01c_my_forced3.png`, `01c_my_monomer_comparison.png`

**Status**: ✅ Experiment 01 complete.

---

## 2026-03-06: Experiment 01 — 01b plotting cell re-run (fix for blank figures)

**Issue**: After the initial run of `01b_molass_runs.ipynb`, three blank figures appeared in the plotting cell output, titled "Apo vs Apo2 — MOLASS decomposition (default settings)", "ATP vs ATP2 …", and "MY vs MY2 …".

**Root cause**: The original plotting code created `plt.subplots(1, 2)` side-by-side panels and called `plt.sca(ax)` to redirect `plot_components()` into them. However, `plot_components()` always opens its own new figure internally and ignores the current-axes setting. The subplot wrapper canvases were therefore never drawn into — they appeared as blank figures when Jupyter flushed all open figures at cell end.

**Fix**: Replaced the subplot-wrapper approach with sequential individual `plot_components()` calls, one per dataset. Source was already corrected in the prior session; this session re-ran the cell to clear the stale blank outputs.

**Outcome**: All 6 dataset plots render correctly (one rich 2×3 panel per dataset). Six PNG files saved: `01b_decomp_apo.png`, `01b_decomp_apo2.png`, `01b_decomp_atp.png`, `01b_decomp_atp2.png`, `01b_decomp_my.png`, `01b_decomp_my2.png`.

**Lesson**: `plot_components()` is not axis-injectable; always call it standalone and save the figure it creates.

---

## 2026-03-06: Experiment 01 — 01a data exploration complete

**01a findings**:
- Renamed `Apo2.txt`→`Apo2_UV.txt`, `ATP2.txt`→`ATP2_UV.txt` (molass requires `_UV.txt` suffix).
- All 6 datasets load: XR shape (1026, 1500) for Apo/ATP pairs, (1027, 1500) for MY pair; UV shape (501, 1500) and (1201, 1500) for MY.
- Peak shapes match perfectly between original and pre-averaged pairs (UV + SAXS overlays).
- UV S/N is identical across pairs — suggesting only SAXS frames were externally pre-averaged.
- MY is the richest test case (2 peaks, lowest S/N ~91).
- All datasets cleared for MOLASS analysis. Next: `01b_molass_runs.ipynb`.

**Status**: 🔬 01a complete; 01b pending

---

## 2026-03-06: Experiment 01 started — Shimizu averaging order question

**Question from**: Shimizu (collaborator)  
**Dataset**: `Dropbox/MOLASS/DATA/20260305` (Apo, ATP, MY + pre-averaged versions)  
**Core question**: Does pre-averaging 19 frames before MOLASS change decomposition results decisively compared to MOLASS's internal averaging?  
**Status**: ✅ 01a complete  
**See**: `experiments/01_shimizu_averaging/README.md`

---

*Add new entries at the top as experiments progress.*
