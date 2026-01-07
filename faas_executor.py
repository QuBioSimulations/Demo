import subprocess
import json
import uuid
import os
import shutil
from datetime import datetime

def run_function(payload):
    job_id = str(uuid.uuid4())

    # Try environment override first, then fall back to PATH lookup
    julia_exec = os.environ.get("JULIA_EXE") or shutil.which("julia")
    if julia_exec is None:
        raise FileNotFoundError(
            "Julia executable not found. Please install Julia (https://julialang.org/downloads/) "
            "and ensure 'julia' is on your PATH, or set the JULIA_EXE environment variable to the julia executable path."
        )

    process = subprocess.Popen(
        [julia_exec, "julia/recursive_ode.jl"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(json.dumps(payload))

    if process.returncode != 0:
        raise RuntimeError(stderr)

    result = json.loads(stdout)

    log = {
        "job_id": job_id,
        "timestamp": datetime.utcnow().isoformat(),
        "input": payload,
        "output": result
    }

    with open(f"logs/{job_id}.json", "w") as f:
        json.dump(log, f, indent=2)

    return result

if __name__ == "__main__":
    payload = {
        "x0": 0.0,
        "y0": 1.0,
        "step": 0.1,
        "steps": 10
    }

    result = run_function(payload)
    print("FaaS result:", result)
