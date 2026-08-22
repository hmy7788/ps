import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, HTTPException

from server.db import (
    get_conn,
    create_custom_problem,
    update_custom_problem,
    delete_custom_problem,
    get_custom_raw,
)
from server.models import CustomProblemCreate, Sample

router = APIRouter(prefix="/api")

TESTCASES_DIR = Path(__file__).resolve().parent.parent.parent / "testcases"
TESTCASES_DIR.mkdir(exist_ok=True)

MIN_LEVEL, MAX_LEVEL = 6, 20


def _tc_path(problem_id: int) -> Path:
    return TESTCASES_DIR / f"{problem_id}.json"


def _write_testcases(problem_id: int, samples: list[Sample], hidden: list[Sample]) -> None:
    """히든 테케가 있으면 그걸, 없으면 샘플을 채점용 테케로 저장해 '제출' 탭이 바로 동작하게 한다."""
    source = hidden if hidden else samples
    testcases = [
        {"input": tc.input, "output": tc.output, "type": "general", "note": "커스텀 테케"}
        for tc in source
    ]
    data = {
        "problem_id": problem_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(testcases),
        "testcases": testcases,
    }
    _tc_path(problem_id).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _validate(req: CustomProblemCreate) -> None:
    if not req.title.strip():
        raise HTTPException(400, "제목을 입력해주세요.")
    if not (MIN_LEVEL <= req.level <= MAX_LEVEL):
        raise HTTPException(400, f"난이도는 {MIN_LEVEL}~{MAX_LEVEL} 사이여야 합니다.")
    if not req.samples:
        raise HTTPException(400, "예제를 최소 1개 이상 입력해주세요.")


def _to_row_data(req: CustomProblemCreate) -> dict:
    from server.utils import render_custom_markdown

    return {
        "title": req.title.strip(),
        "level": req.level,
        "tags": req.tags,
        "description_html": render_custom_markdown(req.description),
        "input_html": render_custom_markdown(req.input_desc),
        "output_html": render_custom_markdown(req.output_desc),
        "raw_description": req.description,
        "raw_input_desc": req.input_desc,
        "raw_output_desc": req.output_desc,
        "samples": [s.model_dump() for s in req.samples],
        "time_limit": req.time_limit,
        "memory_limit": req.memory_limit,
    }


@router.post("/custom-problems")
def create_problem(req: CustomProblemCreate):
    _validate(req)
    conn = get_conn()
    new_id = create_custom_problem(conn, _to_row_data(req))
    conn.close()
    _write_testcases(new_id, req.samples, req.hidden_testcases)
    return {"id": new_id}


@router.put("/custom-problems/{problem_id}")
def update_problem(problem_id: int, req: CustomProblemCreate):
    if problem_id >= 0:
        raise HTTPException(403, "원본 아카이브 문제는 수정할 수 없습니다.")
    _validate(req)
    conn = get_conn()
    ok = update_custom_problem(conn, problem_id, _to_row_data(req))
    conn.close()
    if not ok:
        raise HTTPException(404, "커스텀 문제를 찾을 수 없습니다.")
    _write_testcases(problem_id, req.samples, req.hidden_testcases)
    return {"id": problem_id}


@router.delete("/custom-problems/{problem_id}")
def delete_problem(problem_id: int):
    if problem_id >= 0:
        raise HTTPException(403, "원본 아카이브 문제는 삭제할 수 없습니다.")
    conn = get_conn()
    ok = delete_custom_problem(conn, problem_id)
    conn.close()
    if not ok:
        raise HTTPException(404, "커스텀 문제를 찾을 수 없습니다.")
    _tc_path(problem_id).unlink(missing_ok=True)
    return {"deleted": True}


@router.get("/custom-problems/{problem_id}/edit")
def get_edit_data(problem_id: int):
    if problem_id >= 0:
        raise HTTPException(403, "원본 아카이브 문제입니다.")
    conn = get_conn()
    data = get_custom_raw(conn, problem_id)
    conn.close()
    if not data:
        raise HTTPException(404, "커스텀 문제를 찾을 수 없습니다.")

    # 저장된 테케 중 샘플과 겹치지 않는 것만 "히든 테케"로 되돌려준다.
    hidden: list[dict] = []
    tc_path = _tc_path(problem_id)
    if tc_path.exists():
        tc_data = json.loads(tc_path.read_text(encoding="utf-8"))
        sample_set = {(s["input"], s["output"]) for s in data["samples"]}
        hidden = [
            {"input": tc["input"], "output": tc["output"]}
            for tc in tc_data.get("testcases", [])
            if (tc["input"], tc["output"]) not in sample_set
        ]

    return {
        "id": data["id"],
        "title": data["title"],
        "level": data["level"],
        "tags": data["tags"],
        "description": data["raw_description"] or "",
        "input_desc": data["raw_input_desc"] or "",
        "output_desc": data["raw_output_desc"] or "",
        "samples": data["samples"],
        "hidden_testcases": hidden,
        "time_limit": data["time_limit"],
        "memory_limit": data["memory_limit"],
    }
