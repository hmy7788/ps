import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

PYTHON = sys.executable


def parse_time_limit(raw: str) -> float:
    """'2 초', '1.5초', '3000ms' 등을 초(float)로 변환. 파싱 실패 시 5.0 반환."""
    if not raw:
        return 5.0
    raw_lower = raw.lower()
    match = re.search(r"[\d.]+", raw_lower)
    if not match:
        return 5.0
    value = float(match.group())
    if "ms" in raw_lower:
        return value / 1000
    return value  # 초 단위


def strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html or "")
    return re.sub(r"\s+", " ", text).strip()


def run_one(code: str, stdin: str, limit_sec: float) -> dict:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as f:
        f.write(code)
        tmp = Path(f.name)
    try:
        t0 = time.perf_counter()
        try:
            proc = subprocess.run(
                [PYTHON, str(tmp)],
                input=stdin,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=limit_sec,
            )
            elapsed = round((time.perf_counter() - t0) * 1000, 2)
            status = "OK" if proc.returncode == 0 else "ERROR"
            return {"status": status, "stdout": proc.stdout, "stderr": proc.stderr, "elapsed_ms": elapsed}
        except subprocess.TimeoutExpired:
            return {"status": "TLE", "stdout": "", "stderr": "", "elapsed_ms": None}
    finally:
        tmp.unlink(missing_ok=True)
