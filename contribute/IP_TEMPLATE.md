# IP Contribution Template

If you are bringing existing intellectual property to the commons — a pre-trained model, a proprietary dataset, a patent, or an existing product — fill this out instead of or in addition to `DOMAIN_TEMPLATE.md`.

Your IP is your leverage. This template describes what you're contributing, what you retain, and how revenue gets attributed to your contribution.

---

## What You're Contributing

Check all that apply:

- [ ] **Physics engine** — a frozen causal ODE trained on a physical domain from scratch. This is a Level 2 contribution. Read the section below before proceeding.
- [ ] **Pre-trained model** — an existing model that makes predictions in a physical domain
- [ ] **Proprietary dataset** — data you own or control access to
- [ ] **Patent or trade secret** — domain-specific IP that enables a conditioning layer that wouldn't otherwise be possible
- [ ] **Existing product** — a deployed product that makes AI recommendations in a physical domain

---

## Physics Engine (Level 2 Contribution)

Contributing a physics engine means building a new frozen causal ODE for a domain where none exists yet. This is what LINCR AI did for clinical anesthesia with MargamSim CF2.

**Before you build, answer these:**

**What physical domain are you modeling?**

**What is the ground truth signal?**
What does "the physics was right" mean in numbers?

**What dataset are you training on?**
N cases, time resolution, key channels.

**What is the causal training approach?**
A valid physics engine must use causal training — Pearl's do-calculus as a loss function, or equivalent. Pure correlation learning does not qualify. Describe how you enforce causal direction in your training.

**What freeze tests will you run?**
A physics engine must pass freeze tests before it can be accepted as a foundation layer:
- Constraint violations (0%)
- Intervention directionality (correct causal direction for all interventions)
- Rollout stability (bounded predictions at 15, 30, 60 min)
- Cross-dataset transfer (AUROC improvement must replicate on at least one held-out dataset not in training)

**Cross-dataset transfer is the critical test.** MargamSim CF2 achieved 0.991 AUROC zero-shot on MIMIC-IV after training on MOVER. If your engine only works on its training dataset, it learned correlation not dynamics. It will not be accepted as a foundation layer.

**What is your proposed foundation royalty structure?**
Every conditioning layer licensed against your engine pays you a royalty. Proposed %:

---

**To proceed:** open a discussion at `engines@lincr.ai` before building. The eval bar is higher than for conditioning layers and we want to align on methodology before you invest the training time.

---

## Pre-Trained Model

**What does your model do?**
What does it predict, in what domain, trained on what data?

**What are its performance numbers?**
On what dataset, with what metric? This is the baseline your conditioning layer will be compared against.

**What format are the weights in?**
PyTorch, TensorFlow, ONNX, other?

**What do you want to contribute?**
- [ ] Use my model as a conditioning layer initializer (warm start) — your weights initialize the conditioning layer before fine-tuning against the ODE
- [ ] Use my model as a teacher in a distillation setup — your model's predictions guide the conditioning layer during training
- [ ] Register my model as a standalone conditioning layer — your model maps directly to the ODE's input/output format

**What do you retain?**
You retain ownership of your original model weights. The conditioning layer trained from or with your model is jointly owned unless you specify otherwise.

**Proposed revenue split for conditioning layers that use your model:**

| Contributor | Role | Share |
|-------------|------|-------|
| Your model IP | Initialization / distillation | |
| ML Engineer who trains the conditioning layer | Training | |
| Domain Expert | Causal structure | |
| Other roles | ... | |

---

## Proprietary Dataset

**What does the dataset contain?**
Domain, N, time resolution, key channels, collection period.

**Who owns it?**
You, your institution, a data consortium?

**What access does it require?**
DUA, IRB, institutional approval, NDAs?

**What are you willing to contribute?**
- [ ] Full dataset access to a verified conditioning layer team
- [ ] Federated access only — the data never leaves my environment, teams train against it via the federated path
- [ ] Derived features only — I provide preprocessed inputs, not raw data
- [ ] Holdout set only — for validating a conditioning layer someone else trains

**Proposed dataset licensing terms:**

A dataset that enables a conditioning layer earns a permanent revenue share from any layer registered using it.

Proposed share: ___% of conditioning layer marketplace revenue, in perpetuity.

This share is separate from the team's role-based revenue split. Document both in `build/COMPANY_TEMPLATE.md`.

---

## Patent or Trade Secret

**What does your IP cover?**
Plain language description. You don't need to disclose the implementation here — just enough to establish what it enables.

**How does it improve the deviation score?**
Why would a conditioning layer built on your IP outperform one that isn't?

**What are you willing to license?**
- [ ] Exclusive license to LINCR AI for marketplace distribution
- [ ] Non-exclusive license — you can license independently outside the marketplace
- [ ] Cross-license — your IP to the commons, commons IP to you

**Proposed IP licensing terms:**

---

## Existing Product

**What does your product do?**
What AI recommendations does it make, in what domain, for what customer?

**What would the deviation score add?**
How does your product change if it can tell a customer "this recommendation was backed by physics"?

**What integration are you proposing?**
- [ ] Your product calls the Margam API and displays the deviation score alongside its existing output
- [ ] Your product contributes real-world outcome data back to the commons (improving the eval baseline)
- [ ] Your product registers as a conditioning layer — your AI becomes the domain layer

**What do you want in return?**
- [ ] API access at partner pricing
- [ ] Co-marketing — "built on Margam Physics"
- [ ] Revenue share for outcome data you contribute
- [ ] Other: ___

---

## What You Retain

In all cases:
- You retain ownership of the IP you bring
- The conditioning layer trained using your IP is jointly owned unless you specify full assignment
- Your revenue share is locked at the time your IP is registered — it doesn't change as the conditioning layer earns

---

## Contact

To discuss IP contributions before committing: `ip@lincr.ai`

*Submit this file as a PR to `contribute/ip/your_name_domain.md`.*
