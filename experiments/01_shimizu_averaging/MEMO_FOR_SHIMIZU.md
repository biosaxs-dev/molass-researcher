# Data QC Report — Shimizu 20260305 Dataset

**Prepared by**: Takahashi (AI-assisted, March 6, 2026)  
**Dataset**: `Dropbox\MOLASS\DATA\20260305`  
**Purpose**: Pre-analysis data quality check before MOLASS decomposition runs  
**Notebook**: `01a_data_exploration.ipynb`  
**Requires**: molass ≥ 0.8.3

---

## Summary

All 6 datasets (Apo, Apo2, ATP, ATP2, MY, MY2) passed visual QC. Data are clean and ready for MOLASS analysis. One data hygiene issue was resolved on our end (see below). Key observation: **the UV files in the `*2` (pre-averaged) datasets appear to be unchanged from the originals** — only the SAXS frames seem to have been pre-averaged.

---

## Data Hygiene

The UV data files inside `Apo2/` and `ATP2/` were named `Apo2.txt` and `ATP2.txt` respectively. MOLASS requires the UV file to end with `_UV.txt`. We renamed them locally:

| Folder | Original name | Renamed to |
|--------|--------------|------------|
| `Apo2/` | `Apo2.txt` | `Apo2_UV.txt` |
| `ATP2/` | `ATP2.txt` | `ATP2_UV.txt` |

`MY2/MY2_UV.txt` was already correctly named.

**Question for Shimizu**: Can you confirm whether this naming was intentional, or whether future datasets should follow the `PREFIX_UV.txt` convention?

---

## UV Elution Traces

Peak shapes are visually **identical** between each original/pre-averaged pair (see `01a_uv_traces.png`):

| Sample pair | Peak shape comparison |
|-------------|----------------------|
| Apo vs Apo2 | Single sharp peak — perfect overlay |
| ATP vs ATP2 | Main peak + small shoulder — perfect overlay |
| MY vs MY2   | Two resolved peaks — perfect overlay |

No anomalies (bubble artifacts, baseline drift, UV detector saturation) were observed in any dataset.

---

## SAXS Intensity Elution Traces

Integrated SAXS intensity profiles (see `01a_saxs_traces.png`) also show **identical peak shapes** between pairs. The pre-averaged datasets show visibly smoother baselines between and after peaks, consistent with noise reduction from frame averaging.

---

## S/N Comparison (UV channel)

| Dataset | UV peak (AU) | UV baseline SD | S/N ratio |
|---------|-------------|----------------|-----------|
| Apo     | 0.1388      | 0.000647       | 214.6     |
| Apo2    | 0.1388      | 0.000647       | **214.6** |
| ATP     | 0.0983      | 0.000440       | 223.5     |
| ATP2    | 0.0983      | 0.000440       | **223.5** |
| MY      | 0.0604      | 0.000664       | 90.8      |
| MY2     | 0.0604      | 0.000664       | **90.8**  |

**The UV S/N is identical between each original/pre-averaged pair** (to all displayed digits). This strongly suggests that the UV data files in the `*2` folders are identical to those in the originals, and that the 19-frame pre-averaging was applied only to the SAXS frames.

**Question for Shimizu**: Is this expected? We assumed the pre-averaging would apply to both UV and SAXS channels. If only SAXS was pre-averaged, the comparison in the MOLASS runs will reflect a SAXS-only effect, which is still scientifically useful but worth being explicit about.

---

## Notes on Individual Datasets

**MY / MY2 — most informative test case**  
MY has the most complex elution profile (two clearly separated peaks, see traces) and the lowest UV S/N (~91, vs ~215–224 for Apo/ATP). This makes it the most sensitive test for whether averaging order changes MOLASS decomposition results. We expect the most interesting findings here.

**Apo / Apo2 — simplest case**  
Single sharp peak, highest S/N (~215). Most likely to show identical MOLASS results regardless of averaging order.

**ATP / ATP2 — intermediate case**  
Main peak plus a smaller trailing shoulder. An intermediate test of whether peak boundaries shift with pre-averaging.

---

---

## MOLASS Decomposition Results (01b)

**Settings**: Default settings throughout — no manual parameter tuning. Pipeline: `SSD(folder)` → `trimmed_copy()` → `corrected_copy()` → `quick_decomposition()`.

### Summary table

| Dataset | Components found | Rg (Å) | Elution proportions |
|---------|-----------------|--------|---------------------|
| Apo     | 1 | 33.3 | 100% |
| Apo2    | 1 | 33.4 | 100% |
| ATP     | 1 | 32.9 | 100% |
| ATP2    | 1 | 32.8 | 100% |
| MY      | 2 | 32.3, 32.3 | 95%, 5% |
| MY2     | 3 | **97.0, 53.6, 32.4** | 5%, 5.5%, 89.5% |

### Apo and ATP: no meaningful difference

For both Apo/Apo2 and ATP/ATP2, MOLASS finds exactly 1 component and the Rg values agree to within 0.1 Å (< 0.5%). Pre-averaging does not change the decomposition result for these samples.

### MY vs MY2: decisive qualitative difference

**This is the most important finding.**

The original MY dataset and the pre-averaged MY2 dataset produce qualitatively different decompositions:

- **MY (original)**: 2 components, both with Rg ≈ 32.3 Å. This is likely an artifact — two components with identical Rg means MOLASS is splitting the UV elution peak (which has two UV peaks) into two contributions, but the SAXS does not resolve two distinct species.

- **MY2 (pre-averaged)**: 3 components with Rg = **97**, **53.6**, and **32.4** Å (proportions ≈ 5%, 5.5%, 89.5%). The large-Rg components are consistent with oligomeric aggregates (Rg = 97 Å ≈ tetramer, Rg = 53.6 Å ≈ dimer) co-eluting with the main monomer peak (Rg = 32.4 Å).

**Interpretation**: The higher SAXS signal quality in MY2 (from pre-averaging) gave MOLASS enough signal-to-noise to resolve aggregate populations that were buried in the noise in the original MY data. This is a **decisive qualitative difference** — not just a small shift in Rg, but the detection of species that were previously invisible.

**Question for Shimizu**: Is the presence of oligomeric aggregates expected in the MY sample? The Rg = 97 Å component in particular is substantial. This finding may be biologically significant independent of the averaging-order question.

### Conclusion so far

| Sample | Effect of pre-averaging |
|--------|------------------------|
| Apo, ATP | No meaningful effect (Rg unchanged, same number of components) |
| MY | **Decisive effect**: reveals aggregate populations hidden below noise floor in original |

This directly confirms the hypothesis from the research plan: pre-averaging matters most for samples where the optimization landscape is noise-sensitive — here because the aggregate signals are marginal relative to the noise in the original data.

Detailed pairwise comparison (elution curves, scattering profiles, etc.) will follow in the 01c notebook.

---

## Quantitative Pairwise Comparison (01c)

**Notebook**: `01c_comparison_analysis.ipynb`

### Simple pairs: Apo and ATP

| Pair | Rg_orig (Å) | Rg_avg (Å) | ΔRg (Å) | r P(q) | r elution |
|------|------------|-----------|---------|--------|-----------|
| Apo / Apo2 | 33.34 | 33.40 | 0.06 | 0.99999 | 0.99905 |
| ATP / ATP2 | 32.93 | 32.82 | 0.11 | 0.99999 | 0.99986 |

The Pearson correlation of the scattering profiles P(q) is **0.99999 for both pairs** — the profiles are numerically indistinguishable. The ΔRg values (0.06 and 0.11 Å) are well within normal Guinier fitting uncertainty. There is no meaningful effect of pre-averaging for these single-component, high-S/N samples.

### MY: monomer component is identical regardless of analysis mode

Three analysis variants were compared for the monomer (dominant) component:

| Analysis | Mode | Rg (Å) |
|----------|------|--------|
| MY default | 2 components | 32.30 |
| MY forced-3c | 3 components | 32.44 |
| MY2 default | 3 components | 32.42 |

Pearson r between all three monomer P(q) profiles: **≥ 0.99994**.

When MY is forced to find 3 components, it yields Rg ≈ 32.4, "N/A" (Guinier failed), 29.3 Å — no large-Rg species are found. Component quality scores (a blend of Rg distinctiveness and area proportion, range 0–1) confirm this quantitatively: the spurious components score **0.54 and 0.00**, with the middle component flagged as unreliable (Guinier fit failed). By contrast, all three components in MY2 score **1.00** and are flagged as reliable. The forced extra components are noise artifacts, not biological signal. **The underlying scattering data in MY simply does not contain sufficient signal for two aggregate components.**

By contrast, MY2 automatically finds genuine aggregate species (Rg = 97 and 54 Å) because the pre-averaged data has sufficient SAXS signal quality. This confirms that the qualitative difference (2 vs 3 components, absence vs presence of aggregates) is a **signal-to-noise effect**, not a difference in the physical sample.

### Key conclusion for Shimizu

The monomer in the MY sample is identical in both datasets (Rg ≈ 32.4 Å, r = 0.99994 across all analysis modes). The pre-averaged MY2 additionally reveals **two aggregate populations (Rg = 97, 54 Å) that are below the detection threshold of the original data**. Pre-averaging improves aggregate detection without altering the dominant-component result.

For Apo and ATP samples (single-component, clean), pre-averaging has no measurable effect.
