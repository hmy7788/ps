# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 프로젝트 개요

백준 문제 아카이브를 기반으로 한 **로컬 웹 문제 풀이 플랫폼**.  
33,000+개의 백준 문제가 `all_problems/problems/{id}/problem.json` 형태로 아카이빙되어 있으며,  
이 중 레벨 6~20(Silver~Platinum)을 선별해 Programmers 스타일의 웹 UI로 제공한다.

자세한 설계는 `docs/PLAN.md` 참고. 세션별 작업 기록은 `docs/HANDOFF.md`.

---

## 디렉토리 구조

```
all_problems/
  problems/{id}/problem.json     # 원본 아카이브 (수정 금지)

백준/{난이도}/{id}. {제목}/
  README.md                      # BaekjoonHub 자동 생성 또는 save-solution API가 생성
  {제목}.py (또는 .cc)           # 풀이 (백준 스타일: 직접 stdin 처리)

프로그래머스/{레벨}/{id}. {제목}/
  README.md
  {제목}.py (또는 .cpp)          # solution() 함수 형태

scripts/                         # 인덱싱 CLI 스크립트 (build_index.py)
server/                          # FastAPI 백엔드
  main.py                        # 앱 진입점 + 하트비트/워치독(서버 생명주기)
  db.py                          # SQLite 연결/쿼리/마이그레이션/유저 레벨 계산
  models.py                      # Pydantic 모델
  utils.py                       # 시간제한 파싱, run_one, strip_html 등 공유 유틸
  routers/
    problems.py                  # 문제 검색/조회/필터/통계 API
    run.py                       # 코드 실행 API
    testcases.py                 # AI 테케 생성/채점 API
    solutions.py                 # 백준 폴더 저장/조회 API
    counterexample.py            # testcase.ac 연동 + AI 반례 탐색 폴백
    drafts.py                    # 임시저장(드래프트) API
frontend/                        # 웹 프론트엔드 (순수 JS + Monaco Editor CDN)
  common.css / common.js         # 공통 스타일/유틸
  index.html / index.css         # 문제 목록 페이지 (검색/필터/즐겨찾기/풀고있는 문제)
  problem.html / problem.css     # 문제 풀이 페이지 (실행/제출 탭)
  stats.html / stats.css         # 통계 페이지 (히트맵·스트릭·유저 레벨·태그/난이도 분포)
docs/                            # 프로젝트 문서 (기능별 설계/구현 기록)
testcases/                       # AI 생성 테케 + AI 반례 폴백용 정답코드 캐시 (gitignore)
  {id}.json                      # generate-testcases 결과
  {id}_ref.json                  # AI 반례 폴백용 정답코드+입력생성기 캐시
drafts/                          # 문제별 임시저장 코드 (gitignore, 완전 로컬 전용)
reports/                         # 회귀 테스트 등 애드혹 리포트 (gitignore)
```

---

## problem.json 스키마

```json
{
  "id": 1000,
  "title": "A+B",
  "level": 1,
  "tags": ["implementation", "math"],
  "description": "<p>HTML...</p>",
  "input": "<p>HTML...</p>",
  "output": "<p>HTML...</p>",
  "samples": [{"input": "1 2\n", "output": "3\n"}],
  "time_limit": "2 초",
  "memory_limit": "128 MB",
  "accepted_user_count": 370601,
  "average_tries": 2.6
}
```

레벨 기준: 1–5 Bronze / **6–10 Silver** / **11–15 Gold** / **16–20 Platinum** / 21–25 Diamond / 26–30 Ruby

---

## 풀이 스타일 규칙

| 위치 | 스타일 |
|------|--------|
| `백준/` | `input()` 직접 사용, 함수 없이 절차형 |
| `프로그래머스/` | `def solution(...): return ...` 형태 |

---

## 주요 명령어

```bash
# SQLite 인덱스 생성 (최초 1회, 시간 소요)
python scripts/build_index.py

# 웹 서버 실행
uvicorn server.main:app --reload --port 8000
```

---

## 환경 설정

`.env` 파일을 프로젝트 루트에 생성:

```
ANTHROPIC_API_KEY=sk-ant-...
```

`ANTHROPIC_API_KEY`가 없으면 AI 채점용 테케 생성(`/api/problems/{id}/generate-testcases`)과 AI 반례 탐색 폴백(`/api/problems/{id}/find-counterexample`)을 사용할 수 없다.

---

## 웹 앱 아키텍처

- **백엔드**: FastAPI + SQLite (`problems.db`)
  - `GET /api/problems` — 검색·태그·레벨·즐겨찾기·풀이여부·풀고있는문제(드래프트) 필터 (`q`, `tags`, `levels`, `page`, `size`, `solved`, `favorite`, `in_progress`)
  - `GET /api/problems/{id}` — 문제 상세
  - `GET /api/tags` — 전체 태그 목록
  - `GET /api/stats` — 총 풀이수/난이도별·태그별 분포/최근 풀이
  - `GET /api/stats/heatmap` — 풀이 히트맵 + 연속 스트릭
  - `GET /api/stats/level` — solved.ac 스타일 유저 레벨/경험치/레벨업 히스토리 (`docs/user-level-system.md` 참고)
  - `POST /api/problems/{id}/favorite` — 즐겨찾기 토글
  - `GET/POST/DELETE /api/problems/{id}/draft` — 임시저장(드래프트) 조회/저장/삭제
  - `POST /api/run` — 코드 실행 (subprocess, Python 시간제한 × 3)
  - `GET /api/problems/{id}/testcases` — 저장된 AI 테케 조회
  - `POST /api/problems/{id}/generate-testcases` — Claude API로 테케 생성 후 `testcases/{id}.json` 저장
  - `POST /api/problems/{id}/submit` — 저장된 테케로 채점, 통과/실패/TLE/ERROR 반환
  - `POST /api/problems/{id}/find-counterexample` — testcase.ac 연동, 없으면 AI가 정답코드+입력생성기를 만들어 반례 탐색(폴백)
  - `GET /api/problems/{id}/solutions`, `/last-solution`, `/solutions/{filename}` — 백준 폴더에 저장된 기존 풀이 조회
  - `POST /api/problems/{id}/save-solution` — 코드를 백준 폴더에 파일로 저장 + DB `solved` 갱신
  - `POST /api/heartbeat`, `POST /api/heartbeat/leaving` — 서버 생명주기(아래 참고), 프론트 `common.js`가 자동 호출
- **서버 생명주기**: 브라우저 탭이 열려있는 동안만 로컬 서버가 살아있도록 하는 워치독(`server/main.py`)
  - 프론트가 주기적으로 `POST /api/heartbeat` 전송, 탭이 실제로 닫힐 때(`pagehide`)는 `navigator.sendBeacon`으로 `/api/heartbeat/leaving` 전송
  - "leaving" 신호 후 `_LEAVING_GRACE`(8초) 내 새 하트비트가 없으면 진짜 종료로 판단해 `os._exit(0)`
  - leaving 신호 자체가 안 온 경우(강제종료 등) 대비, 하트비트가 `_SAFETY_TIMEOUT`(30분) 이상 끊기면 최종 안전장치로 종료
- **프론트**: Monaco Editor (CDN), 탭 UI (실행 / 제출)
  - **실행 탭**: 샘플 테케 + 커스텀 테케, 입력 대비 출력 정답 여부 확인
  - **제출 탭**: AI 생성 테케로 채점, 결과만 표시 (정답/오답/TLE/에러)
  - **목록 페이지**: 즐겨찾기·풀이여부·풀고있는 문제(드래프트 존재) 필터, 각 필터는 URL 쿼리 파라미터와 동기화. 헤더에 유저 레벨 미니 배지 상시 노출
  - **통계 페이지**: 유저 레벨 배지+진행률 바+레벨업 히스토리, 히트맵/스트릭, 난이도·태그 분포, 최근 풀이
- **레이아웃**: 좌측 문제 목록/필터 + 우측 문제 설명/코드 에디터 스플릿

---

## 주의사항

- `all_problems/problems/`는 절대 수정하지 않는다 (원본 아카이브).
- `problems.db`, `drafts/`, `reports/`, `testcases/`는 gitignore 대상 (빌드 산출물/로컬 캐시).
- `problem.json`의 `description`, `input`, `output` 필드는 HTML 문자열이므로 프론트에서 `innerHTML`로 렌더링한다.
- 코드 실행(`/api/run`)과 AI 반례 폴백의 입력 생성기 실행은 전부 로컬 subprocess 기반 — 별도 샌드박스 없음, 로컬 전용 도구라는 전제.
- 프로젝트 진행 상황/의사결정/트러블슈팅은 `docs/`에 기능별로 정리한다 (예: `docs/user-level-system.md`).
