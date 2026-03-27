# Role: ML Engineer

---

## What You Bring

You can train a neural network, run an eval, and interpret a metric. You don't need to understand the ODE architecture — the frozen core runs as an API. Your job is to build the conditioning layer that maps a domain's inputs and interventions into the ODE's coordinate system, train it against the API, and prove the deviation score improved.

---

## What You Contribute

- Convert the domain expert's causal structure spec into a conditioning layer architecture
- Write the training loop that sends inputs through the API and trains the conditioning layer on ODE state outputs
- Run the eval harness and document the deviation score delta
- Prepare the layer for registration (checkpoint, eval results, spec)

---

## What You Receive From the Team

- **From Domain Expert:** the causal structure spec — which inputs, which interventions, which directions
- **From Data Engineer:** a clean dataset in the format the conditioning layer expects
- **From Product:** the target use case — which decisions the deviation score needs to inform

---

## What You Produce

- A trained conditioning layer checkpoint
- Eval results against the holdout dataset
- The PR that registers the layer in the marketplace

---

## The Technical Interface

The frozen ODE runs as an API endpoint. Your conditioning layer:
1. Takes domain-specific inputs (your sensor channels, your intervention signals)
2. Maps them into the ODE's 25-channel input format
3. Calls the ODE API with the mapped inputs
4. Receives back the predicted state trajectory (49-dimensional ODE state)
5. Computes the deviation score against the actual trajectory

Training objective: minimize prediction error on the domain's ground truth signal while preserving the causal directions documented by the domain expert.

You are not modifying the frozen ODE. You are teaching it your domain via the conditioning layer.

---

## How This Connects to the Marketplace

A passing eval (AUROC delta ≥ 0.005 on holdout) registers the layer. The ML engineer's share of marketplace revenue is set in the team's `build/COMPANY_TEMPLATE.md`.

---

## What AI Can Do Here

Claude Code can write most of the conditioning layer boilerplate once the domain spec is clear. The ML engineer's judgment matters for: architecture choices (how many layers, what activation, what regularization), training stability, and interpreting eval results. The code is often straightforward — the judgment is not.

---

## To Get Started

1. Get the domain spec from the domain expert (`contribute/your_domain_spec.json`)
2. Get the dataset from the data engineer
3. Request API credentials: `api@lincr.ai`
4. Open Claude Code in this repo — `CLAUDE.md` will walk you through the training setup
