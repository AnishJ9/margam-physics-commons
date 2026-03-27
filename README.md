# Margam Physics Commons

**AI systems that operate in the physical world should be accountable to physics. Right now none of them are. This is the layer that makes that possible.**

A causal neural ODE — 64K parameters, trained to learn the direction of cause not the pattern of correlation — achieved AUROC 0.972 on held-out clinical data, 0.991 on MIMIC-IV, 0.984 on eICU. Cross-dataset transfer improves with distance from training domain. That's not memorization. That's dynamics learning.

Medicine was the proof of concept. The architecture generalizes to any physical domain.

---

## What This Is

A frozen causal model of a physical system becomes the reference frame for every AI operating in that domain. The deviation score — how far a trajectory departed from what physics predicted — is the universal metric for AI accountability in physical domains.

A registered physics layer is a product. A product needs a full company to reach a customer. This repo is the operating system for building that company.

---

## Two Levels of Contribution

There are two fundamentally different things you can contribute. The distinction matters for what you own and what you earn.

### Level 1 — Conditioning Layer

A conditioning layer sits on top of an existing frozen physics engine. You're teaching the engine your domain — mapping your inputs, encoding your interventions, shaping the deviation score for your use case. The physics engine doesn't change. Your layer extends it.

**Your contribution:** domain expertise, dataset, training.
**What you own:** the conditioning layer.
**What you earn:** marketplace revenue when your layer is licensed.

### Level 2 — Physics Engine

A physics engine is a frozen causal ODE trained on a physical domain from scratch. MargamSim CF2 is the first one — trained on 55,483 intraoperative cases, achieving 0.972 AUROC@15 on held-out data and 0.991 zero-shot on MIMIC-IV.

If you have a physical domain where no frozen causal model exists yet, and you have the data and expertise to build one, you can contribute the physics engine for that domain. Every conditioning layer built on top of your engine pays you a foundation royalty. Your engine is the infrastructure; conditioning layer contributors build on it.

**Your contribution:** causal ODE architecture, training pipeline, frozen checkpoint.
**What you own:** the physics engine for your domain.
**What you earn:** foundation royalty on every conditioning layer licensed against your engine.

To contribute a physics engine: fill out `contribute/IP_TEMPLATE.md` (physics engine section) and open a discussion before building. The eval bar is higher — your engine must demonstrate cross-dataset transfer before it's accepted as a foundation layer.

---

## Bring Your IP

If you already have something — a pre-trained model, a proprietary dataset, a patent, or a deployed product — fill out `contribute/IP_TEMPLATE.md`. Your IP is your leverage. The framework attributes revenue to what you bring, not just what you do.

- **Pre-trained model:** your weights initialize or guide the conditioning layer. You own the initializer. You get a permanent share of what the layer earns.
- **Proprietary dataset:** your data enables a domain that wouldn't otherwise exist. Dataset licensing earns a permanent share of any conditioning layer registered against it.
- **Patent or trade secret:** domain-specific IP that makes a conditioning layer work better than one built without it. Licensable through the marketplace.
- **Existing product:** add the deviation score to what you already ship. "This recommendation is accountable to physics" is the claim your product gets to make.

---

## Find Your Role

You don't need to be an ML engineer to contribute. Every function in a company has a role here. Pick yours.

| Role | What You Bring | Where to Start |
|------|---------------|----------------|
| Domain Expert | Knows what "physics was right" means in your field | `contribute/DOMAIN_TEMPLATE.md` |
| Data Engineer | Can access or curate a dataset | `build/roles/data-engineer.md` |
| ML Engineer | Can train and evaluate a conditioning layer | `contribute/train_layer.py` |
| Product | Knows the customer problem and product shape | `build/roles/product.md` |
| Sales / BD | Knows the procurement path and the right stakeholders | `build/roles/sales.md` |
| Marketing | Can position and pitch the deviation score to buyers | `build/roles/marketing.md` |
| Regulatory | Knows the approval path in your domain | `build/roles/regulatory.md` |
| Finance | Can model unit economics and structure a company | `build/roles/finance.md` |
| Legal | Can handle licensing, pilots, and IP assignment | `build/roles/legal.md` |
| Operations | Can run the day-to-day | `build/roles/operations.md` |

**Don't see your role?** Add it. The roles directory is open. If your function helps get a physics layer to a customer, it belongs here. See `build/roles/ROLES.md` for how to add one.

---

## Start a Company

A conditioning layer is an asset. It pays you every time it's licensed. Getting it to market requires a full stack — domain knowledge, data, training, product, sales, and the regulatory path for your domain.

The fastest way to start:

**The fastest way to start:** clone this repo, open Claude Code, and describe your domain or role in plain language. The `CLAUDE.md` in the root tells Claude Code exactly what this project is and how to help you — it will walk you through the right path for your role without you needing to read all of this first.

### 1. Find your domain
Anything where AI makes recommendations that affect physical outcomes.
- Clinical: ICU, OR, emergency, radiology
- Aerospace: flight dynamics, structural integrity
- Energy: grid stability, turbine performance
- Automotive: vehicle dynamics, safety systems
- Any physical system with a measurable ground truth

### 2. Assemble your stack
Use `build/COMPANY_TEMPLATE.md` to map out who you need. You don't need everyone on day one. You need to know which roles are filled and which are open.

### 3. Describe the physics
Fill out `contribute/DOMAIN_TEMPLATE.md`. In plain language:
- What physical system are you modeling?
- What does "the physics was right" mean? (this is your ground truth signal)
- What dataset do you have or know about?
- What interventions matter? What are their causal directions?

You don't need to write code to start. Describe your expertise. AI does the rest.

### 4. Train your conditioning layer

Open Claude Code in this repo. Tell it your domain and point it at your dataset. The `CLAUDE.md` tells Claude Code exactly how to help you — it will convert your domain template into a training spec and walk you through the training run.

If you prefer to run it directly:
```bash
# Training pipeline — coming in v0.2
# For now: open Claude Code and describe your domain
```

The frozen ODE core never changes. You're teaching it your domain, not modifying the physics engine.

### 5. Run the eval

```bash
# Eval harness — coming in v0.2
# For now: Claude Code will run the eval and report the deviation score improvement
```

The eval harness computes the deviation score improvement. The physics decides whether your contribution helped. No committee. No review. The number is the answer.

### 6. Register your layer
If your layer passes the eval threshold, submit a PR. Your layer gets registered in the marketplace with contributor addresses for every role that built it. Every license generates automatic payment, distributed to the team.

---

## Contribute to the Architecture

The architecture is described in full in the NeurIPS 2026 paper. Improvements to the ODE structure, the contrastive loss, the encoder, or the observer are welcome. Submit architectural contributions as a PR with:
- What you changed and why
- Eval results on at least one dataset against the CF2 baseline
- An ablation showing the delta

Architectural improvements that pass the eval threshold get versioned into the next frozen checkpoint. You get credited in the version history.

What stays proprietary: the specific patent claims (collective physiological entropy as distributed physical entropy source; lossless meaning transmission via state space transforms). Those are licensed separately. See `LICENSE.md`.

---

## The Proof

The clinical physics layer is the existence proof. These numbers are reproducible with the eval harness in this repo.

| Dataset | AUROC@15 | Baseline | Δ |
|---------|----------|----------|---|
| MOVER (training domain) | 0.972 | 0.873 | +0.100 |
| MIMIC-IV (zero-shot) | 0.991 | — | — |
| eICU (zero-shot) | 0.984 | — | — |
| VitalDB (zero-shot) | 0.947 | — | — |

Ablation: contrastive causal training (Pearl's do-calculus as loss function) vs non-contrastive baseline on same architecture. Δ = +0.014 AUROC@15. The causal direction matters.

Paper: submitted NeurIPS 2026.

---

## The Architecture

```
GRUEncoder(25ch) → StateInitializer → SimODEFunc(cardio:27/resp:8/pk:14) → Observer
                                              ↑
                                    Your conditioning layer goes here
                                    Your architectural contributions go here
```

63,975 parameters. Smaller than a spam filter. The physics engine is frozen. Your domain expertise goes into the conditioning layers that sit on top of it. Your architectural improvements get evaluated against the frozen baseline and, if they pass, become the next frozen baseline.

---

## The Marketplace

Physics adjudicates value. You don't negotiate payment. The deviation score improvement determines it automatically.

- Contribute a conditioning layer → get paid when it gets licensed
- Contribute a role to a team that ships a layer → get paid your share
- Improve the architecture → get credited in the version history
- Improve the eval harness → get credited in the physics standard versioning
- Validate against a new dataset → your name on the benchmark result

Full marketplace spec: `docs/MARKETPLACE.md`

---

## Open Problems

1. **Entropy extraction rate** — how many cryptographically hard bits per second can be extracted from the 49-dimensional trajectory? Which dimensions carry the most entropy?
2. **PPG-to-ODE mapping** — map consumer-grade photoplethysmography input into the CF2 input format. Makes the architecture accessible from a phone camera.
3. **Higher-resolution training** — CF2 was trained on 1-minute averaged data. Training on higher-frequency signals opens the TRNG application. MIMIC waveform data exists.
4. **New domain conditioning layers** — aerospace, energy, automotive. If you have the domain and the data, the architecture is ready.
5. **Multi-domain transfer** — does a conditioning layer trained on aerospace dynamics improve clinical deviation scores? The cross-domain transfer properties are unexplored.

---

## Legal

Research license. Commercial use requires a separate agreement. See `LICENSE.md`.

The frozen core (MargamSim CF2) is proprietary. The architecture (described in the NeurIPS paper), the conditioning layer framework, the eval harness, and the contribution framework are open under the research license.

Contributing a conditioning layer grants LINCR AI a license to distribute it through the marketplace. You retain ownership. You get paid when it's used.

---

## Citation

```
@article{joseph2026margam,
  title={MargamSim CF2: Causal Physiological Dynamics for Cross-Domain AI Accountability},
  author={Joseph, Anish},
  journal={NeurIPS},
  year={2026}
}
```

---

*LINCR AI — Atlanta, 2026*
*US Provisional Patent Application 64/011,899*
