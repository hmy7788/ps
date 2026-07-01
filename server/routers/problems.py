import re
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
import sqlite3

from server.db import get_conn, get_problems, get_problem_detail, get_all_tags, get_stats, get_heatmap_and_streak
from server.models import ProblemListResponse, ProblemDetail, ProblemSummary

PROBLEMS_DIR = Path(__file__).resolve().parent.parent.parent / "all_problems" / "problems"


def _rewrite_img_src(html: str, problem_id: int) -> str:
    """상대 경로 이미지 src를 API 경로로 교체."""
    return re.sub(
        r'src="(?!https?://)([^"]+)"',
        lambda m: f'src="/api/problems/{problem_id}/images/{m.group(1)}"',
        html,
    )

router = APIRouter(prefix="/api")


def db():
    conn = get_conn()
    try:
        yield conn
    finally:
        conn.close()


@router.get("/problems", response_model=ProblemListResponse)
def list_problems(
    q: str | None = Query(None, description="제목/번호 검색"),
    tags: str | None = Query(None, description="태그 콤마 구분, 예: dp,graph"),
    levels: str | None = Query(None, description="레벨 콤마 구분, 예: 6,7,8,9,10"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    solved: int | None = Query(None, description="1이면 푼 문제만"),
    conn: sqlite3.Connection = Depends(db),
):
    tag_list = [t.strip() for t in tags.split(",")] if tags else []
    level_list = [int(l.strip()) for l in levels.split(",")] if levels else []

    total, items = get_problems(conn, q, tag_list, level_list, page, size, solved_only=(solved == 1))
    return ProblemListResponse(
        total=total,
        page=page,
        size=size,
        items=[ProblemSummary(**item) for item in items],
    )


@router.get("/problems/{problem_id}/images/{filename}")
def get_problem_image(problem_id: int, filename: str):
    path = PROBLEMS_DIR / str(problem_id) / filename
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다.")
    return FileResponse(str(path))


@router.get("/problems/{problem_id}", response_model=ProblemDetail)
def get_problem(problem_id: int, conn: sqlite3.Connection = Depends(db)):
    data = get_problem_detail(conn, problem_id)
    if not data:
        raise HTTPException(status_code=404, detail="문제를 찾을 수 없습니다.")
    for field in ("description", "input_desc", "output_desc"):
        if data.get(field):
            data[field] = _rewrite_img_src(data[field], problem_id)
    return ProblemDetail(**data)


@router.get("/tags", response_model=list[str])
def list_tags(conn: sqlite3.Connection = Depends(db)):
    return get_all_tags(conn)


@router.get("/stats")
def stats(conn: sqlite3.Connection = Depends(db)):
    return get_stats(conn)


@router.get("/stats/heatmap")
def heatmap(conn: sqlite3.Connection = Depends(db)):
    return get_heatmap_and_streak(conn)
