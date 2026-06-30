# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 프로젝트 개요

백준 문제 아카이브를 기반으로 한 **로컬 웹 문제 풀이 플랫폼**.  
33,000+개의 백준 문제가 `all_problems/problems/{id}/problem.json` 형태로 아카이빙되어 있으며,  
이 중 레벨 6~20(Silver~Platinum)을 선별해 Programmers 스타일의 웹 UI로 제공한다.

자세한 설계는 `PLAN.md` 참고.

---

## 디렉토리 구조

```
all_problems/
  problems/{id}/problem.json     # 원본 아카이브 (수정 금지)

백준/{난이도}/{id}. {제목}/
  README.md                      # BaekjoonHub 자동 생성
  {제목}.py (또는 .cc)           # 풀이 (백준 스타일: 직접 stdin 처리)

프로그래머스/{레벨}/{id}. {제목}/
  README.md
  {제목}.py (또는 .cpp)          # solution() 함수 형태

scripts/                         # 인덱싱 CLI 스크립트
server/                          # FastAPI 백엔드
  routers/
    problems.py                  # 문제 검색/조회 API
    run.py                       # 코드 실행 API
    testcases.py                 # AI 테케 생성/채점 API
frontend/                        # 웹 프론트엔드
  common.css / common.js         # 공통 스타일/유틸
  index.html / index.css         # 문제 목록 페이지
  problem.html / problem.css     # 문제 풀이 페이지
testcases/                       # AI 생성 테케 저장소 (gitignore)
  {id}.json
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

`ANTHROPIC_API_KEY`가 없으면 AI 채점용 테케 생성 기능(`/api/problems/{id}/generate-testcases`)을 사용할 수 없다.

---

## 웹 앱 아키텍처

- **백엔드**: FastAPI + SQLite (`problems.db`)
  - `GET /api/problems` — 검색·태그·레벨 필터 (`q`, `tags`, `levels`, `page`, `size`)
  - `GET /api/problems/{id}` — 문제 상세
  - `GET /api/tags` — 전체 태그 목록
  - `POST /api/run` — 코드 실행 (subprocess, Python 시간제한 × 3)
  - `GET /api/problems/{id}/testcases` — 저장된 AI 테케 조회
  - `POST /api/problems/{id}/generate-testcases` — Claude API로 테케 생성 후 `testcases/{id}.json` 저장
  - `POST /api/problems/{id}/submit` — 저장된 테케로 채점, 통과/실패/TLE/ERROR 반환
- **프론트**: Monaco Editor (CDN), 탭 UI (실행 / 제출)
  - **실행 탭**: 샘플 테케 + 커스텀 테케, 입력 대비 출력 정답 여부 확인
  - **제출 탭**: AI 생성 테케로 채점, 결과만 표시 (정답/오답/TLE/에러)
- **레이아웃**: 좌측 문제 목록/필터 + 우측 문제 설명/코드 에디터 스플릿

---

## 주의사항

- `all_problems/problems/`는 절대 수정하지 않는다 (원본 아카이브).
- `problems.db`, `testcases/`는 gitignore 대상 (빌드 산출물).
- `problem.json`의 `description`, `input`, `output` 필드는 HTML 문자열이므로 프론트에서 `innerHTML`로 렌더링한다.
- 코드 실행(`/api/run`)은 로컬 전용 — 별도 샌드박스 없음.
