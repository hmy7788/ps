import subprocess
import sys
import tempfile
import time
from pathlib import Path

from fastapi import APIRouter

from server.models import RunRequest, RunResponse
from server.utils import last_error_line, parse_time_limit

router = APIRouter(prefix="/api")

PYTHON = sys.executable
PYTHON_TIME_MULTIPLIER = 3


@router.post("/run", response_model=RunResponse)
def run_code(req: RunRequest):
    base_limit = parse_time_limit(req.time_limit)
    python_limit = base_limit * PYTHON_TIME_MULTIPLIER

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as f:
        f.write(req.code)
        tmp_path = Path(f.name)

    try:
        start = time.perf_counter()
        try:
            result = subprocess.run(
                [PYTHON, "-X", "utf8", str(tmp_path)],
                input=req.stdin,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=python_limit,
            )
            elapsed_ms = (time.perf_counter() - start) * 1000

            status = "OK" if result.returncode == 0 else "ERROR"
            stderr = last_error_line(result.stderr) if status == "ERROR" else result.stderr
            return RunResponse(
                status=status,
                stdout=result.stdout,
                stderr=stderr,
                elapsed_ms=round(elapsed_ms, 2),
                time_limit_ms=round(python_limit * 1000, 0),
                raw_time_limit=req.time_limit,
            )

        except subprocess.TimeoutExpired:
            return RunResponse(
                status="TLE",
                stdout="",
                stderr="",
                elapsed_ms=None,
                time_limit_ms=round(python_limit * 1000, 0),
                raw_time_limit=req.time_limit,
            )
    finally:
        tmp_path.unlink(missing_ok=True)
