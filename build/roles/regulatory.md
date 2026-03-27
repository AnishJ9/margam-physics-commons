# Role: Regulatory

---

## What You Bring

You know the approval path in your domain. FDA, FAA, FERC, OSHA, NRC — different domains, different regulators, same fundamental question: what does this product do, what can go wrong, and what evidence is required before it can be used.

---

## What You Contribute

- Classify the product in your domain's regulatory framework
- Identify whether there is an exemption path (and what it requires)
- Define the minimum viable evidence package for deployment
- Review all external-facing claims for regulatory accuracy
- Own the relationship with the relevant regulatory body if a submission is required

---

## What You Receive From the Team

- **From Product:** what the product does and who uses it
- **From Domain Expert:** what the deviation score means clinically/physically
- **From Legal:** corporate structure and liability framing

---

## What You Produce

- A regulatory classification memo: what this is, what exemption applies (or what approval path)
- A list of claims the product can and cannot make
- The evidence package outline: what studies are needed, what format, what threshold

---

## Clinical Domain Specifically

The clinical physics layer is a retrospective QI tool — it analyzes completed cases, does not give real-time clinical recommendations, and is not used to diagnose or treat. This positions it as a Clinical Decision Support tool under FDA's 520(o)(1)(E) exemption.

The key requirements for that exemption: the tool must display its basis, allow the clinician to independently review, and not be the primary basis for the clinical decision. A deviation score report that shows its reasoning and is reviewed by a QI committee satisfies all three.

For other domains, the analogous question is: is this advisory (human makes the final decision) or autonomous (system acts without human review)? Advisory tools generally have a lower regulatory burden.

---

## What AI Can Do Here

Claude Code can research the regulatory framework for a new domain and draft a classification memo. Regulatory judgment — what an agency will actually accept — requires experience in that domain.

---

## To Get Started

1. Read the product spec in `build/companies/your_domain/PRODUCT_SPEC.md`
2. Identify the regulatory framework for your domain
3. Write the classification memo and claims list
4. Flag any claim in the README or role templates that needs adjustment for your domain
