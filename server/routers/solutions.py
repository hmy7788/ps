import re
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


def _strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", "", html or "")
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&nbsp;", " ")
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _build_readme(prob: dict) -> str:
    title      = prob["title"]
    problem_id = prob["id"]
    grade      = _grade(prob["level"])
    tags       = ", ".join(prob.get("tags") or [])
    desc       = _strip_html(prob.get("description", ""))
    inp        = _strip_html(prob.get("input_desc", ""))
    out        = _strip_html(prob.get("output_desc", ""))

    samples_md = ""
    for i, s in enumerate(prob.get("samples") or [], 1):
        samples_md += f"\n**입력 {i}**\n```\n{s['input'].strip()}\n```\n"
        samples_md += f"**출력 {i}**\n```\n{s['output'].strip()}\n```\n"

    return f"""# {problem_id}번: {title}

> https://www.acmicpc.net/problem/{problem_id}
> 난이도: {grade} (레벨 {prob["level"]}) | 태그: {tags}

---

## 문제

{desc}

## 입력

{inp}

## 출력

{out}

## 예제
{samples_md}
"""


class SaveRequest(BaseModel):
    code: str
    memo: str = ""


@router.post("/problems/{problem_id}/save-solution")
def save_solution(problem_id: int, req: SaveRequest):
    conn = get_conn()
    prob = get_problem_detail(conn, problem_id)
    if not prob:
        conn.close()
        raise HTTPException(404, "문제를 찾을 수 없습니다.")

    grade      = _grade(prob["level"])
    title      = prob["title"]
    safe_title = title.replace("/", "_").replace("\\", "_")
    folder     = ROOT / "백준" / grade / f"{problem_id}. {safe_title}"
    folder.mkdir(parents=True, exist_ok=True)

    # 풀이 파일명: memo 있으면 {title}_{memo}.py
    memo = req.memo.strip()
    safe_memo = re.sub(r'[^\w가-힣]', '_', memo) if memo else ""
    filename = f"{safe_title}_{safe_memo}.py" if safe_memo else f"{safe_title}.py"
    (folder / filename).write_text(req.code, encoding="utf-8")

    # README는 처음 저장 시에만 생성 (이후엔 덮어쓰지 않음)
    readme_path = folder / "README.md"
    if not readme_path.exists():
        readme_path.write_text(_build_readme(prob), encoding="utf-8")

    mark_solved(conn, problem_id)
    conn.close()

    return {
        "saved":    True,
        "path":     str(folder.relative_to(ROOT)),
        "filename": filename,
    }
