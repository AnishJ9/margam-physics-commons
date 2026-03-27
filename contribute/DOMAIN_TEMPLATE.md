# Domain Contribution Template

Fill this out in plain language. You don't need to write code.

---

## Your Domain

**What physical system are you modeling?**
(e.g., "ICU patients during mechanical ventilation", "turbine blade fatigue under cyclic load", "power grid frequency during demand spikes")

**What does "the physics was right" mean in your domain?**
This is your ground truth signal — the thing that tells you whether a prediction was accurate.
(e.g., "MAP stayed above 65 mmHg", "blade did not fracture within predicted cycle count", "grid frequency stayed within 0.2 Hz of nominal")

---

## Your Dataset

**What dataset are you using?**
Name, source, approximate size, time resolution, key channels.

**Is it public or private?**
Public: link it. Private: we'll use the federated training path — your data never leaves your machine.

**What are the input channels?**
List the measurements your system records. Time-series signals, not derived features.

---

## The Causal Structure

**What interventions matter in your domain?**
List the things someone does that causally affect the physical outcome.
(e.g., "vasopressor administration raises blood pressure", "reducing turbine RPM reduces stress")

**What is the causal direction of each intervention?**
Does this intervention increase or decrease the ground truth signal?
Mark each as +1 (increases) or -1 (decreases).

| Intervention | Direction | Notes |
|-------------|-----------|-------|
| | | |
| | | |

**What are the confounders?**
Things that are correlated with the outcome but don't cause it.
(e.g., "vasopressors are given when blood pressure is already low — the model must learn they raise it, not lower it")

---

## Your Expertise

**How long have you worked in this domain?**

**What do practitioners in your domain know that datasets don't capture?**
This is the most valuable thing you can contribute. What does experience tell you that the numbers alone don't show?

**What failure modes do you see most often?**
Cases where a model would get it wrong because it learned the correlation not the cause.

---

## Contact

**Name:**
**Affiliation (optional):**
**How to reach you:**
**Contributor wallet address (for marketplace payments):**

---

*Submit this file as a PR to `contribute/domains/your_domain_name.md`. Someone will help you convert it into a training specification.*
