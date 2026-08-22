# ps

This is an auto push repository for Baekjoon Online Judge created with [BaekjoonHub](https://github.com/BaekjoonHub/BaekjoonHub).

## 이 저장소는 뭔가요

백준/프로그래머스 풀이 아카이브 + **로컬 전용 웹 문제 풀이 플랫폼**입니다.

- `백준/`, `프로그래머스/` — 실제로 푼 문제들의 풀이 코드 (BaekjoonHub 자동 커밋 또는 아래 웹 앱의 "백준에 저장" 기능으로 생성)
- `all_problems/problems/` — 33,000+개 백준 문제 원본 아카이브 (수정 금지, 웹 앱이 읽기 전용으로 참조)
- `server/`, `frontend/` — Programmers 스타일로 문제를 검색·풀이·채점할 수 있는 FastAPI + Vanilla JS 웹 앱

## 빠르게 시작하기

```bash
pip install -r requirements.txt
pip install anthropic httpx python-dotenv   # requirements.txt에 누락되어 있음

python scripts/build_index.py               # SQLite 인덱스 생성 (최초 1회)
uvicorn server.main:app --reload --port 8000
```

`http://localhost:8000` 접속. 브라우저 탭을 닫으면 서버도 자동으로 같이 종료됩니다.

## 웹 앱 주요 기능

- 문제 검색/태그/레벨 필터, 즐겨찾기, 풀고 있는 문제(임시저장) 필터
- Monaco 에디터로 코드 작성 → 샘플 테케 실행, AI 생성 테케로 채점
- testcase.ac 연동 + AI 반례 탐색 폴백 (틀린 코드의 반례 자동 탐색)
- 전체 통과 시 "백준에 저장" 버튼으로 `백준/` 폴더에 자동 저장
- 통계 페이지 — 풀이 히트맵/연속 스트릭, 난이도·태그 분포, solved.ac 스타일 유저 레벨(경험치·레벨업 히스토리)

## 더 자세한 내용

| 문서 | 내용 |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | 프로젝트 규칙, 디렉토리 구조, API 목록, 아키텍처 |
| [`PLAN.md`](PLAN.md) | 원래 설계 문서, 목표 기능, 미결 사항 |
| [`HANDOFF.md`](HANDOFF.md) | 세션별 작업 기록, 알려진 잡음/함정, 다음에 할 일 |
| [`docs/`](docs/) | 기능별 상세 설계·구현·트러블슈팅 (예: [`docs/user-level-system.md`](docs/user-level-system.md)) |
