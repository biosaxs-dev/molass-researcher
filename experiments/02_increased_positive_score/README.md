# Experiment 02: Increased Positive Scores in Guinier Analysis Report

**Issue**: [molass-library #4](https://github.com/biosaxs-dev/molass-library/issues/4)  
**Date started**: March 11, 2026  
**Status**: ✅ Root cause identified — fix in progress  

---

## Observation

After migrating the analysis report (Excel workbook) to the new library, the Guinier analysis chart shows a significant increase in "positive scores" — frames for which the Guinier fit is judged valid/successful.

The numeric summaries (Rg values etc.) appear nearly identical between old and new, so the migration itself looks correct. The question is why *more frames pass the Guinier quality test* in the new version.

---

## What Is a "Positive Score"?

In the Guinier chart, each frame is marked as either:
- **Positive (valid)**: the Guinier fit passed quality criteria (good linearity in ln I vs q², qRg range, etc.)
- **Negative (rejected)**: the fit failed or was outside acceptable bounds

A higher positive count means more frames are considered usable — which could reflect:
- Genuinely improved data quality
- A relaxed or changed acceptance criterion
- A bug in the old rejection logic that was fixed
- A bug in the new acceptance logic that is too permissive

---

## Key Question

> What changed between the old (legacy) and new (library) implementations that affects the Guinier fit acceptance criterion?

---

## AI Collaboration Note

The primary evidence in issue #4 is an image (Guinier chart comparison). Since Copilot cannot read image content, we use this `.md` file to:

1. Capture what the image shows in text/numeric form (filled in by the human)
2. Build hypotheses from that description
3. Write notebook experiments to test each hypothesis computationally

---

## Image Description (to be filled in)

*Please describe or quantify what the chart shows. For example:*

- Old version: ___ positive frames / ___ total = ____%
- New version: ___ positive frames / ___ total = ____%
- Are the extra positives concentrated in a particular region (e.g., near the peak, the tails)?
- Do the accepted frames look physically reasonable (Rg values consistent with the rest)?

---

## Hypotheses

To be refined once the image is described. Candidate causes:

| # | Hypothesis | Testable? |
|---|-----------|-----------|
| H1 | Acceptance criterion (qRg range, linearity threshold) differs between legacy and library | Yes — compare source |
| H2 | q-range used for fitting changed (different q-min/q-max selection) | Yes — compare source |
| H3 | Error weighting changed → noisier frames now fit better | Yes — compare source |
| H4 | Frames near peak are correctly included now (bug fix) | Yes — run both on same data |
| H5 | Too-permissive criterion introduced in new code (regression) | Yes — unit test |

---

## Investigation Plan

### Step 1 — Source comparison
Find where the Guinier acceptance criterion is implemented in:
- `molass-legacy` (old)
- `molass-library` (new)

Compare the logic side by side.

### Step 2 — Quantify the difference
Write a notebook (`02a_score_comparison.ipynb`) that:
- Runs `molass-library` Guinier analysis on the same dataset
- Counts positive/negative scores per frame
- Plots the result in a form equivalent to the Excel chart

### Step 3 — Identify the cause
Based on source comparison + notebook output, narrow down which hypothesis holds.

### Step 4 — Decide: fix or document
- If the new behavior is correct → document as intentional improvement, close issue #4
- If it's a regression → fix and add a test

---

## Findings (March 11, 2026)

### Root Cause

The increased `positive_score` is caused by **`corrected_copy()` subtracting a negative baseline**, which shifts all intensities upward and mechanically increases `positive_ratio` per frame.

The negative baseline arises from the library's LPM implementation using a **hardcoded `p_final=10%`** (i.e., `PERCENTILE_FINAL=10` in `ScatteringBaseline.solve()`), while the legacy computes `p_final` **adaptively** per q-row using:

```python
noisiness = std(row - spline_fit(row))
p_final = base_percentile_offset(noisiness, size_sigma=size_sigma)
```

For SAMPLE1 at high-q (pure noise regime, q ≈ 0.221):
- Library: `p_final = 10%` → baseline intercept = −0.000504 → `positive_ratio` mean = **0.899**
- Legacy: `p_final = 28.6%` → baseline intercept = −0.000216 → `positive_ratio` mean = **0.716**
- Trimmed (no correction): `positive_ratio` mean = **0.627**

The adaptive `p_final` places the final baseline anchor at a higher percentile of the residuals, closer to zero, resulting in a baseline much nearer zero and far less positive shift.

### Call chain

```
corrected_copy()
  └─ xr.get_baseline2d()
       └─ Baseline2D.individual_axes(method='linear')
            └─ _lpm_individual_axes_impl()
                 └─ compute_lpm_baseline()
                      └─ ScatteringBaseline(row, x=frames).solve()
                           # solve() uses hardcoded p_final=PERCENTILE_FINAL=10
```

### What the legacy does differently

```
ScatteringBaseCorrector.correct_all_q_planes()
  └─ correct_a_single_q_plane(i)
       └─ noisiness = std(row - LSQUnivariateSpline(row))
          p_final = base_percentile_offset(noisiness, size_sigma)
          ScatteringBaseline(row, curve=ecurve).solve(p_final=p_final)
```

### Fix

Implement adaptive `p_final` in `compute_lpm_baseline()` in `molass-library/molass/Baseline/LpmBaseline.py`.
Pass `size_sigma` (computed from the integrated elution curve) via `method_kwargs` through `_lpm_individual_axes_impl`.

---

## Files in This Folder

| File | Description |
|------|-------------|
| `README.md` | This file — investigation plan and running log |
| `02a_score_comparison.ipynb` | Notebook: `positive_ratio` comparison, LPM diagnosis, adaptive p_final fix |
| `02a_positive_ratio_comparison.png` | Per-frame positive_ratio: trimmed vs corrected |
| `02a_iq_profiles.png` | I(q) profiles at tail/peak frames before/after correction |
| `02a_baseline2d_inspection.png` | LPM baseline surface (confirmed negative, ~−0.0005) |
| `02a_lpm_anchor_inspection.png` | LPM anchor frames for mid-q row (all 61 anchors negative) |
| `02a_curve_effect.png` | Effect of passing curve= to ScatteringBaseline (none for SAMPLE1) |
| `02a_asls_vs_lpm.png` | pybaseline asls 2D vs LPM (asls is worse, 0.937) |
| `02a_weighted_asls.png` | Buffer-weighted asls (no improvement vs unweighted) |
| `02a_adaptive_pfinal.png` | Adaptive p_final=28.6% vs fixed 10%: positive_ratio drops to 0.716 |

---

## Running Log

### March 11, 2026
- Created experiment folder and this README
- Issue #4 read: observation is increased positive scores after Excel report migration
- Fixed prerequisite bug in `molass_legacy/LRF/PnoScdMap.py` (list→array for peak_top_x)
- Built `02a_score_comparison.ipynb` with 20 cells
- Root cause confirmed: adaptive `p_final` in legacy vs fixed 10% in library
- Fix to be implemented in `molass-library/molass/Baseline/LpmBaseline.py`
