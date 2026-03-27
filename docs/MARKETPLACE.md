# Marketplace

The marketplace connects contributors to licensees and handles payment automatically. Physics adjudicates value — the deviation score improvement determines what a layer is worth, not negotiation.

---

## Revenue Structure

Two levels. Both earn from the same license event.

```
Physics Engine contributor  →  foundation royalty (% of every conditioning layer license)
Conditioning Layer team     →  layer revenue (remaining % split among team roles)
```

When a conditioning layer license is sold:
1. Foundation royalty flows to the physics engine contributor first
2. Remainder flows to the conditioning layer team per their documented split

**MargamSim CF2 (clinical):** contributed by LINCR AI. Foundation royalty applies to all clinical conditioning layers licensed through the marketplace.

**Other domains:** when a new physics engine is accepted, its contributor's royalty structure is locked at registration. Contributors who build conditioning layers on that engine see the foundation royalty rate before they commit.

---

## How It Works

### Registration

When a conditioning layer passes the eval threshold, it gets registered with:
- The contributor team's addresses (one per role, weighted by the team's revenue agreement)
- The domain it covers
- The eval result — baseline deviation score, layer deviation score, delta
- The dataset it was validated on
- The version of the frozen ODE core it was trained against

Registration is permanent and auditable. The eval result is part of the record.

### Licensing

Licensees pay to use a conditioning layer in their product or research. Two license types:

**Research license:** Free for academic and non-commercial use. Requires attribution. Contributor gets credited in citations.

**Commercial license:** Annual fee, set by the marketplace based on the deviation score delta. Larger improvement = higher fee floor. Negotiated ceiling for enterprise agreements.

The deviation score delta is the price signal. A layer that improves predictions by 0.010 AUROC is priced differently than one that improves by 0.100. The physics sets the floor. The market negotiates above it.

### Payment

Commercial license fees flow to contributor addresses automatically when a license is issued. Split according to the revenue agreement documented in `build/COMPANY_TEMPLATE.md` at the time of registration.

The split is locked at registration. It doesn't change after a license is sold.

---

## Phase 1 (Current): Manual

While the automated marketplace infrastructure is being built, registration and payment work as follows:

1. Submit a PR with your conditioning layer and eval results
2. The PR review confirms the eval harness ran correctly and the delta is real
3. On merge, your layer is listed in `layers/registry.json` with your team's payment addresses
4. Licenses are issued manually via email: `marketplace@lincr.ai`
5. Payment via Stripe invoice, split to team members manually per your agreement

This is slow but auditable. Every transaction is documented.

---

## Phase 2 (Coming): Automated

- API endpoint for layer registration
- Automated license issuance on payment
- Payment distribution via Stripe Connect to contributor accounts
- Real-time dashboard showing layer usage and revenue

---

## IP Attribution

Contributors who bring existing IP — a pre-trained model, a proprietary dataset, a patent — earn a permanent revenue share separate from the role-based team split.

**Dataset licensing:** A proprietary dataset that enables a conditioning layer earns a share of marketplace revenue from any layer registered against it. The share is set at the time the dataset is registered and does not change.

**Model IP:** A pre-trained model used to initialize or guide a conditioning layer earns a share determined by ablation:

```
auroc_scratch     = conditioning layer trained from scratch
auroc_with_ip     = conditioning layer initialized from contributed model
ip_delta          = auroc_with_ip - auroc_scratch
total_delta       = auroc_with_ip - domain_baseline

ip_share = clip(ip_delta / total_delta, 0, 0.50)
```

- If `ip_delta > 0`: IP contributor earns up to 50% of the layer's marketplace revenue, proportional to how much of the improvement came from their model
- If `ip_delta ≤ 0`: IP share is zero. The contributor keeps their model. Nothing is owed.
- If `ip_delta < 0.005` (below eval noise floor): default 5% fixed share, negotiable up to 15%

The ablation runs as part of the registration eval. The result is locked into the registry. It does not change after registration.

**Patent licensing:** Domain IP licensed to the marketplace earns royalties per conditioning layer that uses it. Terms set at the time of the IP contribution agreement.

Bring your IP contributions via `contribute/IP_TEMPLATE.md`. Contact `ip@lincr.ai` to discuss terms before committing.

---

## Revenue Attribution

Before you register, your team needs a documented revenue split in `build/COMPANY_TEMPLATE.md`. Every role that contributed gets a share. The split is your team's decision, not the marketplace's.

What the marketplace enforces:
- The total must sum to 100%
- Shares are locked at registration
- Changes to the split require a new registration (new layer version)

What the marketplace does not enforce:
- Which roles deserve what share — that's your team's decision
- Whether a contributor actually did their job — the eval harness handles that for the technical roles; the team handles it for the others

---

## Eval Threshold

A conditioning layer must improve the deviation score over the domain baseline to be registered. The current threshold:

**AUROC@15 delta ≥ 0.005** on the holdout dataset.

Layers that don't pass the threshold are not registered. The physics decides. Submit the eval results with your PR and the harness re-runs them to verify.

---

## What Happens When the ODE Core Updates

When a new frozen checkpoint is released (CF3, CF4, etc.), existing registered layers remain valid against the version of the core they were trained on. Layers are versioned against the core checkpoint.

Contributors who want to upgrade their layer to the new core need to retrain and re-eval. A passing result against the new core creates a new registration alongside the old one.

---

## Contact

`marketplace@lincr.ai`
