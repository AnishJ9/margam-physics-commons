"""
Margam Client — Python client for the Margam Physics API

Usage:
    from margam_client import MargamClient

    client = MargamClient()  # reads MARGAM_API_KEY and MARGAM_API_ENDPOINT from env

    # Single prediction
    result = client.predict(inputs)  # inputs: list of 25-channel timesteps

    # Batch prediction (more efficient for training)
    results = client.predict_batch(cases)

    # Get channel specs for normalization
    channels = client.get_channels()

Development:
    Run the mock server first:
        python api/mock_server.py

    Then set:
        export MARGAM_API_ENDPOINT=http://localhost:8765/v1
        # No API key needed for mock

Production:
    export MARGAM_API_KEY=your_key
    export MARGAM_API_ENDPOINT=https://api.lincr.ai/v1
"""

import json
import os
import urllib.request
import urllib.error
from typing import Optional


class MargamClient:

    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ.get("MARGAM_API_KEY", "")
        self.endpoint = (endpoint or os.environ.get("MARGAM_API_ENDPOINT", "https://api.lincr.ai/v1")).rstrip("/")
        self._channels = None

    def _request(self, method: str, path: str, body=None):
        url = f"{self.endpoint}{path}"
        data = json.dumps(body).encode() if body is not None else None
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            raise RuntimeError(f"API error {e.code}: {error_body}") from e

    def health(self):
        """Check API connectivity."""
        return self._request("GET", "/health")

    def get_channels(self):
        """Get channel specs including population mean/std for normalization."""
        if self._channels is None:
            resp = self._request("GET", "/channels")
            self._channels = {ch["name"]: ch for ch in resp["channels"]}
        return self._channels

    def normalize(self, raw_inputs: list, channel_names: list) -> list:
        """
        Normalize raw domain inputs to z-scores using population stats.

        Args:
            raw_inputs: list of T timesteps, each a dict {channel_name: value}
            channel_names: ordered list of the 25 channel names for your domain

        Returns:
            list of T timesteps, each a list of 25 normalized floats
        """
        channels = self.get_channels()
        normalized = []
        for timestep in raw_inputs:
            row = []
            for name in channel_names:
                raw = timestep.get(name, None)
                if raw is None or raw != raw:  # None or NaN
                    row.append(0.0)  # population mean after normalization
                else:
                    ch = channels.get(name, {})
                    mean = ch.get("population_mean", 0)
                    std = ch.get("population_std", 1)
                    row.append((raw - mean) / max(std, 1e-6))
            normalized.append(row)
        return normalized

    def predict(self, inputs: list, horizon_minutes: int = 15, return_trajectory: bool = True) -> dict:
        """
        Single forward pass through the frozen ODE.

        Args:
            inputs: list of T timesteps, each a list of 25 normalized floats
            horizon_minutes: prediction horizon (5, 10, or 15)
            return_trajectory: whether to return full 49-dim ODE state

        Returns:
            {
                trajectory: float[T][49],   # full ODE state (if requested)
                predicted_map: float[H],    # predicted MAP over horizon
                deviation_score: float,     # scalar departure from baseline
                checkpoint_version: str
            }
        """
        return self._request("POST", "/predict", {
            "inputs": inputs,
            "horizon_minutes": horizon_minutes,
            "return_trajectory": return_trajectory,
        })

    def predict_batch(self, cases: list, return_trajectory: bool = True) -> list:
        """
        Batch forward pass. More efficient for training.

        Args:
            cases: list of {case_id, inputs, horizon_minutes}
            return_trajectory: whether to return full ODE state

        Returns:
            list of results, one per case
        """
        resp = self._request("POST", "/predict/batch", {
            "cases": cases,
            "return_trajectory": return_trajectory,
        })
        return resp["results"]
