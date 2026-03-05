# molass-researcher: Concept & First Experiment Plan

**Date**: March 6, 2026  
**Status**: 🔬 In progress  
**Participants**: Takahashi + Copilot  
**Trigger**: Shimizu (collaborator) provided new SEC-SAXS dataset with averaging question

---

## 1. Repo Concept: `molass-researcher`

### What it is
A GitHub repository for **AI-augmented experimental data research** — the counterpart to `molass-tutorial` (teaching) and `molass-technical` (theory). Where those repos deliver content, `molass-researcher` documents the *process* of doing research with real data.

### Target audience
- Research collaborators with real experimental questions
- People who want to see how AI + Jupyter + MOLASS work together on actual data
- Readers of Paper (2) who want a concrete scientific example to contrast with the governance example (kannondai-community)

### Contrast with existing repos

| Repo | Content type | AI role | Audience |
|------|-------------|---------|----------|
| `molass-tutorial` | Step-by-step instruction | Passive | Students |
| `molass-technical` | Theory exposition | Passive | Developers |
| `modeling-vs-model_free` | Mathematical research | Active collaborator | Theorists |
| **`molass-researcher`** | **Experimental research** | **Active collaborator** | **Collaborating researchers** |

### Key design principle
Each notebook documents a **real question from a real collaborator**, answered with **real data**, with the AI reasoning process visible. This is the empirical science counterpart to the mathematical research in `modeling-vs-model_free`.

### Connection to Paper (2)
- `modeling-vs-model_free` demonstrates AI-augmented **theoretical** research (programmer + AI → foundational math)
- `molass-researcher` demonstrates AI-augmented **experimental** research (researcher + AI → data-driven insight)
- Together they show the literacy generalizes across research modes, not just domains
- Both use the same infrastructure: COPILOT-INIT.md + AI_CONTEXT_STANDARD.md + Jupyter

---

## 2. First Experiment: Shimizu's Averaging Order Question

### Context
Shimizu (March 5–6, 2026) provided new SEC-SAXS data at:
```
Dropbox\MOLASS\DATA\20260305
```

### Dataset
| Sample | UV wavelength | Raw data | Pre-averaged data |
|--------|--------------|----------|-------------------|
| Apo    | 280 nm       | `Apo`    | `Apo2`            |
| ATP    | 290 nm       | `ATP`    | `ATP2`            |
| MY     | 290 nm       | `MY`     | `MY2`             |

- Baseline wavelength: 400 nm (same for all)
- Pre-averaged: 19-frame average computed with MOLASS's averaging tool before analysis
- All raw data already has unusually good S/N; averaged versions have even better S/N

### Research Question
> Does pre-averaging the data (before passing to MOLASS) change decomposition results decisively, compared to letting MOLASS average internally during processing?

### Background: Why This Is Non-Trivial
MOLASS averages frames internally by default. Shimizu's question: what if you supply the pre-averaged single dataset instead?

**The linear intuition** (why you'd expect no difference):
- Averaging is a linear operation: $\bar{M} = \frac{1}{N}\sum_i M_i$  
- If decomposition were linear, averaging before or after would give the same result

**The nonlinear reality** (why it might matter):
- MOLASS's decomposition is nonlinear: optimization + regularization + constraint application
- S/N affects the **optimization landscape**: higher S/N → sharper cost function → different local minima structure
- Pre-averaging changes the effective noise floor, which affects:
  - Which elution peak boundaries get detected
  - How well the rank-2 (or rank-3) approximation fits
  - Stability of the R-matrix determination
  - Sensitivity to regularization parameter λ

**Hypothesis**: The result will likely be similar for clean cases, but the pre-averaged version may show decisive improvement for peaks with marginal separation — exactly where the optimization landscape matters most.

### Expected Outcomes and Their Meaning
| Outcome | Interpretation |
|---------|----------------|
| Identical results | MOLASS is robustly insensitive to pre-averaging; internal averaging is sufficient |
| Small quantitative difference | S/N affects fine-grained quantities ($R_g$, second virial coefficient) but not structural conclusions |
| Decisive qualitative difference | Pre-averaging changes which decomposition basin the optimizer finds; nonlinearity is operationally significant |
| Difference varies by sample (Apo vs ATP vs MY) | Sample-dependent — overlap structure matters, not just S/N |

### Analysis Plan

**Step 1: Basic quality check**  
- Plot UV and SAXS traces for all 6 datasets  
- Confirm wavelength assignments (280/290/400 nm)  
- Visually assess elution peak shapes and overlap  

**Step 2: Run MOLASS on all 6 datasets with default settings**  
- Use identical parameters across all runs  
- Record decomposition results: $P$, $C$, $R_g$, fit quality ($\chi^2$)  

**Step 3: Pairwise comparison (original vs pre-averaged)**  
For each sample pair (Apo vs Apo2, ATP vs ATP2, MY vs MY2):  
- Compare elution curves $C$: shape, peak positions, overlap fractions  
- Compare scattering profiles $P$: $R_g$, $I(0)$, Kratky plot features  
- Compare R-matrix (if accessible): how far from identity? (This links to `modeling-vs-model_free` theory)  
- Quantify difference: Pearson $r$ between curves, $\Delta R_g$, $\Delta \chi^2$  

**Step 4: Interpretation**  
- Identify which samples show the largest difference and why  
- Connect to theory: is the difference consistent with the optimization landscape picture?  
- Write up conclusions with explicit uncertainty statements  

### Notebooks
```
experiments/01_shimizu_averaging/
  01a_data_exploration.ipynb     — visual QC of all 6 datasets
  01b_molass_runs.ipynb          — MOLASS analysis, parameter recording
  01c_comparison_analysis.ipynb  — pairwise comparison and interpretation
  README.md                      — experiment context (condensed)
```

---

## 3. Repo Structure

```
molass-researcher/
  COPILOT-INIT.md              — AI initialization
  README.md                    — What this repo is and how to use it
  RESEARCH_PLAN.md             — this file
  EXPERIMENT_LOG.md            — chronological log of all experiments
  DATA_SOURCES.md              — where data lives (not in git)
  molass-researcher.code-workspace  — 2-repo workspace (+ molass-library)

  experiments/
    01_shimizu_averaging/      — First experiment (Shimizu, March 2026) ✅
    02_.../                    — Future experiments

  shared/
    utils.py                   — Shared plotting/analysis helpers
```

---

## 4. Next Steps

| Step | Action | Status |
|------|--------|--------|
| 1 | Document this plan | ✅ Done |
| 2 | Create `molass-researcher` GitHub repo | ✅ Done (March 6, 2026) |
| 3 | Set up COPILOT-INIT.md and repo scaffold | ✅ Done |
| 4 | Open dedicated 2-repo workspace (`molass-researcher.code-workspace`) | ✅ Done |
| 5 | Create `01a_data_exploration.ipynb` | ✅ Done |
| 6 | Set `DATA_ROOT` in notebook and run exploration | ⏳ Next |
| 7 | Run `01b_molass_runs.ipynb` and `01c_comparison_analysis.ipynb` | ⏳ |
| 8 | Update `PAPER_VISION_DISCUSSION.md` with this as Paper (2) evidence | ⏳ |

---

## 5. Why Start Here?

This experiment is ideal as `molass-researcher`'s first notebook because:

1. **Concrete, answerable question** — not exploratory, has a clear expected outcome
2. **Real collaborator, real data** — not synthetic; this matters for Paper (2)
3. **Connects to theory** — the answer directly illustrates why nonlinear optimization landscape matters (links back to `modeling-vs-model_free` Bullets 3–4)
4. **Low-risk** — 6 datasets, same analysis repeated; even a null result is publishable ("pre-averaging doesn't matter in practice")
5. **Good first AI-collaboration story** — Shimizu asks question → Takahashi sets up repo → Copilot helps design and execute analysis → findings reported back to Shimizu
