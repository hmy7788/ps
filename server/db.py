import json
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent.parent / "problems.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def _parse_row(row: sqlite3.Row) -> dict[str, Any]:
    d = dict(row)
    d["tags"] = json.loads(d["tags"] or "[]")
    if "samples" in d:
        d["samples"] = json.loads(d["samples"] or "[]")
    return d


def get_problems(
    conn: sqlite3.Connection,
    q: str | None,
    tags: list[str],
    levels: list[int],
    page: int,
    size: int,
) -> tuple[int, list[dict]]:
    conditions: list[str] = []
    params: list[Any] = []

    if q:
        conditions.append("(title LIKE ? OR CAST(id AS TEXT) LIKE ?)")
        like = f"%{q}%"
        params += [like, like]

    if levels:
        placeholders = ",".join("?" * len(levels))
        conditions.append(f"level IN ({placeholders})")
        params += levels

    if tags:
        # 모든 태그를 AND 조건으로 포함하는 문제만 (tags 컬럼은 JSON 문자열)
        for tag in tags:
            conditions.append("tags LIKE ?")
            params.append(f'%"{tag}"%')

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    total = conn.execute(
        f"SELECT COUNT(*) FROM problems {where}", params
    ).fetchone()[0]

    offset = (page - 1) * size
    rows = conn.execute(
        f"""
        SELECT id, title, level, tags, time_limit, memory_limit, accepted_user_count
        FROM problems {where}
        ORDER BY level ASC, id ASC
        LIMIT ? OFFSET ?
        """,
        params + [size, offset],
    ).fetchall()

    return total, [_parse_row(r) for r in rows]


def get_problem_detail(conn: sqlite3.Connection, problem_id: int) -> dict | None:
    row = conn.execute(
        """
        SELECT id, title, level, tags, description, input_desc, output_desc,
               samples, time_limit, memory_limit, accepted_user_count, average_tries
        FROM problems WHERE id = ?
        """,
        (problem_id,),
    ).fetchone()
    return _parse_row(row) if row else None


def get_all_tags(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute("SELECT tag FROM all_tags ORDER BY tag").fetchall()
    return [r["tag"] for r in rows]
