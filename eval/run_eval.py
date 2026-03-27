"""
Conditioning Layer Evaluation Harness

Computes the deviation score improvement of a trained conditioning layer
against the domain baseline. This is the number that determines whether
your layer gets registered in the marketplace.

Usage:
    python eval/run_eval.py \
        --layer layers/your_domain/ \
        --dataset path/to/holdout.json \
        --spec contribute/your_domain_spec.json \
        --baseline 0.873

    # With baseline from file:
    python eval/run_eval.py \
        --layer layers/your_domain/ \
        --dataset path/to/holdout.json \
        --spec contribute/your_domain_spec.json \
        --baseline-file eval/baselines/your_domain.json

Output:
    eval/results/your_domain_TIMESTAMP.json
    Printed summary with pass/fail verdict.

Pass threshold: AUROC@horizon delta >= 0.005 vs baseline
"""

import argparse
import json
import os
import sys
import math
import random
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from margam_client import MargamClient
from contribute.train_layer import ConditioningLayer, extract_domain_channels

PASS_THRESHOLD = 0.005  # minimum AUROC delta to register


# ── Metrics ───────────────────────────────────────────────────────────────────

def auroc(scores: list, labels: list) -> float:
    """Compute AUROC from parallel lists of scores and binary labels."""
    pairs = list(zip(scores, labels))
    pairs.sort(key=lambda x: x[0], reverse=True)

    n_pos = sum(labels)
    n_neg = len(labels) - n_pos
    if n_pos == 0 or n_neg == 0:
        return 0.5

    tp = 0
    fp = 0
    auc = 0.0
    prev_fp = 0

    for score, label in pairs:
        if label == 1:
            tp += 1
        else:
            fp += 1
            auc += tp  # area under curve: count TPs at each FP step

    return auc / (n_pos * n_neg)


def compute_baseline_scores(cases: list, gt_threshold: float, horizon: int) -> tuple:
    """
    Baseline scorer: use the last observed value as the prediction.
    Returns (scores, labels).
    """
    scores = []
    labels = []
    for case in cases:
        timesteps = case.get("timesteps", [])
        actual_map = case.get("actual_map", [])
        label = case.get("label", 0)

        # Baseline: last observed MAP value (lower = higher risk)
        last_map = 85.0  # population mean fallback
        if timesteps:
            last_map = float(timesteps[-1].get("map_mmhg", 85.0) or 85.0)

        # Score = negative MAP (higher score = higher risk)
        scores.append(-last_map)
        labels.append(int(label))

    return scores, labels


# ── Eval ──────────────────────────────────────────────────────────────────────

def run_eval(args):
    # Load spec
    with open(args.spec) as f:
        spec = json.load(f)

    domain_name = spec.get("domain", {}).get("name", "unknown")
    channel_names = [ch["name"] for ch in spec.get("input_channels", [])]
    horizon = spec.get("domain", {}).get("prediction_horizon_minutes", 15)
    gt_threshold = spec.get("domain", {}).get("ground_truth_threshold", 65)

    # Load holdout dataset
    with open(args.dataset) as f:
        cases = json.load(f)
    print(f"Holdout dataset: {len(cases)} cases")

    # Load baseline AUROC
    baseline_auroc = None
    if args.baseline is not None:
        baseline_auroc = float(args.baseline)
    elif args.baseline_file:
        with open(args.baseline_file) as f:
            baseline_data = json.load(f)
        baseline_auroc = baseline_data.get("auroc_at_horizon", baseline_data.get("auroc"))

    # Load conditioning layer
    layer_path = Path(args.layer) / "best.json"
    if not layer_path.exists():
        layer_path = Path(args.layer) / "final.json"
    layer = ConditioningLayer.load(str(layer_path))
    print(f"Layer: {layer_path}")

    # Connect to API
    client = MargamClient()
    health = client.health()
    print(f"API: {client.endpoint} | checkpoint: {health.get('checkpoint_version')}")
    if health.get("mock"):
        print("NOTE: Running against mock server. AUROC will not be real physics.")

    # Run layer predictions
    print(f"\nRunning predictions on {len(cases)} cases...")
    layer_scores = []
    labels = []

    batch_size = 64
    for i in range(0, len(cases), batch_size):
        batch = cases[i:i + batch_size]
        api_cases = []
        for case in batch:
            timesteps = case.get("timesteps", [])
            domain_inputs = [extract_domain_channels(t, channel_names) for t in timesteps]
            mapped_inputs = [layer.forward(x)[0] for x in domain_inputs]
            api_cases.append({
                "case_id": case.get("case_id", str(i)),
                "inputs": mapped_inputs,
                "horizon_minutes": horizon
            })

        results = client.predict_batch(api_cases, return_trajectory=False)
        for case, result in zip(batch, results):
            layer_scores.append(result.get("deviation_score", 0.0))
            labels.append(int(case.get("label", 0)))

        if (i // batch_size + 1) % 10 == 0:
            print(f"  {i + len(batch)}/{len(cases)}")

    # Compute metrics
    layer_auc = auroc(layer_scores, labels)

    # Compute baseline if not provided
    if baseline_auroc is None:
        baseline_scores, _ = compute_baseline_scores(cases, gt_threshold, horizon)
        baseline_auroc = auroc(baseline_scores, labels)
        print(f"Baseline AUROC computed from last-value predictor: {baseline_auroc:.4f}")

    delta = layer_auc - baseline_auroc
    passed = delta >= PASS_THRESHOLD

    # Results
    n_pos = sum(labels)
    n_neg = len(labels) - n_pos
    prevalence = n_pos / max(len(labels), 1)

    result = {
        "domain": domain_name,
        "checkpoint_version": health.get("checkpoint_version"),
        "mock": health.get("mock", False),
        "n_cases": len(cases),
        "n_positive": n_pos,
        "n_negative": n_neg,
        "prevalence": round(prevalence, 4),
        "horizon_minutes": horizon,
        "layer_auroc": round(layer_auc, 4),
        "baseline_auroc": round(baseline_auroc, 4),
        "delta": round(delta, 4),
        "pass_threshold": PASS_THRESHOLD,
        "passed": passed,
        "timestamp": datetime.utcnow().isoformat(),
        "layer_path": str(layer_path),
        "dataset_path": args.dataset,
    }

    # Save results
    results_dir = Path("eval/results")
    results_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    results_path = results_dir / f"{domain_name}_{timestamp}.json"
    with open(results_path, "w") as f:
        json.dump(result, f, indent=2)

    # Print summary
    print(f"\n{'='*50}")
    print(f"EVAL RESULTS — {domain_name}")
    print(f"{'='*50}")
    print(f"Cases:          {len(cases)} ({n_pos} positive, {n_neg} negative)")
    print(f"Prevalence:     {prevalence:.1%}")
    print(f"Horizon:        {horizon} min")
    print(f"Baseline AUROC: {baseline_auroc:.4f}")
    print(f"Layer AUROC:    {layer_auc:.4f}")
    print(f"Delta:          {delta:+.4f}")
    print(f"Threshold:      {PASS_THRESHOLD:+.4f}")
    print(f"{'='*50}")
    if passed:
        print(f"✓ PASSED — layer is eligible for marketplace registration")
    else:
        print(f"✗ FAILED — delta {delta:+.4f} below threshold {PASS_THRESHOLD:+.4f}")
        print(f"  Options: more training data, more epochs, better causal structure")
    print(f"{'='*50}")
    print(f"Results saved: {results_path}")

    if passed:
        print(f"\nNext step: submit a PR with your layer and this results file.")
        print(f"  Layer:   {args.layer}")
        print(f"  Results: {results_path}")
        print(f"  Spec:    {args.spec}")

    return result


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a Margam conditioning layer")
    parser.add_argument("--layer",         required=True, help="Path to layer checkpoint directory")
    parser.add_argument("--dataset",       required=True, help="Path to holdout dataset JSON")
    parser.add_argument("--spec",          required=True, help="Path to domain spec JSON")
    parser.add_argument("--baseline",      type=float,    help="Baseline AUROC (scalar)")
    parser.add_argument("--baseline-file", dest="baseline_file", help="Path to baseline JSON file")
    args = parser.parse_args()

    if args.baseline is None and args.baseline_file is None:
        print("NOTE: No baseline provided. Computing from last-value predictor.")

    run_eval(args)
