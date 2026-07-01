from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from server.db import get_conn, get_problem_detail, mark_solved

router = APIRouter(prefix="/api")

ROOT = Path(__file__).resolve().parent.parent.parent

LEVEL_GRADE = {
    range(1, 6):   "Bronze",
    range(6, 11):  "Silver",
    range(11, 16): "Gold",
    range(16, 21): "Platinum",
    range(21, 26): "Diamond",
    range(26, 31): "Ruby",
}


def _grade(level: int) -> str:
    for r, name in LEVEL_GRADE.items():
        if level in r:
            return name
    return "Unknown"


class SaveRequest(BaseModel):
    code: str


@router.post("/problems/{problem_id}/save-solution")
def save_solution(problem_id: int, req: SaveRequest):
    conn = get_conn()
    prob = get_problem_detail(conn, problem_id)
    if not prob:
        conn.close()
        raise HTTPException(404, "문제를 찾을 수 없습니다.")

    grade   = _grade(prob["level"])
    title   = prob["title"]
    safe_title = title.replace("/", "_").replace("\\", "_")
    folder  = ROOT / "백준" / grade / f"{problem_id}. {safe_title}"
    folder.mkdir(parents=True, exist_ok=True)

    # 풀이 파일
    (folder / f"{safe_title}.py").write_text(req.code, encoding="utf-8")

    # README (BaekjoonHub 포맷)
    readme = f"""# {problem_id}번: {title}

### 문제 링크
https://www.acmicpc.net/problem/{problem_id}

### 난이도
{grade} (레벨 {prob["level"]})

### 태그
{", ".join(prob.get("tags") or [])}
"""
    (folder / "README.md").write_text(readme, encoding="utf-8")

    mark_solved(conn, problem_id)
    conn.close()

    return {
        "saved": True,
        "path": str(folder.relative_to(ROOT)),
    }
