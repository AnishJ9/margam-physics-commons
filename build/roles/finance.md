# Role: Finance

---

## What You Bring

You can model unit economics, structure a company, and figure out whether a deal is worth doing. A conditioning layer that generates marketplace revenue is a business. Someone needs to make sure it's a good one.

---

## What You Contribute

- Model the unit economics: cost to train, cost to run (API calls), revenue per license, margin
- Structure the company: what entity, what ownership split, what vesting schedule
- Manage the revenue attribution agreement in `build/COMPANY_TEMPLATE.md`
- Project when the layer becomes self-sustaining
- Advise on pricing: is the marketplace floor fee appropriate for your domain's buyer?

---

## What You Receive From the Team

- **From Sales:** what the buyer will pay
- **From ML Engineer:** infrastructure costs (API call volume, compute)
- **From Legal:** entity structure and IP assignment

---

## What You Produce

- A unit economics model: cost, revenue, margin, breakeven
- A revenue attribution agreement (documented in `build/COMPANY_TEMPLATE.md`)
- A company structure recommendation

---

## The Revenue Model

Conditioning layers earn marketplace revenue two ways:
1. **Commercial licenses** — annual fee from organizations that use the layer in their product
2. **Usage-based** — per-API-call fee for high-volume users

The marketplace sets the floor based on deviation score delta. Teams negotiate above it for enterprise agreements.

The finance role owns making sure the team's split is documented before the first license is issued. Splits locked at registration cannot be changed without a new layer version.

---

## What AI Can Do Here

Claude Code can build unit economics models and draft revenue agreements once you give it the inputs. Judgment calls — what's fair, what's sustainable, what a buyer in this domain will actually pay — are yours.

---

## To Get Started

1. Read `docs/MARKETPLACE.md` for the revenue structure
2. Get the cost estimate from the ML engineer (training + inference)
3. Get the price signal from sales (what will a buyer pay?)
4. Model the unit economics and document the team split in `build/COMPANY_TEMPLATE.md`
