"""
Margam API Mock Server

Returns random trajectories with the correct shape and structure.
Use this to develop and test your conditioning layer code before
the live API is available.

Run:
    python api/mock_server.py

Then set:
    MARGAM_API_ENDPOINT=http://localhost:8765/v1

Your conditioning layer code will run against this mock.
Shapes, channels, and response structure are identical to the real API.
Deviation scores and predictions are random — not real physics.
"""

import json
import random
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

# 25 input channels — matches the real API
CHANNELS = [
    {"index": 0,  "name": "map_mmhg",              "group": "cardiovascular", "population_mean": 85.2,  "population_std": 18.4,  "units": "mmHg"},
    {"index": 1,  "name": "sbp_mmhg",              "group": "cardiovascular", "population_mean": 120.5, "population_std": 22.1,  "units": "mmHg"},
    {"index": 2,  "name": "dbp_mmhg",              "group": "cardiovascular", "population_mean": 68.3,  "population_std": 14.2,  "units": "mmHg"},
    {"index": 3,  "name": "hr_bpm",                "group": "cardiovascular", "population_mean": 72.4,  "population_std": 16.8,  "units": "bpm"},
    {"index": 4,  "name": "cvp_mmhg",              "group": "cardiovascular", "population_mean": 8.2,   "population_std": 4.1,   "units": "mmHg"},
    {"index": 5,  "name": "co_l_min",              "group": "cardiovascular", "population_mean": 5.1,   "population_std": 1.4,   "units": "L/min"},
    {"index": 6,  "name": "svr_dyn_s_cm5",         "group": "cardiovascular", "population_mean": 1050,  "population_std": 280,   "units": "dyn·s/cm5"},
    {"index": 7,  "name": "spo2_pct",              "group": "respiratory",    "population_mean": 98.1,  "population_std": 1.8,   "units": "%"},
    {"index": 8,  "name": "etco2_mmhg",            "group": "respiratory",    "population_mean": 38.2,  "population_std": 4.6,   "units": "mmHg"},
    {"index": 9,  "name": "rr_breaths_min",        "group": "respiratory",    "population_mean": 14.2,  "population_std": 3.8,   "units": "breaths/min"},
    {"index": 10, "name": "fio2_pct",              "group": "respiratory",    "population_mean": 45.0,  "population_std": 18.2,  "units": "%"},
    {"index": 11, "name": "pip_cmh2o",             "group": "respiratory",    "population_mean": 18.4,  "population_std": 5.2,   "units": "cmH2O"},
    {"index": 12, "name": "peep_cmh2o",            "group": "respiratory",    "population_mean": 5.0,   "population_std": 2.1,   "units": "cmH2O"},
    {"index": 13, "name": "tv_ml",                 "group": "respiratory",    "population_mean": 480,   "population_std": 95,    "units": "mL"},
    {"index": 14, "name": "temp_c",                "group": "metabolic",      "population_mean": 36.8,  "population_std": 0.8,   "units": "°C"},
    {"index": 15, "name": "glucose_mg_dl",         "group": "metabolic",      "population_mean": 112,   "population_std": 32,    "units": "mg/dL"},
    {"index": 16, "name": "lactate_mmol_l",        "group": "metabolic",      "population_mean": 1.4,   "population_std": 0.9,   "units": "mmol/L"},
    {"index": 17, "name": "hgb_g_dl",              "group": "metabolic",      "population_mean": 11.2,  "population_std": 2.1,   "units": "g/dL"},
    {"index": 18, "name": "ph",                    "group": "metabolic",      "population_mean": 7.40,  "population_std": 0.05,  "units": ""},
    {"index": 19, "name": "hco3_meq_l",            "group": "metabolic",      "population_mean": 24.2,  "population_std": 3.8,   "units": "mEq/L"},
    {"index": 20, "name": "vasopressor_mcg_kg_min","group": "pharmacokinetic","population_mean": 0.05,  "population_std": 0.12,  "units": "mcg/kg/min"},
    {"index": 21, "name": "propofol_mcg_ml",       "group": "pharmacokinetic","population_mean": 1.8,   "population_std": 1.2,   "units": "mcg/mL"},
    {"index": 22, "name": "fentanyl_ng_ml",        "group": "pharmacokinetic","population_mean": 0.8,   "population_std": 0.6,   "units": "ng/mL"},
    {"index": 23, "name": "vecuronium_mcg_ml",     "group": "pharmacokinetic","population_mean": 0.2,   "population_std": 0.3,   "units": "mcg/mL"},
    {"index": 24, "name": "fluid_rate_ml_hr",      "group": "pharmacokinetic","population_mean": 120,   "population_std": 85,    "units": "mL/hr"},
]

ODE_STATE_DIM = 49  # cardio:27 + resp:8 + PK:14
CHECKPOINT_VERSION = "mock_v1"


def make_trajectory(n_timesteps, horizon_minutes):
    """Random trajectory with correct shape. Not real physics."""
    trajectory = [
        [random.gauss(0, 1) for _ in range(ODE_STATE_DIM)]
        for _ in range(n_timesteps)
    ]
    predicted_map = [
        random.gauss(85, 15) for _ in range(horizon_minutes)
    ]
    deviation_score = abs(random.gauss(0.1, 0.05))
    return trajectory, predicted_map, deviation_score


class MockHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"[mock] {self.address_string()} {format % args}")

    def send_json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length))

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/v1/health":
            self.send_json(200, {
                "status": "ok",
                "checkpoint_version": CHECKPOINT_VERSION,
                "mock": True
            })

        elif path == "/v1/channels":
            self.send_json(200, {"channels": CHANNELS})

        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        body = self.read_json()

        if path == "/v1/predict":
            inputs = body.get("inputs", [])
            horizon = body.get("horizon_minutes", 15)
            return_traj = body.get("return_trajectory", True)

            if not inputs:
                self.send_json(400, {"error": "inputs required"})
                return

            n_timesteps = len(inputs)
            trajectory, predicted_map, deviation_score = make_trajectory(n_timesteps, horizon)

            response = {
                "predicted_map": predicted_map,
                "deviation_score": deviation_score,
                "checkpoint_version": CHECKPOINT_VERSION,
                "timesteps": horizon,
                "mock": True
            }
            if return_traj:
                response["trajectory"] = trajectory

            self.send_json(200, response)

        elif path == "/v1/predict/batch":
            cases = body.get("cases", [])
            return_traj = body.get("return_trajectory", True)

            results = []
            for case in cases:
                inputs = case.get("inputs", [])
                horizon = case.get("horizon_minutes", 15)
                n_timesteps = len(inputs) if inputs else 15
                trajectory, predicted_map, deviation_score = make_trajectory(n_timesteps, horizon)

                result = {
                    "case_id": case.get("case_id", ""),
                    "predicted_map": predicted_map,
                    "deviation_score": deviation_score,
                    "mock": True
                }
                if return_traj:
                    result["trajectory"] = trajectory
                results.append(result)

            self.send_json(200, {
                "results": results,
                "checkpoint_version": CHECKPOINT_VERSION
            })

        else:
            self.send_json(404, {"error": "not found"})


if __name__ == "__main__":
    port = 8765
    server = HTTPServer(("localhost", port), MockHandler)
    print(f"Margam mock server running at http://localhost:{port}/v1")
    print(f"Set: MARGAM_API_ENDPOINT=http://localhost:{port}/v1")
    print(f"Trajectories are random — not real physics. Use for shape/flow testing only.")
    print(f"Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
