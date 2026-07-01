import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from server.db import get_conn, get_problem_detail
from server.utils import parse_time_limit

router = APIRouter(prefix="/api")

PYTHON = sys.executable
PYTHON_TIME_MULTIPLIER = 3
TESTCASES_DIR = Path(__file__).resolve().parent.parent.parent / "testcases"
TESTCASES_DIR.mkdir(exist_ok=True)


def _tc_path(problem_id: int) -> Path:
    return TESTCASES_DIR / f"{problem_id}.json"


def _strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html or "")
    return re.sub(r"\s+", " ", text).strip()


def _run_one(code: str, stdin: str, limit_sec: float) -> dict:
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
            return {"status": status, "stdout": proc.stdout, "elapsed_ms": elapsed}
        except subprocess.TimeoutExpired:
            return {"status": "TLE", "stdout": "", "elapsed_ms": None}
    finally:
        tmp.unlink(missing_ok=True)


# ── GET: 저장된 테케 조회 ────────────────────────────────
@router.get("/problems/{problem_id}/testcases")
def get_testcases(problem_id: int):
    p = _tc_path(problem_id)
    if not p.exists():
        return {"exists": False}
    data = json.loads(p.read_text(encoding="utf-8"))
    return {"exists": True, **data}


# ── POST: Claude API로 테케 생성 ─────────────────────────
@router.post("/problems/{problem_id}/generate-testcases")
async def generate_testcases(problem_id: int):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(400, "ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")

    conn = get_conn()
    prob = get_problem_detail(conn, problem_id)
    conn.close()
    if not prob:
        raise HTTPException(404, "문제를 찾을 수 없습니다.")

    desc     = _strip_html(prob["description"])
    inp_fmt  = _strip_html(prob["input_desc"])
    out_fmt  = _strip_html(prob["output_desc"])
    samples  = "\n\n".join(
        f"입력:\n{s['input'].strip()}\n출력:\n{s['output'].strip()}"
        for s in prob["samples"]
    )

    prompt = f"""백준 알고리즘 문제의 테스트케이스 10개를 생성해주세요.

문제: {prob['title']}
설명: {desc}
입력 형식: {inp_fmt}
출력 형식: {out_fmt}
샘플:
{samples}

생성 규칙:
- general 4개: 전형적인 입력
- edge 3개: 경계값 (최솟값, 최댓값, 특수 패턴)
- stress 3개: 큰 입력으로 시간복잡도 도전

output은 반드시 수학적으로 정확해야 합니다.

테스트케이스를 생성했으면 submit_testcases 도구를 호출해서 결과를 전달하세요."""

    tool = {
        "name": "submit_testcases",
        "description": "생성한 테스트케이스 목록을 제출한다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "testcases": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "input":  {"type": "string"},
                            "output": {"type": "string"},
                            "type":   {"type": "string", "enum": ["general", "edge", "stress"]},
                            "note":   {"type": "string"},
                        },
                        "required": ["input", "output", "type", "note"],
                    },
                },
            },
            "required": ["testcases"],
        },
    }

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=[tool],
            tool_choice={"type": "tool", "name": "submit_testcases"},
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        raise HTTPException(500, f"Claude API 오류: {e}")

    testcases = None
    for block in msg.content:
        if block.type == "tool_use" and block.name == "submit_testcases":
            testcases = block.input.get("testcases")
            break

    if not testcases:
        raise HTTPException(500, "테스트케이스 생성 실패: 모델이 도구를 호출하지 않았습니다.")

    data = {
        "problem_id":   problem_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count":        len(testcases),
        "testcases":    testcases,
    }
    _tc_path(problem_id).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return data


# ── POST: 제출 (AI 테케 전체 실행) ──────────────────────
class SubmitRequest(BaseModel):
    code: str
    time_limit: str


@router.post("/problems/{problem_id}/submit")
def submit(problem_id: int, req: SubmitRequest):
    p = _tc_path(problem_id)
    if not p.exists():
        raise HTTPException(404, "테스트케이스가 없습니다. 먼저 생성해주세요.")

    data      = json.loads(p.read_text(encoding="utf-8"))
    limit_sec = parse_time_limit(req.time_limit) * PYTHON_TIME_MULTIPLIER

    results = []
    for tc in data["testcases"]:
        r        = _run_one(req.code, tc["input"], limit_sec)
        actual   = (r["stdout"] or "").rstrip()
        expected = tc["output"].rstrip()
        passed   = (actual == expected) and r["status"] == "OK"
        results.append({
            "type":       tc.get("type", "general"),
            "note":       tc.get("note", ""),
            "status":     r["status"],
            "passed":     passed,
            "elapsed_ms": r.get("elapsed_ms"),
        })

    passed_n = sum(1 for r in results if r["passed"])
    return {"total": len(results), "passed": passed_n, "results": results}
