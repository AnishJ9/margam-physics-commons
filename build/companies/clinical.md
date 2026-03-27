# Company: Clinical Physics Layer (LINCR AI)

This is the reference implementation. The clinical physics layer was the first conditioning layer trained on the frozen ODE core. It is the existence proof that the contribution model works.

---

## The Domain

**Physical system:** Intraoperative and ICU patient physiology during anesthesia and critical care

**Ground truth signal:** Mean arterial pressure stayed above 65 mmHg for 15 minutes following the prediction window

**Customer:** Hospital quality improvement committees, anesthesia departments, ICU directors

**Decision informed:** Which completed cases had physiological trajectories that departed most from what the physics predicted — and what interventions, if any, were associated with that departure

---

## The Stack

| Role | Person | Contribution |
|------|--------|--------------|
| Domain Expert | Anish Joseph, CAA | 20 years anesthesia. Causal structure: TED FARIOS intervention map. Ground truth: MAP ≥ 65 mmHg. |
| ML Engineer | Anish Joseph | CF2 architecture, contrastive causal training, 5-channel freeze tests |
| Data Engineer | Anish Joseph | MOVER dataset (55,483 cases), 25-channel preprocessing pipeline |
| Regulatory | Anish Joseph | 520(o)(1)(E) CDS exemption. Retrospective QI, not real-time clinical decision support. |
| Product | Anish Joseph | QI report: deviation score + tier assignment + case narrative. Reviewed by QI committee, not used for individual patient care. |

---

## The Dataset

**Training:** MOVER — 55,483 intraoperative cases, 1-minute averaged, 25 channels

**Validation:**
- MIMIC-IV (zero-shot): 0.991 AUROC@15
- eICU (zero-shot): 0.984 AUROC@15
- VitalDB (zero-shot): 0.947 AUROC@15

All validation datasets are public. Eval harness is reproducible.

---

## The Physics Standard

**Baseline:** 0.873 AUROC@15 (standard clinical early warning score)

**CF2 result:** 0.972 AUROC@15 on held-out MOVER data

**Delta:** +0.100

**Ablation:** Contrastive causal training vs non-contrastive baseline on same architecture: Δ = +0.014. The causal direction matters.

---

## The Regulatory Path

**Classification:** Clinical Decision Support tool

**Exemption:** 21 U.S.C. 520(o)(1)(E) — not intended to replace clinical judgment, displays its basis, allows independent clinician review

**What it is:** Retrospective QI analysis of completed cases. Not real-time. Not used for individual patient care decisions.

**What it is not:** A diagnostic device, a therapeutic device, a real-time monitoring system.

---

## Revenue Attribution

LINCR AI holds this layer. Revenue from clinical licensing flows to LINCR AI.

---

## Open Roles

This layer is fully staffed. It is listed here as a reference for other teams building domain layers.

---

## What Other Teams Can Learn From This

1. **The domain expert is the bottleneck — in a good way.** The causal structure (what interventions raise MAP, what confounders make it look like they lower it) is what makes the deviation score valid. Time spent getting that right compounds across every dataset the layer is validated on.

2. **Zero-shot transfer is the test that matters.** Training on MOVER and validating on MIMIC-IV, eICU, and VitalDB was not planned — it emerged from the architecture. If your conditioning layer only works on the dataset it was trained on, the physics isn't generalizing. That's a signal.

3. **Regulatory classification first.** Knowing this was a retrospective QI tool shaped everything: the product spec, the pilot design, the claims. Build the regulatory classification before the product spec, not after.

4. **The paper is the distribution.** Submitting to NeurIPS created a citation path. Academic users cite the paper. Commercial users discover it through the academic users. The paper is part of the go-to-market.

---

*Registered: 2026*
*Layer version: CF2 (epoch 3, val_auroc=0.9724)*
*Core checkpoint: MargamSim CF2*
*Paper: Joseph 2026, NeurIPS*
