import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import bleach
import markdown

PYTHON = sys.executable

MD_ALLOWED_TAGS = [
    "p", "br", "hr",
    "strong", "b", "em", "i", "u", "s", "del", "mark",
    "code", "pre", "blockquote",
    "ul", "ol", "li",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "a", "img",
    "table", "thead", "tbody", "tr", "th", "td",
    "span", "div",
]
MD_ALLOWED_ATTRS = {
    "a": ["href", "title"],
    "img": ["src", "alt", "title"],
    "*": ["class"],
}


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


def render_custom_markdown(raw: str) -> str:
    """커스텀 문제 설명/입출력 형식에 마크다운·HTML 문법을 허용하되,
    이후 innerHTML로 렌더링되므로 bleach로 위험한 태그/속성(script, on* 등)을 걸러낸다."""
    raw = (raw or "").strip()
    if not raw:
        return ""
    rendered = markdown.markdown(raw, extensions=["fenced_code", "tables", "nl2br", "sane_lists"])
    return bleach.clean(rendered, tags=MD_ALLOWED_TAGS, attributes=MD_ALLOWED_ATTRS, strip=True)


def last_error_line(stderr: str) -> str:
    """트레이스백에서 임시파일 경로·스택프레임을 다 걷어내고 마지막 줄(실제 예외 메시지)만 남긴다."""
    lines = [line for line in stderr.splitlines() if line.strip()]
    return lines[-1] if lines else stderr


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
                [PYTHON, "-X", "utf8", str(tmp)],
                input=stdin,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=limit_sec,
            )
            elapsed = round((time.perf_counter() - t0) * 1000, 2)
            status = "OK" if proc.returncode == 0 else "ERROR"
            return {"status": status, "stdout": proc.stdout, "stderr": proc.stderr, "elapsed_ms": elapsed}
        except subprocess.TimeoutExpired:
            return {"status": "TLE", "stdout": "", "stderr": "", "elapsed_ms": None}
    finally:
        tmp.unlink(missing_ok=True)
