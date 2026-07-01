"""
all_problems/problems/ 를 순회해 level 6~20 문제를 SQLite(problems.db)에 인덱싱한다.
최초 1회 실행. 재실행 시 --reset 플래그로 DB 초기화 가능.

사용법:
    python scripts/build_index.py   # 레벨 1~20
    python scripts/build_index.py --min-level 6 --max-level 20 # 레벨 6~20
    python scripts/build_index.py --reset  # DB 초기화
"""

import argparse
import json
import os
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = ROOT / "all_problems" / "problems"
DB_PATH = ROOT / "problems.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS problems (
    id                  INTEGER PRIMARY KEY,
    title               TEXT    NOT NULL,
    level               INTEGER NOT NULL,
    tags                TEXT,       -- JSON 배열 문자열
    description         TEXT,
    input_desc          TEXT,
    output_desc         TEXT,
    samples             TEXT,       -- JSON 배열 문자열
    time_limit          TEXT,       -- "2 초" 형태 원본 문자열
    memory_limit        TEXT,       -- "128 MB" 형태 원본 문자열
    accepted_user_count INTEGER,
    average_tries       REAL,
    solved              INTEGER DEFAULT 0,
    solved_at           TEXT
);

CREATE TABLE IF NOT EXISTS all_tags (
    tag TEXT PRIMARY KEY
);

CREATE INDEX IF NOT EXISTS idx_level ON problems(level);
CREATE INDEX IF NOT EXISTS idx_title ON problems(title);
"""


def create_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()


def reset_db(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        DROP TABLE IF EXISTS problems;
        DROP TABLE IF EXISTS all_tags;
    """)
    conn.commit()
    create_db(conn)
    print("DB 초기화 완료.")


def already_indexed(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COUNT(*) FROM problems").fetchone()
    return row[0]


def build(conn: sqlite3.Connection, min_level: int, max_level: int) -> None:
    if not PROBLEMS_DIR.exists():
        print(f"[ERROR] 경로가 존재하지 않음: {PROBLEMS_DIR}", file=sys.stderr)
        sys.exit(1)

    problem_dirs = [p for p in PROBLEMS_DIR.iterdir() if p.is_dir()]
    total = len(problem_dirs)
    print(f"전체 문제 폴더: {total:,}개 / 레벨 {min_level}~{max_level} 선별 중...")

    inserted = 0
    skipped_level = 0
    skipped_error = 0
    tag_set: set[str] = set()

    start = time.time()

    for i, problem_dir in enumerate(problem_dirs, 1):
        json_path = problem_dir / "problem.json"
        if not json_path.exists():
            skipped_error += 1
            continue

        try:
            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            skipped_error += 1
            continue

        level = data.get("level")
        if not isinstance(level, int) or not (min_level <= level <= max_level):
            skipped_level += 1
            continue

        tags = data.get("tags") or []
        tag_set.update(tags)

        conn.execute(
            """
            INSERT INTO problems
                (id, title, level, tags, description, input_desc, output_desc,
                 samples, time_limit, memory_limit, accepted_user_count, average_tries)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title, level=excluded.level, tags=excluded.tags,
                description=excluded.description, input_desc=excluded.input_desc,
                output_desc=excluded.output_desc, samples=excluded.samples,
                time_limit=excluded.time_limit, memory_limit=excluded.memory_limit,
                accepted_user_count=excluded.accepted_user_count,
                average_tries=excluded.average_tries
            """,
            (
                data.get("id"),
                data.get("title", ""),
                level,
                json.dumps(tags, ensure_ascii=False),
                data.get("description", ""),
                data.get("input", ""),
                data.get("output", ""),
                json.dumps(data.get("samples") or [], ensure_ascii=False),
                data.get("time_limit", ""),
                data.get("memory_limit", ""),
                data.get("accepted_user_count"),
                data.get("average_tries"),
            ),
        )
        inserted += 1

        if i % 1000 == 0:
            conn.commit()
            elapsed = time.time() - start
            print(f"  {i:,}/{total:,} 처리 중... (선별: {inserted:,}개, {elapsed:.1f}초 경과)")

    # 태그 테이블 갱신
    conn.executemany(
        "INSERT OR IGNORE INTO all_tags (tag) VALUES (?)",
        [(t,) for t in sorted(tag_set)],
    )
    conn.commit()

    elapsed = time.time() - start
    print(f"\n완료 ({elapsed:.1f}초)")
    print(f"  선별 삽입: {inserted:,}개")
    print(f"  레벨 범위 외: {skipped_level:,}개")
    print(f"  파싱 오류: {skipped_error:,}개")
    print(f"  태그 종류: {len(tag_set)}개")
    print(f"  DB 경로: {DB_PATH}")


def main() -> None:
    parser = argparse.ArgumentParser(description="백준 문제 SQLite 인덱서")
    parser.add_argument("--min-level", type=int, default=6)
    parser.add_argument("--max-level", type=int, default=20)
    parser.add_argument("--reset", action="store_true", help="기존 DB 초기화 후 재인덱싱")
    args = parser.parse_args()

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")

    create_db(conn)

    if args.reset:
        reset_db(conn)
    else:
        count = already_indexed(conn)
        if count > 0:
            print(f"이미 {count:,}개 인덱싱됨. 재실행하려면 --reset 플래그를 사용하세요.")
            conn.close()
            return

    build(conn, args.min_level, args.max_level)
    conn.close()


if __name__ == "__main__":
    main()
