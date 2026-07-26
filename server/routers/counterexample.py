import json
import os
from pathlib import Path

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from server.db import get_conn, get_problem_detail
from server.utils import parse_time_limit, run_one, strip_html

router = APIRouter(prefix="/api")

TESTCASE_AC_BASE = "https://api.testcase.ac"
FALLBACK_TIME_MULTIPLIER = 3
FALLBACK_ITERATIONS = 10

REF_DIR = Path(__file__).resolve().parent.parent.parent / "testcases"
REF_DIR.mkdir(exist_ok=True)


class FindCounterexampleRequest(BaseModel):
    code: str


def _ref_path(problem_id: int) -> Path:
    return REF_DIR / f"{problem_id}_ref.json"


_MAX_OUTPUT_CHARS = 2000


def _truncate(text: str) -> str:
    if len(text) <= _MAX_OUTPUT_CHARS:
        return text
    return text[:_MAX_OUTPUT_CHARS] + f"\n... ({len(text) - _MAX_OUTPUT_CHARS}자 생략)"


@router.post("/problems/{problem_id}/find-counterexample")
async def find_counterexample(problem_id: int, req: FindCounterexampleRequest):
    async with httpx.AsyncClient(timeout=15) as client:
        try:
            detail_res = await client.get(
                f"{TESTCASE_AC_BASE}/api/problems/boj/{problem_id}"
            )
        except httpx.RequestError as e:
            raise HTTPException(502, f"testcase.ac 연결 실패: {e}")

        if detail_res.status_code == 200:
            detail = detail_res.json()
            has_generators = bool(
                detail.get("generators") or detail.get("testcases") or detail.get("singlegens")
            )
            if detail.get("correctCodes") and has_generators:
                try:
                    stress_res = await client.post(
                        f"{TESTCASE_AC_BASE}/api/problems/boj/{problem_id}/stress",
                        json={"targetCode": req.code, "targetCodeLang": "python3"},
                        timeout=100,
                    )
                except httpx.RequestError as e:
                    raise HTTPException(502, f"testcase.ac 연결 실패: {e}")

                if stress_res.status_code == 429:
                    raise HTTPException(429, "testcase.ac 요청 한도를 초과했습니다. 잠시 후 다시 시도하세요.")
                if stress_res.status_code != 200:
                    detail_msg = (
                        stress_res.json().get("detail", stress_res.text)
                        if stress_res.headers.get("content-type", "").startswith("application/json")
                        else stress_res.text
                    )
                    raise HTTPException(502, f"testcase.ac 오류: {detail_msg}")

                return {"registered": True, "source": "testcase-ac", **stress_res.json()}
        elif detail_res.status_code != 404:
            raise HTTPException(502, f"testcase.ac 오류: {detail_res.status_code}")

    return _run_ai_fallback(problem_id, req.code)


def _run_ai_fallback(problem_id: int, code: str) -> dict:
    conn = get_conn()
    prob = get_problem_detail(conn, problem_id)
    conn.close()
    if not prob:
        raise HTTPException(404, "문제를 찾을 수 없습니다.")

    ref = _load_or_build_reference(problem_id, prob)
    if ref.get("error"):
        return {"registered": False, "source": "ai-fallback", "errorMessage": ref["error"]}

    limit_sec = parse_time_limit(prob["time_limit"]) * FALLBACK_TIME_MULTIPLIER
    inputs = _generate_inputs(ref["generator_code"])

    for stdin in inputs:
        correct = run_one(ref["reference_code"], stdin, limit_sec)
        if correct["status"] != "OK":
            continue  # 정답 코드가 실패하는 입력은 제너레이터 결함 가능성 → 건너뜀

        target = run_one(code, stdin, limit_sec)
        expected = correct["stdout"].rstrip()
        actual = (target["stdout"] or "").rstrip()

        if target["status"] == "OK" and actual == expected:
            continue

        verdict = {"TLE": "TLE", "ERROR": "RTE"}.get(target["status"], "WA")
        return {
            "registered": True,
            "source": "ai-fallback",
            "status": "found",
            "counterexample": {
                "verdict": verdict,
                "testcase": {"text": _truncate(stdin)},
                "targetOutput": {"text": _truncate(target["stdout"] or target.get("stderr", ""))},
                "correctOutput": {"text": _truncate(correct["stdout"])},
            },
        }

    return {
        "registered": True,
        "source": "ai-fallback",
        "status": "not_found",
        "totalAttempted": len(inputs),
    }


def _load_or_build_reference(problem_id: int, prob: dict) -> dict:
    path = _ref_path(problem_id)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return {"error": "ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다."}

    desc = strip_html(prob["description"])
    inp_fmt = strip_html(prob["input_desc"])
    out_fmt = strip_html(prob["output_desc"])
    samples = prob["samples"]
    samples_text = "\n\n".join(
        f"입력:\n{s['input'].strip()}\n출력:\n{s['output'].strip()}" for s in samples
    )

    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    reference_code = _generate_reference_code(client, prob, desc, inp_fmt, out_fmt, samples_text)
    if reference_code is None:
        return {"error": "정답 코드 생성 실패"}

    limit_sec = parse_time_limit(prob["time_limit"]) * FALLBACK_TIME_MULTIPLIER
    for s in samples:
        result = run_one(reference_code, s["input"], limit_sec)
        if result["status"] != "OK" or (result["stdout"] or "").rstrip() != s["output"].rstrip():
            return {"error": "AI가 생성한 정답 코드가 샘플 테케를 통과하지 못했습니다."}

    generator_code = _generate_generator_code(client, prob, desc, inp_fmt)
    if generator_code is None:
        return {"error": "입력 생성기 생성 실패"}

    data = {
        "problem_id": problem_id,
        "reference_code": reference_code,
        "generator_code": generator_code,
    }
    _ref_path(problem_id).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def _generate_reference_code(client, prob, desc, inp_fmt, out_fmt, samples_text):
    prompt = f"""다음 백준 알고리즘 문제의 정답 파이썬 코드를 작성해주세요.

문제: {prob['title']}
설명: {desc}
입력 형식: {inp_fmt}
출력 형식: {out_fmt}
샘플:
{samples_text}

코드는 sys.stdin에서 직접 입력을 읽고 print로 출력하는 완결된 스크립트여야 합니다.
작성했으면 submit_code 도구를 호출해서 코드를 전달하세요."""

    tool = {
        "name": "submit_code",
        "description": "작성한 정답 코드를 제출한다.",
        "input_schema": {
            "type": "object",
            "properties": {"code": {"type": "string"}},
            "required": ["code"],
        },
    }
    try:
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=[tool],
            tool_choice={"type": "tool", "name": "submit_code"},
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception:
        return None

    for block in msg.content:
        if block.type == "tool_use" and block.name == "submit_code":
            return block.input.get("code")
    return None


def _generate_generator_code(client, prob, desc, inp_fmt):
    prompt = f"""다음 백준 알고리즘 문제의 입력 제약조건에 맞는 랜덤 입력을 생성하는
파이썬 함수 generate(rng, kind)를 작성해주세요.

문제: {prob['title']}
설명: {desc}
입력 형식: {inp_fmt}

- rng는 random.Random 인스턴스입니다. 반드시 rng를 통해서만 난수를 생성하세요 (random 모듈 직접 호출 금지).
- kind는 "general"(평범한 입력), "edge"(경계값: 최솟값/최댓값 등), "stress"(제약조건 최댓값 근처의 큰 입력) 중 하나입니다.
- generate 함수는 완성된 stdin 문자열 하나를 return해야 합니다 (개행 포함, 실행 시 그대로 표준입력으로 들어감).
- import는 함수 내부 또는 최상단에 필요한 만큼 포함하세요.

작성했으면 submit_generator 도구를 호출해서 코드를 전달하세요."""

    tool = {
        "name": "submit_generator",
        "description": "작성한 입력 생성기 코드를 제출한다.",
        "input_schema": {
            "type": "object",
            "properties": {"code": {"type": "string"}},
            "required": ["code"],
        },
    }
    try:
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            tools=[tool],
            tool_choice={"type": "tool", "name": "submit_generator"},
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception:
        return None

    for block in msg.content:
        if block.type == "tool_use" and block.name == "submit_generator":
            return block.input.get("code")
    return None


_GENERATOR_RUNNER = """
import json, random, sys

{generator_code}

kinds = ["general"] * 5 + ["edge"] * 3 + ["stress"] * 2
inputs = []
for i, kind in enumerate(kinds):
    rng = random.Random(1000 + i)
    try:
        inputs.append(generate(rng, kind))
    except Exception:
        pass
sys.stdout.write(json.dumps(inputs))
"""


def _generate_inputs(generator_code: str) -> list[str]:
    script = _GENERATOR_RUNNER.format(generator_code=generator_code)
    result = run_one(script, "", limit_sec=10)
    if result["status"] != "OK":
        return []
    try:
        return json.loads(result["stdout"])
    except (json.JSONDecodeError, TypeError):
        return []
