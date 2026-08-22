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
8. **AI 반례 탐색 폴백** — testcase.ac에 등록 안 된 문제는 AI가 정답코드+입력생성기 생성 후 스트레스 테스트 ✅
9. **풀이 완료 시 백준 폴더 자동 저장** — `solved` DB 갱신 + 파일 생성 ✅
10. **즐겨찾기 / 임시저장(드래프트)** — 문제 즐겨찾기 토글, 미완성 코드 자동 저장·복원 ✅
11. **통계 페이지** — 풀이 히트맵/연속 스트릭, 난이도·태그 분포, solved.ac 스타일 유저 레벨(경험치·레벨업 히스토리) ✅
12. **풀고 있는 문제 필터링** — 드래프트가 남아있는 문제만 보기 ✅
13. **로컬 서버 자동 종료(그레이스풀 셧다운)** — 브라우저 탭 종료 감지 시 서버도 함께 종료 ✅

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
│   └── problems/                   # 원본 아카이브 (건드리지 않음)
├── scripts/
│   └── build_index.py              # SQLite 인덱스 생성 (최초 1회) ✅
├── server/
│   ├── main.py                     # FastAPI 앱 진입점 + 하트비트/워치독 ✅
│   ├── db.py                       # SQLite 연결/쿼리/마이그레이션/유저 레벨 계산 ✅
│   ├── models.py                   # Pydantic 모델 ✅
│   ├── utils.py                    # 시간제한 파싱, run_one, strip_html ✅
│   └── routers/
│       ├── problems.py             # 검색/필터/통계 API ✅
│       ├── run.py                  # 코드 실행 API ✅
│       ├── testcases.py            # AI 테케 생성/채점 API ✅
│       ├── solutions.py            # 백준 폴더 저장/조회 API ✅
│       ├── counterexample.py       # testcase.ac 연동 + AI 반례 폴백 ✅
│       └── drafts.py               # 임시저장(드래프트) API ✅
├── frontend/
│   ├── common.css, common.js       # 공통 (태그 한글화, 레벨 배지, 하트비트 전송 등) ✅
│   ├── index.html, index.css       # 문제 목록 페이지 (검색/필터/즐겨찾기/드래프트) ✅
│   ├── problem.html, problem.css   # 문제 풀이 페이지 (실행/제출 탭, 반례 탐색) ✅
│   └── stats.html, stats.css       # 통계 페이지 (히트맵/레벨/분포) ✅
├── docs/                           # 프로젝트 문서
│   ├── PLAN.md                     # 이 문서 (원래 설계)
│   ├── HANDOFF.md                  # 세션 간 인수인계 문서
│   └── ...                         # 기능별 설계/구현/트러블슈팅 기록 ✅
├── testcases/                      # AI 생성 테케 + AI 반례용 정답코드 캐시 (gitignore)
│   ├── {id}.json
│   └── {id}_ref.json
├── drafts/                         # 문제별 임시저장 코드 (gitignore)
├── reports/                        # 회귀 테스트 등 애드혹 리포트 (gitignore)
├── problems.db                     # SQLite 인덱스 (gitignore)
├── .env                            # ANTHROPIC_API_KEY (gitignore)
└── CLAUDE.md
```

---

## API 목록

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/problems` | 목록 조회 (검색·태그·레벨·즐겨찾기·풀이여부·풀고있는문제 필터) |
| GET | `/api/problems/{id}` | 문제 상세 |
| GET | `/api/tags` | 전체 태그 목록 |
| GET | `/api/stats` | 총 풀이수/난이도별·태그별 분포/최근 풀이 |
| GET | `/api/stats/heatmap` | 풀이 히트맵 + 연속 스트릭 |
| GET | `/api/stats/level` | 유저 레벨/경험치/레벨업 히스토리 (`docs/user-level-system.md`) |
| POST | `/api/problems/{id}/favorite` | 즐겨찾기 토글 |
| GET/POST/DELETE | `/api/problems/{id}/draft` | 임시저장(드래프트) 조회/저장/삭제 |
| POST | `/api/run` | 코드 실행 (subprocess) |
| GET | `/api/problems/{id}/testcases` | 저장된 AI 테케 조회 |
| POST | `/api/problems/{id}/generate-testcases` | Claude API로 테케 생성 |
| POST | `/api/problems/{id}/submit` | AI 테케로 채점 |
| POST | `/api/problems/{id}/find-counterexample` | testcase.ac 연동, 없으면 AI 반례 탐색 폴백 |
| GET | `/api/problems/{id}/solutions`, `/last-solution`, `/solutions/{filename}` | 백준 폴더에 저장된 풀이 조회 |
| POST | `/api/problems/{id}/save-solution` | 코드를 백준 폴더에 저장 + `solved` 갱신 |
| POST | `/api/heartbeat`, `/api/heartbeat/leaving` | 서버 생명주기 신호 (브라우저 탭 종료 시 서버 자동 종료) |

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
| 풀이 저장/불러오기 | 구현 완료 | DB `solved` + 백준 폴더 파일 저장(`save-solution`), 임시저장은 `drafts/`로 별도 |
| 코드 실행 보안 | subprocess + timeout | 샌드박스 없음 (로컬 전용) |
| 태그 필터 정렬 | 구현 완료 | 코딩테스트 중요도 순 |
| 풀이 완료 시 백준 폴더 자동 저장 | 구현 완료 | 아래 참고 |
| 즐겨찾기 / 드래프트 / 통계 / 유저 레벨 / 그레이스풀 셧다운 | 구현 완료 | `HANDOFF.md`에 세션별 구현 기록 |
| 자동화 테스트(`tests/`) | 미구현 | 아직 빈 폴더, 회귀 검증은 `harness` 브랜치의 `scripts/regression_test.py`가 main에 미병합 상태로 존재 |
| `testcases/` 완전한 gitignore화 | 구현 완료 | `.gitignore`에 `testcases/` 추가 + 기존 커밋 파일 `git rm --cached` (2026-08-22) |
| `requirements.txt` 누락 패키지 | 구현 완료 | `anthropic`/`httpx`/`python-dotenv` 추가 (2026-08-22) |

---

## 풀이 완료 시 백준 폴더 자동 저장

### 흐름
```
제출 → 전체 통과 → "백준에 저장" 버튼 노출 → 클릭 → 파일 생성
```

### 생성 파일
```
백준/{난이도}/{id}. {title}/
  README.md       # BaekjoonHub 포맷 모방
  {title}.py      # 에디터 코드 그대로 저장
```

난이도 매핑: 1–5 Bronze / 6–10 Silver / 11–15 Gold / 16–20 Platinum / 21–25 Diamond / 26–30 Ruby

### DB solved 체킹

`problems` 테이블에 컬럼 추가:
```sql
ALTER TABLE problems ADD COLUMN solved INTEGER DEFAULT 0;
ALTER TABLE problems ADD COLUMN solved_at TEXT;
```

- 저장 시: `UPDATE problems SET solved=1, solved_at=<ISO datetime> WHERE id=?`
- `build_index.py`는 `INSERT OR IGNORE` 방식이므로 재실행해도 solved 값 유지됨
- 문제 목록 API(`GET /api/problems`)에서 `solved` 필드 포함해 반환 → 목록에 ✅ 표시

### 추가 API
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/problems/{id}/save-solution` | 코드 받아 백준 폴더에 파일 저장 + DB solved 업데이트 |
