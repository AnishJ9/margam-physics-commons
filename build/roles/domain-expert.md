# Role: Domain Expert

---

## What You Bring

You know what good looks like in your physical domain. You've seen enough cases, failures, and near-misses to know what the physics was doing before anyone else noticed. That knowledge is the most valuable thing in the commons. The model can learn correlation from data. It cannot learn what correlation means without you.

---

## What You Contribute

- Define the ground truth signal — what does "the physics was right" mean in your domain?
- Map the causal structure — what interventions matter, in which direction, with which confounders?
- Identify the failure modes — where does a model trained on correlation get it wrong?
- Describe what practitioners know that datasets don't capture
- Review the trained conditioning layer's outputs for clinical/physical sense

---

## What You Receive From the Team

- **From ML Engineer:** a trained conditioning layer that encodes your causal structure
- **From Product:** a product spec that uses your ground truth signal as the core metric
- **From Sales:** customer feedback on which parts of your framing land

---

## What You Produce

- A completed `contribute/DOMAIN_TEMPLATE.md`
- A causal structure spec that becomes the training specification
- A validation opinion on the conditioning layer outputs — does this match what you'd expect?

---

## How This Connects to the Marketplace

Your expertise is what makes the conditioning layer valid. A deviation score that doesn't reflect the real physics of your domain doesn't pass the eval. A deviation score that does — one that encodes the right causal directions — passes and gets registered. Your contribution is why it works.

---

## What AI Can Do Here

AI can convert your plain-language description into a training specification. You describe the causal structure in the domain template. AI translates it into the JSON spec the training pipeline reads. You don't write code.

---

## To Get Started

Fill out `contribute/DOMAIN_TEMPLATE.md`. Plain language. No code required. That's the whole first step.
