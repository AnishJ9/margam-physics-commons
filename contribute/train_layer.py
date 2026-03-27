"""
Conditioning Layer Training Pipeline

Trains a domain conditioning layer on top of the frozen Margam ODE core.
The ODE core runs server-side — you train the input mapping layer locally.

Usage:
    # Start the mock server first (for development):
    #   python api/mock_server.py

    python contribute/train_layer.py \
        --domain your_domain \
        --spec contribute/your_domain_spec.json \
        --dataset path/to/data.json \
        --out layers/your_domain/ \
        --epochs 20

    # Against real API:
    export MARGAM_API_KEY=your_key
    export MARGAM_API_ENDPOINT=https://api.lincr.ai/v1
    python contribute/train_layer.py --domain your_domain ...

Dataset format (JSON):
    [
        {
            "case_id": "string",
            "timesteps": [
                {"channel_name": value, ...},  // one dict per minute
                ...
            ],
            "actual_map": [float, ...],        // actual MAP values
            "label": 0 or 1                   // 1 = ground truth event occurred
        },
        ...
    ]
"""

import argparse
import json
import os
import random
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from margam_client import MargamClient


# ── Conditioning Layer ────────────────────────────────────────────────────────

class ConditioningLayer:
    """
    Minimal conditioning layer: maps domain inputs to 25 ODE channels.

    Architecture:
        domain_channels → linear → ReLU → linear → 25 channels

    No ML framework required — pure Python with manual gradients.
    Replace with PyTorch/JAX if you need more capacity.
    """

    def __init__(self, n_domain_channels: int, hidden_dim: int = 64):
        self.n_in = n_domain_channels
        self.hidden = hidden_dim
        self.n_out = 25

        # Xavier initialization
        self.W1 = self._xavier(n_domain_channels, hidden_dim)
        self.b1 = [0.0] * hidden_dim
        self.W2 = self._xavier(hidden_dim, 25)
        self.b2 = [0.0] * 25

        # Gradient accumulators
        self.dW1 = [[0.0] * hidden_dim for _ in range(n_domain_channels)]
        self.db1 = [0.0] * hidden_dim
        self.dW2 = [[0.0] * 25 for _ in range(hidden_dim)]
        self.db2 = [0.0] * 25

    def _xavier(self, fan_in, fan_out):
        scale = math.sqrt(2.0 / (fan_in + fan_out))
        return [[random.gauss(0, scale) for _ in range(fan_out)] for _ in range(fan_in)]

    def forward(self, x):
        """x: list of n_domain_channels floats → list of 25 floats"""
        # Layer 1
        h = [sum(x[i] * self.W1[i][j] for i in range(self.n_in)) + self.b1[j]
             for j in range(self.hidden)]
        # ReLU
        h = [max(0.0, v) for v in h]
        # Layer 2
        out = [sum(h[i] * self.W2[i][j] for i in range(self.hidden)) + self.b2[j]
               for j in range(self.n_out)]
        return out, h  # return h for backprop

    def zero_grad(self):
        self.dW1 = [[0.0] * self.hidden for _ in range(self.n_in)]
        self.db1 = [0.0] * self.hidden
        self.dW2 = [[0.0] * self.n_out for _ in range(self.hidden)]
        self.db2 = [0.0] * self.n_out

    def step(self, lr: float):
        """SGD update"""
        for i in range(self.n_in):
            for j in range(self.hidden):
                self.W1[i][j] -= lr * self.dW1[i][j]
        for j in range(self.hidden):
            self.b1[j] -= lr * self.db1[j]
        for i in range(self.hidden):
            for j in range(self.n_out):
                self.W2[i][j] -= lr * self.dW2[i][j]
        for j in range(self.n_out):
            self.b2[j] -= lr * self.db2[j]

    def save(self, path: str):
        state = {
            "n_in": self.n_in, "hidden": self.hidden, "n_out": self.n_out,
            "W1": self.W1, "b1": self.b1, "W2": self.W2, "b2": self.b2
        }
        with open(path, "w") as f:
            json.dump(state, f)

    @classmethod
    def load(cls, path: str):
        with open(path) as f:
            state = json.load(f)
        layer = cls(state["n_in"], state["hidden"])
        layer.W1, layer.b1, layer.W2, layer.b2 = state["W1"], state["b1"], state["W2"], state["b2"]
        return layer


# ── Training Loop ─────────────────────────────────────────────────────────────

def mse_loss(predicted: list, actual: list) -> float:
    n = min(len(predicted), len(actual))
    return sum((predicted[i] - actual[i]) ** 2 for i in range(n)) / max(n, 1)


def load_dataset(path: str):
    with open(path) as f:
        return json.load(f)


def extract_domain_channels(timestep: dict, channel_names: list) -> list:
    return [float(timestep.get(name, 0.0) or 0.0) for name in channel_names]


def train(args):
    # Load spec
    with open(args.spec) as f:
        spec = json.load(f)

    domain_name = spec.get("domain", {}).get("name", args.domain)
    channel_names = [ch["name"] for ch in spec.get("input_channels", [])]
    n_channels = len(channel_names)
    horizon = spec.get("domain", {}).get("prediction_horizon_minutes", 15)
    gt_threshold = spec.get("domain", {}).get("ground_truth_threshold", 65)

    print(f"Domain: {domain_name}")
    print(f"Input channels: {n_channels} ({', '.join(channel_names[:4])}...)")
    print(f"Prediction horizon: {horizon} min")
    print(f"Ground truth threshold: {gt_threshold}")

    # Load dataset
    dataset = load_dataset(args.dataset)
    random.shuffle(dataset)
    split = int(len(dataset) * 0.8)
    train_cases = dataset[:split]
    val_cases = dataset[split:]
    print(f"Dataset: {len(train_cases)} train, {len(val_cases)} val")

    # Init
    client = MargamClient()
    layer = ConditioningLayer(n_channels, hidden_dim=args.hidden_dim)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nUsing API: {client.endpoint}")
    health = client.health()
    print(f"API status: {health.get('status')} | checkpoint: {health.get('checkpoint_version')}")
    if health.get("mock"):
        print("NOTE: Running against mock server. Metrics are not real physics.")

    best_val_loss = float("inf")

    for epoch in range(args.epochs):
        random.shuffle(train_cases)
        train_loss = 0.0
        n_batches = 0

        for i in range(0, len(train_cases), args.batch_size):
            batch = train_cases[i:i + args.batch_size]
            layer.zero_grad()
            batch_loss = 0.0

            # Build API batch
            api_cases = []
            domain_inputs_per_case = []

            for case in batch:
                timesteps = case.get("timesteps", [])
                domain_inputs = [extract_domain_channels(t, channel_names) for t in timesteps]
                mapped_inputs = [layer.forward(x)[0] for x in domain_inputs]
                domain_inputs_per_case.append(domain_inputs)
                api_cases.append({
                    "case_id": case.get("case_id", str(i)),
                    "inputs": mapped_inputs,
                    "horizon_minutes": horizon
                })

            # Single API call for whole batch
            results = client.predict_batch(api_cases, return_trajectory=False)

            # Compute loss and accumulate gradients
            for case, result, domain_inputs in zip(batch, results, domain_inputs_per_case):
                actual_map = case.get("actual_map", [])
                predicted_map = result.get("predicted_map", [])
                loss = mse_loss(predicted_map, actual_map)
                batch_loss += loss

                # Gradient of MSE w.r.t. predicted_map
                n = min(len(predicted_map), len(actual_map))
                d_pred = [(2 / n) * (predicted_map[k] - actual_map[k]) if k < n else 0.0
                          for k in range(len(predicted_map))]

                # Backprop through conditioning layer (simplified: use first timestep gradient)
                if domain_inputs:
                    x = domain_inputs[0]
                    out, h = layer.forward(x)
                    # dL/dout — approximate via MAP channel (channel 0 of ODE output)
                    d_out = [d_pred[0] if j == 0 else 0.0 for j in range(25)]
                    # Layer 2 gradients
                    for ii in range(layer.hidden):
                        for jj in range(25):
                            layer.dW2[ii][jj] += h[ii] * d_out[jj]
                    for jj in range(25):
                        layer.db2[jj] += d_out[jj]

            layer.step(args.lr)
            train_loss += batch_loss / len(batch)
            n_batches += 1

        train_loss /= max(n_batches, 1)

        # Validation
        val_loss = 0.0
        val_cases_api = []
        for case in val_cases:
            timesteps = case.get("timesteps", [])
            domain_inputs = [extract_domain_channels(t, channel_names) for t in timesteps]
            mapped_inputs = [layer.forward(x)[0] for x in domain_inputs]
            val_cases_api.append({
                "case_id": case.get("case_id", "val"),
                "inputs": mapped_inputs,
                "horizon_minutes": horizon
            })

        val_results = client.predict_batch(val_cases_api, return_trajectory=False)
        for case, result in zip(val_cases, val_results):
            val_loss += mse_loss(result.get("predicted_map", []), case.get("actual_map", []))
        val_loss /= max(len(val_cases), 1)

        print(f"Epoch {epoch+1}/{args.epochs} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            layer.save(str(out_dir / "best.json"))
            print(f"  ✓ Saved best checkpoint (val_loss={val_loss:.4f})")

    layer.save(str(out_dir / "final.json"))
    print(f"\nTraining complete. Best val_loss: {best_val_loss:.4f}")
    print(f"Checkpoints saved to: {out_dir}/")
    print(f"\nNext step: run eval")
    print(f"  python eval/run_eval.py --layer {out_dir}/ --dataset {args.dataset} --spec {args.spec}")


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a Margam conditioning layer")
    parser.add_argument("--domain",     required=True, help="Domain name")
    parser.add_argument("--spec",       required=True, help="Path to domain spec JSON")
    parser.add_argument("--dataset",    required=True, help="Path to training dataset JSON")
    parser.add_argument("--out",        required=True, help="Output directory for checkpoints")
    parser.add_argument("--epochs",     type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=32, dest="batch_size")
    parser.add_argument("--lr",         type=float, default=1e-3)
    parser.add_argument("--hidden-dim", type=int, default=64, dest="hidden_dim")
    args = parser.parse_args()
    train(args)
