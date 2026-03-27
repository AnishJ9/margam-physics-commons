# Margam API Interface

The frozen ODE core runs server-side. Contributors call this API during training and eval. Your raw data never leaves your machine — only preprocessed 25-channel input vectors go out.

Base URL: `https://api.lincr.ai/v1`
Local mock: `http://localhost:8765/v1` (run `python api/mock_server.py`)

---

## Authentication

```
Authorization: Bearer YOUR_API_KEY
```

Request a contributor key: `api@lincr.ai`

---

## Endpoints

### `POST /v1/predict`

Single forward pass. Takes a sequence of 25-channel inputs, returns the ODE's predicted state trajectory.

**Request:**
```json
{
  "inputs": [
    [float, ...],
    ...
  ],
  "horizon_minutes": 15,
  "return_trajectory": true
}
```

| Field | Type | Description |
|-------|------|-------------|
| `inputs` | `float[T][25]` | T timesteps × 25 channels. Channels must match `contribute/spec_format.json` channel map. Values normalized to z-score against population mean/std. |
| `horizon_minutes` | `int` | How far ahead to predict. Default: 15. Supported: 5, 10, 15. |
| `return_trajectory` | `bool` | Return full ODE state trajectory (49-dim × T). Default: true. |

**Response:**
```json
{
  "trajectory": [[float, ...], ...],
  "predicted_map": [float, ...],
  "deviation_score": float,
  "checkpoint_version": "cf2_epoch3",
  "timesteps": 15
}
```

| Field | Type | Description |
|-------|------|-------------|
| `trajectory` | `float[T][49]` | Full ODE state: cardio (27) + resp (8) + PK (14) per timestep |
| `predicted_map` | `float[H]` | Predicted MAP over the horizon window (mmHg) |
| `deviation_score` | `float` | Scalar: how far this trajectory departed from the predicted baseline. Higher = larger departure. |
| `checkpoint_version` | `str` | Which frozen checkpoint produced this result |

---

### `POST /v1/predict/batch`

Batch forward pass. More efficient for training — sends a full dataset, gets all trajectories back in one call.

**Request:**
```json
{
  "cases": [
    {
      "case_id": "string",
      "inputs": [[float, ...], ...],
      "horizon_minutes": 15
    }
  ],
  "return_trajectory": true
}
```

Max batch size: 512 cases per call.

**Response:**
```json
{
  "results": [
    {
      "case_id": "string",
      "trajectory": [[float, ...], ...],
      "predicted_map": [float, ...],
      "deviation_score": float
    }
  ],
  "checkpoint_version": "cf2_epoch3"
}
```

---

### `GET /v1/health`

```json
{ "status": "ok", "checkpoint_version": "cf2_epoch3" }
```

---

### `GET /v1/channels`

Returns the full 25-channel specification with normalization stats.

```json
{
  "channels": [
    {
      "index": 0,
      "name": "map_mmhg",
      "group": "cardiovascular",
      "population_mean": 85.2,
      "population_std": 18.4,
      "units": "mmHg"
    }
  ]
}
```

Use this to normalize your domain's inputs before sending.

---

## Input Normalization

All inputs must be z-score normalized using the population stats from `/v1/channels` before sending. Missing channels should be filled with 0.0 (population mean after normalization).

```python
normalized = (raw_value - channel["population_mean"]) / channel["population_std"]
```

---

## Rate Limits

| Tier | Calls/day | Batch size |
|------|-----------|------------|
| Contributor (free) | 100,000 | 512 cases |
| Registered layer | Unlimited | 4,096 cases |

---

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad request — check input shape and normalization |
| 401 | Invalid or missing API key |
| 422 | Input contains NaN or out-of-range values |
| 429 | Rate limit exceeded |
| 503 | Service temporarily unavailable |
