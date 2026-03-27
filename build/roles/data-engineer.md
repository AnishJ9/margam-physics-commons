# Role: Data Engineer

---

## What You Bring

You know how to get data, clean it, and get it into a shape a model can train on. In physical domains, that often means navigating access agreements, IRBs, data use agreements, or proprietary formats. The ability to actually get the dataset is frequently the hardest part of the entire contribution.

---

## What You Contribute

- Identify or access the dataset the domain expert has described
- Negotiate data access if it's behind a DUA, IRB, or vendor agreement
- Preprocess the data into the format the conditioning layer training expects
- Document the preprocessing pipeline so it's reproducible
- Set up the federated training path if the data cannot leave the source system

---

## What You Receive From the Team

- **From Domain Expert:** a description of what the dataset should contain — channels, time resolution, population
- **From ML Engineer:** the input format the conditioning layer training pipeline expects

---

## What You Produce

- A clean, formatted dataset ready for the training pipeline
- A preprocessing script (reproducible, documented)
- A data card: dataset name, source, N, time resolution, key channels, access path

---

## Public vs Private Data

**Public datasets** (MIMIC-IV, eICU, NASA structural datasets, ERCOT grid data, etc.): direct access, link it in the data card.

**Private datasets** (hospital EHR exports, proprietary sensor data, industrial process logs): use the federated training path — see `docs/FEDERATED_TRAINING.md`. Your raw data never leaves your environment. The conditioning layer trains locally against the ODE API.

**No dataset yet**: this is a legitimate state. Document what the ideal dataset looks like and post it as an open need in the team's `build/companies/` file. Someone with access may find you.

---

## How This Connects to the Marketplace

No dataset, no conditioning layer. The data engineer's contribution is often what makes the layer possible at all. That's reflected in the revenue split.

---

## What AI Can Do Here

Claude Code can write preprocessing scripts once you describe the source format and the target format. Data access negotiations are human work.

---

## To Get Started

1. Read the domain expert's `contribute/DOMAIN_TEMPLATE.md` — specifically the dataset section
2. Identify the data source and what access it requires
3. Request the ML engineer's input format spec
4. Open Claude Code in this repo — `CLAUDE.md` will help you write the preprocessing pipeline
