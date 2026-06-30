# 백준 아카이브 → Programmers 스타일 웹 문제 풀이 시스템

## 배경

`all_problems/problems/`에 33,000+개의 백준 문제가 `problem.json` 형태로 아카이빙되어 있다.
이를 기반으로 **로컬호스트 웹 앱**을 만들어 Programmers처럼 문제를 검색하고 코드를 작성할 수 있는 환경을 구성한다.

**원본 `all_problems/problems/`는 건드리지 않는다.**

---

## 목표 기능

1. **문제 검색** — 제목/번호로 검색 ✅
2. **태그(유형) 필터링** — 체크박스로 복수 선택 ✅
3. **레벨 필터링** — Silver(6~10) / Gold(11~15) / Platinum(16~20) 체크 ✅
4. **태그 + 레벨 복합 필터링** ✅
5. **문제 + 코드 에디터 스플릿 뷰** — Programmers 스타일 ✅
6. **샘플 테케 실행** — 정답/오답 확인 ✅
7. **AI 채점 테케 생성/제출** — Claude API로 테케 생성, 채점 ✅

---

## 레벨 기준

| 레벨  | 등급      |
|-------|-----------|
| 6–10  | Silver ✅  |
| 11–15 | Gold ✅    |
| 16–20 | Platinum ✅|

---

## 기술 스택

| 영역 | 선택 | 이유 |
|------|------|------|
| 백엔드 | FastAPI (Python) | 기존 스크립트 재활용, 빠른 개발 |
| DB | SQLite | 인덱싱 후 빠른 검색/필터 쿼리 |
| 프론트 | 단일 HTML + Vanilla JS | 별도 빌드 불필요 |
| 코드 에디터 | Monaco Editor (CDN) | VS Code 엔진, Programmers 느낌 |
| AI 테케 생성 | Claude API (`claude-sonnet-4-6`) | 문제 분석 후 테케 자동 생성 |

---

## 레이아웃

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 검색창        [태그 필터 ▼]    [레벨 필터 ▼]            │
├────────────────────────┬────────────────────────────────────┤
│ 문제 목록              │  문제 설명 (HTML 렌더링)            │
│ ──────────────────     │  ─────────────────────────────────│
│ #1234 두 수의 합  G5   │  입력: ...  출력: ...              │
│ #5678 DFS 탐색   S3    ├────────────────────────────────────┤
│ ...                    │  def solution():                   │
│                        │      pass   ← Monaco Editor       │
│                        ├────────────────────────────────────┤
│                        │  [실행] [제출]                     │
│                        │  샘플 테케 / AI 채점 테케          │
└────────────────────────┴────────────────────────────────────┘
```

---

## 디렉토리 구조

```
ps/
├── all_problems/
│   └── problems/               # 원본 아카이브 (건드리지 않음)
├── scripts/
│   └── build_index.py          # SQLite 인덱스 생성 (최초 1회) ✅
├── server/
│   ├── main.py                 # FastAPI 앱 진입점 ✅
│   ├── db.py                   # SQLite 연결/쿼리 ✅
│   ├── models.py               # Pydantic 모델 ✅
│   ├── utils.py                # 시간제한 파싱 등 ✅
│   └── routers/
│       ├── problems.py         # 검색/필터 API ✅
│       ├── run.py              # 코드 실행 API ✅
│       └── testcases.py        # AI 테케 생성/채점 API ✅
├── frontend/
│   ├── common.css / common.js  # 공통 (태그 한글화, 레벨 배지 등) ✅
│   ├── index.html / index.css  # 문제 목록 페이지 ✅
│   └── problem.html / problem.css  # 문제 풀이 페이지 ✅
├── testcases/                  # AI 생성 테케 저장 (gitignore)
│   └── {id}.json
├── problems.db                 # SQLite 인덱스 (gitignore)
├── .env                        # ANTHROPIC_API_KEY (gitignore)
├── PLAN.md
└── CLAUDE.md
```

---

## API 목록

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/problems` | 목록 조회 (검색·필터 쿼리 파라미터) |
| GET | `/api/problems/{id}` | 문제 상세 |
| GET | `/api/tags` | 전체 태그 목록 |
| POST | `/api/run` | 코드 실행 (subprocess) |
| GET | `/api/problems/{id}/testcases` | 저장된 AI 테케 조회 |
| POST | `/api/problems/{id}/generate-testcases` | Claude API로 테케 생성 |
| POST | `/api/problems/{id}/submit` | AI 테케로 채점 |

---

## 테스트케이스 시스템

### 실행 탭 (샘플 테케)
- 문제 샘플 입출력 자동 로드
- 커스텀 테케 추가 가능
- 코드 실행 후 기대 출력과 비교 → ✅/❌

### 제출 탭 (AI 채점 테케)
- "채점용 테케 만들기" → Claude API로 10개 생성, `testcases/{id}.json` 저장
- 이후 "제출" → 저장된 테케로 채점
- 결과: 통과/오답(WA)/시간초과(TLE)/에러(ERROR)
- 문제당 API 비용: ~$0.025 (약 35원)

---

## 실행 방법

```bash
# 최초 설정
pip install -r requirements.txt
python scripts/build_index.py      # DB 인덱싱 (시간 걸림)

# .env 파일 생성
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# 서버 실행
uvicorn server.main:app --reload --port 8000
```

---

## 미결 사항 / 향후 계획

| 항목 | 상태 | 비고 |
|------|------|------|
| C++ 코드 실행 지원 | 미구현 | 현재 Python만 |
| 풀이 저장/불러오기 | 미구현 | localStorage 또는 파일 저장 |
| 코드 실행 보안 | subprocess + timeout | 샌드박스 없음 (로컬 전용) |
| 태그 필터 정렬 | 구현 완료 | 코딩테스트 중요도 순 |
