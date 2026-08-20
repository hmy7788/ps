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
    if "favorite" not in cols:
        conn.execute("ALTER TABLE problems ADD COLUMN favorite INTEGER DEFAULT 0")
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
    favorite_only: bool = False,
    in_progress_only: bool = False,
    draft_ids: set[int] | None = None,
) -> tuple[int, list[dict]]:
    draft_ids = draft_ids or set()
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

    if favorite_only:
        conditions.append("favorite = 1")

    if in_progress_only:
        if not draft_ids:
            return 0, []
        placeholders = ",".join("?" * len(draft_ids))
        conditions.append(f"id IN ({placeholders})")
        params += list(draft_ids)

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    total = conn.execute(
        f"SELECT COUNT(*) FROM problems {where}", params
    ).fetchone()[0]

    offset = (page - 1) * size
    rows = conn.execute(
        f"""
        SELECT id, title, level, tags, time_limit, memory_limit,
               accepted_user_count, solved, favorite
        FROM problems {where}
        ORDER BY level ASC, id ASC
        LIMIT ? OFFSET ?
        """,
        params + [size, offset],
    ).fetchall()

    items = [_parse_row(r) for r in rows]
    for item in items:
        item["in_progress"] = item["id"] in draft_ids
    return total, items


def get_problem_detail(conn: sqlite3.Connection, problem_id: int) -> dict | None:
    row = conn.execute(
        """
        SELECT id, title, level, tags, description, input_desc, output_desc,
               samples, time_limit, memory_limit, accepted_user_count, average_tries,
               solved, solved_at, favorite
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


def toggle_favorite(conn: sqlite3.Connection, problem_id: int) -> bool:
    """즐겨찾기 상태를 토글하고 변경 후 상태(True/False)를 반환."""
    row = conn.execute("SELECT favorite FROM problems WHERE id=?", (problem_id,)).fetchone()
    if row is None:
        raise ValueError("problem not found")
    new_val = 0 if row["favorite"] else 1
    conn.execute("UPDATE problems SET favorite=? WHERE id=?", (new_val, problem_id))
    conn.commit()
    return bool(new_val)


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


def get_heatmap_and_streak(conn: sqlite3.Connection) -> dict:
    rows = conn.execute(
        "SELECT solved_at FROM problems WHERE solved=1 AND solved_at IS NOT NULL"
    ).fetchall()

    # 날짜별 카운트 (YYYY-MM-DD)
    from collections import Counter
    day_count: Counter = Counter()
    for row in rows:
        day = row["solved_at"][:10]
        day_count[day] += 1

    # 스트릭 계산
    from datetime import date, timedelta
    today = date.today()
    streak = 0
    d = today
    while True:
        if d.isoformat() in day_count:
            streak += 1
            d -= timedelta(days=1)
        elif d == today:
            # 오늘 안 풀었으면 어제부터 체크
            d -= timedelta(days=1)
            if d.isoformat() in day_count:
                streak += 1
                d -= timedelta(days=1)
            else:
                break
        else:
            break

    return {
        "heatmap": dict(day_count),
        "streak":  streak,
    }


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
