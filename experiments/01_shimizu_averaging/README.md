# Experiment 01: Averaging Order Effect on MOLASS Decomposition

**Collaborator**: Shimizu  
**Date started**: March 6, 2026  
**Status**: 🔬 In progress  
**Data**: `Dropbox\MOLASS\DATA\20260305` (see [DATA_SOURCES.md](../../DATA_SOURCES.md))

---

## Research Question

> Does pre-averaging 19 data frames **before** passing to MOLASS produce materially different decomposition results compared to MOLASS's internal default averaging?

MOLASS by default averages frames internally during processing. Shimizu's question: if you pre-compute the 19-frame average externally (using MOLASS's averaging tool) and supply that single averaged dataset, does the downstream decomposition change — and if so, does it change decisively?

---

## Dataset

| Dataset | Sample | UV λ | S/N level |
|---------|--------|------|-----------|
| `Apo`   | Apo protein | 280 nm | High (original) |
| `ATP`   | ATP-bound   | 290 nm | High (original) |
| `MY`    | MY          | 290 nm | High (original) |
| `Apo2`  | Apo protein | 280 nm | Very high (19-frame pre-average) |
| `ATP2`  | ATP-bound   | 290 nm | Very high (19-frame pre-average) |
| `MY2`   | MY          | 290 nm | Very high (19-frame pre-average) |

Baseline wavelength: **400 nm** (same for all).  
Note: All original datasets already have unusually good S/N compared to typical SEC-SAXS data.

---

## Why This Is Non-Trivial

**The linear intuition** (why you'd expect no difference):
- Frame averaging is linear: $\bar{M} = \frac{1}{N}\sum_i M_i$
- If decomposition were linear, pre-averaging and post-averaging would commute

**The nonlinear reality** (why it might matter):
- MOLASS decomposition is nonlinear: optimization + regularization + constraint application
- Higher S/N sharpens the cost function landscape → potentially different local minima
- Pre-averaging changes the effective noise floor, which affects:
  - Peak boundary detection
  - Rank of the effective data matrix
  - Sensitivity to regularization parameter λ
  - Stability of the R-matrix determination

**Hypothesis**: Results will likely be similar for well-separated peaks, but pre-averaged data may show decisive improvement for samples with marginal peak separation — where the optimization landscape matters most.

---

## Expected Outcomes

| Outcome | Interpretation |
|---------|----------------|
| Identical results | MOLASS is robustly insensitive; internal averaging is sufficient |
| Small quantitative differences | S/N affects fine-grained quantities ($R_g$, $I(0)$) but not structural conclusions |
| Decisive qualitative differences | Pre-averaging changes optimization basin; nonlinearity is operationally significant |
| Sample-dependent differences | Overlap structure matters more than S/N alone |

---

## Analysis Notebooks

| Notebook | Purpose | Status |
|----------|---------|--------|
| [01a_data_exploration.ipynb](01a_data_exploration.ipynb) | Visual QC: UV/SAXS traces for all 6 datasets | ✅ |
| [01b_molass_runs.ipynb](01b_molass_runs.ipynb) | Run MOLASS with default settings on all 6 | ✅ |
| [01c_comparison_analysis.ipynb](01c_comparison_analysis.ipynb) | Pairwise comparison and interpretation | ⏳ |

---

## Findings

### 01b — MOLASS runs (March 6, 2026)

| Dataset | Components | Rg (Å) | Proportions |
|---------|-----------|---------|-------------|
| Apo     | 1 | 33.34 | 1.000 |
| Apo2    | 1 | 33.40 | 1.000 |
| ATP     | 1 | 32.93 | 1.000 |
| ATP2    | 1 | 32.82 | 1.000 |
| MY      | 2 | 32.30, 32.32 | 0.947, 0.053 |
| MY2     | 3 | 97.04, 53.62, 32.42 | 0.050, 0.055, 0.895 |

**Key finding**: MY and MY2 give qualitatively different decompositions. Original MY: 2 components both with Rg = 32.3 Å (suspicious, likely artifact). Pre-averaged MY2: 3 components with Rg = 97, 53.6, 32.4 Å — plausible aggregate detection enabled by higher S/N.
**Apo and ATP**: Rg agrees to within 0.1 Å between original and pre-averaged. No meaningful difference.

### 01a — Data exploration (March 6, 2026)
- All 6 datasets loaded successfully (needed to rename `Apo2.txt`→`Apo2_UV.txt`, `ATP2.txt`→`ATP2_UV.txt` to match `_UV.txt` convention).
- Peak shapes are identical between original and pre-averaged pairs (normalized UV and SAXS overlays).
- UV S/N is **identical** between pairs — SAXS frames appear to be the pre-averaged data; UV data may be unchanged.
- **MY** has the most complex elution (2 peaks, lowest S/N ~91) → most informative test case for the averaging-order question.
- All 6 datasets cleared for MOLASS runs → proceed to `01b`.

---

## Connection to Theory

This experiment directly illustrates concepts from `modeling-vs-model_free`:
- The R-matrix framework predicts that optimization landscape topology (local minima structure) depends on data quality
- Higher S/N → sharper χ² landscape → potentially more reliable R-matrix determination
- Bullets 3–4 of the "why hard" analysis: singularity barriers and optimization trapping are noise-sensitive

See [RESEARCH_PLAN.md](../../RESEARCH_PLAN.md) for full planning context.
