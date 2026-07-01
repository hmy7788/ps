import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent.parent / "problems.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    _migrate(conn)
    return conn


def _migrate(conn: sqlite3.Connection) -> None:
    cols = {r[1] for r in conn.execute("PRAGMA table_info(problems)")}
    if "solved" not in cols:
        conn.execute("ALTER TABLE problems ADD COLUMN solved INTEGER DEFAULT 0")
    if "solved_at" not in cols:
        conn.execute("ALTER TABLE problems ADD COLUMN solved_at TEXT")
    conn.commit()


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
    solved_only: bool = False,
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
        for tag in tags:
            conditions.append("tags LIKE ?")
            params.append(f'%"{tag}"%')

    if solved_only:
        conditions.append("solved = 1")

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    total = conn.execute(
        f"SELECT COUNT(*) FROM problems {where}", params
    ).fetchone()[0]

    offset = (page - 1) * size
    rows = conn.execute(
        f"""
        SELECT id, title, level, tags, time_limit, memory_limit,
               accepted_user_count, solved
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
               samples, time_limit, memory_limit, accepted_user_count, average_tries,
               solved, solved_at
        FROM problems WHERE id = ?
        """,
        (problem_id,),
    ).fetchone()
    return _parse_row(row) if row else None


def mark_solved(conn: sqlite3.Connection, problem_id: int) -> None:
    conn.execute(
        "UPDATE problems SET solved=1, solved_at=? WHERE id=?",
        (datetime.now(timezone.utc).isoformat(), problem_id),
    )
    conn.commit()


def sync_solved_from_fs(conn: sqlite3.Connection, root: Path) -> int:
    """백준/ 폴더를 스캔해 풀이 파일이 있는 문제를 solved=1로 동기화. 변경된 수 반환."""
    import re
    baekjoon_dir = root / "백준"
    if not baekjoon_dir.exists():
        return 0
    updated = 0
    seen: set[int] = set()
    for py_file in baekjoon_dir.rglob("*.py"):
        folder_name = py_file.parent.name
        m = re.match(r'^(\d+)', folder_name)
        if not m:
            continue
        problem_id = int(m.group(1))
        if problem_id in seen:
            continue
        seen.add(problem_id)
        row = conn.execute("SELECT solved FROM problems WHERE id=?", (problem_id,)).fetchone()
        if row and row["solved"] == 0:
            mtime = datetime.fromtimestamp(py_file.stat().st_mtime, tz=timezone.utc).isoformat()
            conn.execute(
                "UPDATE problems SET solved=1, solved_at=? WHERE id=?",
                (mtime, problem_id),
            )
            updated += 1
    conn.commit()
    return updated


def get_all_tags(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute("SELECT tag FROM all_tags ORDER BY tag").fetchall()
    return [r["tag"] for r in rows]


def get_stats(conn: sqlite3.Connection) -> dict:
    # 총 풀었던 수
    total = conn.execute("SELECT COUNT(*) FROM problems WHERE solved=1").fetchone()[0]

    # 레벨별 분포
    rows = conn.execute(
        "SELECT level, COUNT(*) as cnt FROM problems WHERE solved=1 GROUP BY level ORDER BY level"
    ).fetchall()
    by_level = {r["level"]: r["cnt"] for r in rows}

    # 태그 분포 (풀었던 문제의 태그 집계)
    solved_rows = conn.execute("SELECT tags FROM problems WHERE solved=1").fetchall()
    tag_count: dict[str, int] = {}
    for row in solved_rows:
        for tag in json.loads(row["tags"] or "[]"):
            tag_count[tag] = tag_count.get(tag, 0) + 1
    top_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:10]

    # 최근 풀이 (solved_at 기준 최근 20개)
    recent_rows = conn.execute(
        """SELECT id, title, level, solved_at FROM problems
           WHERE solved=1 AND solved_at IS NOT NULL
           ORDER BY solved_at DESC LIMIT 20"""
    ).fetchall()
    recent = [dict(r) for r in recent_rows]

    return {
        "total":    total,
        "by_level": by_level,
        "top_tags": [{"tag": t, "count": c} for t, c in top_tags],
        "recent":   recent,
    }
