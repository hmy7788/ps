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


TIER_NAMES = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ruby"]
ROMAN = ["V", "IV", "III", "II", "I"]
MAX_LEVEL = 30

# 문제 1개 풀 때 얻는 경험치: 10 * (문제레벨 ^ 1.5)
EXP_BASE_MULT = 10
EXP_LEVEL_POW = 1.5
# 내 레벨보다 5 이상 낮은 문제는 경험치 10%만 인정 (쉬운 문제 우려먹기 방지)
PENALTY_GAP = 5
PENALTY_MULT = 0.1
# 레벨 L 도달에 필요한 누적 경험치: 30 * (L ^ 2.5)
LEVEL_THRESHOLD_MULT = 30
LEVEL_THRESHOLD_POW = 2.5


def level_label(level: int) -> str:
    if level <= 0:
        return "Unrated"
    level = min(level, MAX_LEVEL)
    tier_idx = (level - 1) // 5
    sub_idx = (level - 1) % 5
    return f"{TIER_NAMES[tier_idx]} {ROMAN[sub_idx]}"


def level_class(level: int) -> str:
    if level <= 0:
        return "unrated"
    tier_idx = min((level - 1) // 5, len(TIER_NAMES) - 1)
    return TIER_NAMES[tier_idx].lower()


def _exp_for_problem(problem_level: int, user_level: int) -> float:
    base = EXP_BASE_MULT * (problem_level ** EXP_LEVEL_POW)
    if problem_level <= user_level - PENALTY_GAP:
        base *= PENALTY_MULT
    return base


def _threshold(level: int) -> float:
    if level <= 0:
        return 0.0
    return LEVEL_THRESHOLD_MULT * (level ** LEVEL_THRESHOLD_POW)


def get_user_level(conn: sqlite3.Connection) -> dict:
    """solved.ac 스타일 유저 레벨: 푼 문제 난이도를 경험치로 환산해 누적."""
    rows = conn.execute(
        """SELECT id, level, solved_at FROM problems
           WHERE solved = 1
           ORDER BY (solved_at IS NULL), solved_at ASC, id ASC"""
    ).fetchall()

    level = 0
    exp = 0.0
    level_ups: list[dict] = []

    for row in rows:
        exp += _exp_for_problem(row["level"], level)
        while level < MAX_LEVEL and exp >= _threshold(level + 1):
            level += 1
            level_ups.append({
                "level": level,
                "label": level_label(level),
                "at": row["solved_at"],
                "problem_id": row["id"],
            })

    cur_threshold = _threshold(level)
    next_threshold = _threshold(level + 1) if level < MAX_LEVEL else None
    if next_threshold is not None:
        progress = (exp - cur_threshold) / (next_threshold - cur_threshold)
    else:
        progress = 1.0

    return {
        "level": level,
        "label": level_label(level),
        "class": level_class(level),
        "exp": round(exp, 1),
        "cur_threshold": round(cur_threshold, 1),
        "next_threshold": round(next_threshold, 1) if next_threshold is not None else None,
        "progress_pct": round(max(0.0, min(1.0, progress)) * 100, 1),
        "level_up_history": list(reversed(level_ups[-20:])),
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
