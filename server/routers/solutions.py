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


@router.get("/problems/{problem_id}/solutions")
def list_solutions(problem_id: int):
    import re
    baekjoon = ROOT / "백준"
    if not baekjoon.exists():
        return {"files": []}

    pattern = re.compile(r'^' + str(problem_id) + r'[\.\s]')
    files = []
    for grade_dir in baekjoon.iterdir():
        if not grade_dir.is_dir():
            continue
        for folder in grade_dir.iterdir():
            if folder.is_dir() and pattern.match(folder.name):
                for py in sorted(folder.glob("*.py"), key=lambda f: f.stat().st_mtime, reverse=True):
                    files.append({
                        "filename": py.name,
                        "mtime":    py.stat().st_mtime,
                    })

    files.sort(key=lambda f: f["mtime"], reverse=True)
    return {"files": files}


@router.get("/problems/{problem_id}/last-solution")
def last_solution(problem_id: int):
    import re
    baekjoon = ROOT / "백준"
    if not baekjoon.exists():
        return {"exists": False}

    # 폴더명이 "1010. title" 또는 "1010. title" 등 다양하므로 숫자 prefix로 찾음
    pattern = re.compile(r'^' + str(problem_id) + r'[\.\s]')
    all_py: list[Path] = []
    for grade_dir in baekjoon.iterdir():
        if not grade_dir.is_dir():
            continue
        for folder in grade_dir.iterdir():
            if folder.is_dir() and pattern.match(folder.name):
                all_py.extend(folder.glob("*.py"))

    if not all_py:
        return {"exists": False}

    latest = max(all_py, key=lambda f: f.stat().st_mtime)
    return {
        "exists":   True,
        "filename": latest.name,
        "code":     latest.read_text(encoding="utf-8"),
    }


@router.get("/problems/{problem_id}/solutions/{filename}")
def get_solution(problem_id: int, filename: str):
    import re
    baekjoon = ROOT / "백준"
    pattern = re.compile(r'^' + str(problem_id) + r'[\.\s]')
    for grade_dir in baekjoon.iterdir():
        if not grade_dir.is_dir():
            continue
        for folder in grade_dir.iterdir():
            if folder.is_dir() and pattern.match(folder.name):
                f = folder / filename
                if f.exists() and f.suffix == ".py":
                    return {"code": f.read_text(encoding="utf-8")}
    raise HTTPException(404, "파일을 찾을 수 없습니다.")


@router.post("/problems/{problem_id}/save-solution")
def save_solution(problem_id: int, req: SaveRequest):
    conn = get_conn()
    prob = get_problem_detail(conn, problem_id)
    if not prob:
        conn.close()
        raise HTTPException(404, "문제를 찾을 수 없습니다.")

    grade      = _grade(prob["level"])
    title      = prob["title"]
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)

    # 기존 폴더 우선 재사용 (BaekjoonHub 등이 만든 폴더 중복 방지)
    grade_dir = ROOT / "백준" / grade
    pattern   = re.compile(rf"^{re.escape(str(problem_id))}\.")
    folder    = next(
        (d for d in grade_dir.iterdir() if d.is_dir() and pattern.match(d.name)),
        None
    ) if grade_dir.exists() else None
    if folder is None:
        folder = grade_dir / f"{problem_id}. {safe_title}"
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
