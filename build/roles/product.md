# Role: Product

---

## What You Bring

You understand how the deviation score fits into a real workflow. You know what a buyer actually uses day-to-day, where a new signal would change a decision, and what "good enough" looks like for a first version. The physics can predict a trajectory. You figure out what someone does with that prediction.

---

## What You Contribute

- Define the customer workflow — where in the existing process does the deviation score appear?
- Translate the ground truth signal into a product decision: what action does a high deviation score trigger?
- Write the product spec: inputs, outputs, user interface (even if it's just a number on a screen)
- Define what a pilot looks like — what does the customer measure to decide if it worked?
- Own the feedback loop from pilot customers back to the domain expert and ML engineer

---

## What You Receive From the Team

- **From Domain Expert:** what the deviation score means physically
- **From Sales:** what the customer said they want (often different from what they need)
- **From Regulatory:** what the product is allowed to do

---

## What You Produce

- A product spec in `build/companies/your_domain/PRODUCT_SPEC.md`
- A pilot design: what the customer measures, over what time period, with what success criteria
- A prioritized list of what to build first

---

## The Core Product Question

Every physics layer in this marketplace answers the same question: "how far did the real trajectory depart from what physics predicted?" Your job is to make that answer legible to a person who is not a physicist and who has a decision to make in the next five minutes.

---

## What AI Can Do Here

Claude Code can draft product specs and pilot designs once you describe the customer workflow. The product judgment — what matters to this specific customer, what they'll actually use — is yours.

---

## To Get Started

1. Read the domain expert's `contribute/DOMAIN_TEMPLATE.md`
2. Talk to one customer in the domain — even a 30-minute call — before writing anything
3. Write the product spec in `build/companies/your_domain/PRODUCT_SPEC.md`
4. Open Claude Code in this repo — `CLAUDE.md` will help you structure the spec
