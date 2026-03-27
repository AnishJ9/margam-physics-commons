# Federated Training

If your dataset cannot leave your environment — hospital EHR data, proprietary industrial logs, protected government data — you train the conditioning layer locally using the federated path. Your raw data never leaves your machine. Only API calls go out.

---

## How It Works

```
Your machine                          LINCR API
─────────────────                     ─────────────────
Raw dataset                           Frozen ODE core
    ↓                                      ↑
Conditioning layer    ──── input ──────────┘
    ↑                 ←─── trajectory ─────┘
Loss computation
    ↓
Weight update (local)
```

1. Your conditioning layer preprocesses your local data into the ODE's 25-channel input format
2. Those inputs are sent to the LINCR API — no raw data, only the preprocessed vectors
3. The API runs the frozen ODE and returns the predicted state trajectory
4. Your conditioning layer computes the loss against the actual trajectory (local)
5. Gradients flow back through the conditioning layer only — the ODE weights never update
6. Repeat until convergence

The ODE weights stay on LINCR servers. Your raw data stays on your machine. The only thing crossing the boundary is preprocessed input vectors (25 floats per timestep) and predicted trajectories.

---

## What Leaves Your Machine

**Sent to the API:**
- Input vectors: 25 channels × N timesteps per batch
- These are normalized, channel-mapped values — not raw sensor readings, not patient identifiers

**Never sent:**
- Raw sensor data
- Patient identifiers or demographics
- Labels or outcomes
- Anything in your source dataset that you haven't explicitly mapped into the 25-channel format

---

## Setup

### 1. Get API credentials
Request a contributor API key: `api@lincr.ai`

Include:
- Your name and institution
- The domain you're working in
- Whether your dataset is covered by a DUA, IRB, or other access restriction

### 2. Configure your environment
```bash
export MARGAM_API_KEY=your_key_here
export MARGAM_API_ENDPOINT=https://api.lincr.ai/v1
```

### 3. Install the client library
```bash
pip install margam-client
```

### 4. Write your conditioning layer

Your conditioning layer handles two things:
- **Input mapping:** translate your domain's sensor channels into the 25 standard channels
- **Intervention encoding:** encode your domain's interventions as the ODE's intervention signals

See `contribute/spec_format.json` for the channel mapping specification.

### 5. Train

```python
from margam_client import MargamAPI
from your_domain import ConditioningLayer, load_dataset

api = MargamAPI(api_key=os.environ["MARGAM_API_KEY"])
layer = ConditioningLayer(spec="contribute/your_domain_spec.json")
dataset = load_dataset("path/to/your/local/data")

for batch in dataset:
    # Map domain inputs → 25-channel format (local)
    mapped_inputs = layer.map_inputs(batch)

    # Get ODE predictions (API call — no raw data sent)
    predicted_trajectory = api.predict(mapped_inputs)

    # Compute loss against actual trajectory (local)
    loss = layer.compute_loss(predicted_trajectory, batch.actual_trajectory)

    # Update conditioning layer weights only (local)
    loss.backward()
    optimizer.step()
```

---

## Eval

Eval runs the same way — local data, API forward passes, deviation score computed locally. The eval harness produces a result you can submit with your PR.

```bash
python eval/run_eval.py \
  --layer layers/your_domain/ \
  --dataset path/to/holdout \
  --api-key $MARGAM_API_KEY
```

---

## Data Governance

If your institution requires a Data Use Agreement before any data-derived computations leave the environment, contact `api@lincr.ai` before starting. We can provide:
- Documentation of exactly what is sent to the API (input format, no raw data)
- A signed agreement between LINCR AI and your institution
- An on-premises API option for institutions with strict network egress controls (contact us)

---

## Rate Limits

| Tier | Calls/day | Batch size | Notes |
|------|-----------|------------|-------|
| Contributor (free) | 100,000 | 512 timesteps | During training phase |
| Registered layer | Unlimited | 4,096 timesteps | After layer passes eval |
| Enterprise | Negotiated | Custom | For institutions with volume needs |

Training a conditioning layer typically requires 50,000–200,000 API calls depending on dataset size and convergence. The free contributor tier covers most training runs.
