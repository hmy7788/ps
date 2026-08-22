# HANDOFF.md

다른 컴퓨터에서 이어서 개발하기 위한 인수인계 문서. 2026-08-22 기준 최신 상태 (섹션 2-1~2-4는 2026-07-26 세션, 2-5부터는 이후 세션).
`../CLAUDE.md`(프로젝트 규칙, 루트)와 `PLAN.md`(원래 설계 문서, 같은 `docs/` 폴더)는 그대로 유효하며, 이 문서는 "지금까지 뭘 했고 다음에 뭘 할지"에 집중한다.

*(2026-08-22: 이 문서와 `PLAN.md`를 루트에서 `docs/`로 이동함. 그 이전 세션 기록에 나오는 "루트의 PLAN.md/HANDOFF.md" 언급은 지금은 `docs/PLAN.md`, `docs/HANDOFF.md`를 가리킨다.)*

---

## 1. 새 컴퓨터에서 시작하는 법

```bash
git clone https://github.com/hmy7788/ps.git
cd ps
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt   # anthropic/httpx/python-dotenv 전부 포함됨 (2026-08-22에 수정)

# SQLite 인덱스 생성 (최초 1회, 시간 소요 — all_problems/ 스캔)
python scripts/build_index.py

# .env 파일 생성 (AI 테케 생성 기능 쓰려면 필수)
echo ANTHROPIC_API_KEY=sk-ant-... > .env

# 서버 실행
uvicorn server.main:app --reload --port 8000
```

`problems.db`, `testcases/*.json`(AI 생성분), `drafts/`는 전부 gitignore 대상이라 새 컴퓨터에는 없다.
- `problems.db`는 `build_index.py`로 재생성.
- `testcases/`, `drafts/`는 로컬 캐시라 없어도 기능은 동작하고, 쓰면서 다시 쌓인다.

---

## 2. 이번 세션에서 한 일 (커밋 순서대로)

### 2-1. 즐겨찾기(⭐) 기능
- `problems` 테이블에 `favorite INTEGER DEFAULT 0` 컬럼 추가 (`server/db.py`의 `_migrate()` — 기존 `solved`/`solved_at` 마이그레이션과 동일 패턴, `PRAGMA table_info` 체크 후 없으면 `ALTER TABLE`).
- `POST /api/problems/{id}/favorite` — 토글 엔드포인트 (`server/db.py::toggle_favorite`, `server/routers/problems.py`).
- `GET /api/problems?favorite=1` — 즐겨찾기만 필터링.
- 프론트: 목록 페이지(`index.html`) 카드에 별 아이콘, "⭐ 즐겨찾기만" 필터 버튼(pill 스타일). 문제 상세 페이지(`problem.html`) 헤더에도 별 아이콘.
- 별 클릭 시 bounce+glow 애니메이션 (`@keyframes fav-pop`, `index.css`/`problem.css`에 **중복** 정의되어 있음 — 8번 CSS 정리 항목 참고).

### 2-2. 임시 코드 자동저장 (드래프트)
- **명시적 제약**: 안 풀린/미완성 코드도 저장해야 하고, `백준/` 폴더에는 절대 쓰지 않는다. 완전히 별도 메커니즘.
- `server/routers/drafts.py` (신규 파일) — `drafts/{problem_id}.json`에 `{code, updated_at}` 저장. `testcases/{id}.json` 캐시 패턴을 그대로 재사용.
  - `GET /api/problems/{id}/draft`
  - `POST /api/problems/{id}/draft`
  - `DELETE /api/problems/{id}/draft`
- 프론트(`problem.html`): Monaco 에디터 `onDidChangeModelContent`에 1초 디바운스로 `scheduleDraftSave()` 연결. 문제 진입 시 드래프트 있으면 자동 복원 + "되돌리기" 링크로 삭제 가능. **"백준에 저장" 버튼으로 실제 저장(`saveSolution()`) 성공하면 드래프트는 자동 삭제됨.**
- `drafts/`는 `.gitignore`에 추가되어 완전히 로컬 전용.

### 2-3. testcase.ac 미등록 문제용 AI 반례 탐색 폴백
(이건 이전 세션 작업이 이번에 main으로 merge된 것 — 새로 만든 게 아님)
- testcase.ac에 케이스가 없는 문제는 AI가 정답 코드 + 입력 생성기를 작성해서 반례를 탐색.
- 정답 코드는 생성 직후 샘플로 자체 검증 후 실패하면 폴백 자체를 포기 (틀린 코드를 정답으로 오인 방지).
- 입력 생성기는 subprocess로 격리 실행 (AI가 무한루프/크래시 코드를 생성해도 서버는 안 죽음).
- 정답 코드/생성기는 `testcases/{id}_ref.json`으로 캐싱해서 문제당 API 호출 1회로 제한.
- `server/routers/counterexample.py`, `server/utils.py`(`run_one`/`strip_html` 공유 유틸로 분리).

### 2-4. 브랜치 정리 및 main 병합
세 개 feature 브랜치를 검토 후 main에 병합, push 완료:

| 브랜치 | 상태 |
|---|---|
| `feature/favorites-drafts` | main에 merge 완료 (conflict 없음) |
| `feature/ai-counterexample-fallback` | main에 merge 완료 (`problem.css`/`problem.html`에서 auto-merge, conflict 없음) |
| `feature/testcase-ac-integration` | 이미 main에 완전히 반영되어 있었음 (고유 커밋 0개, 병합할 것 없었음) |

세 브랜치 모두 origin에 아직 남아있음 (삭제 요청받지 않아서 그대로 둠). 필요 없으면 `git branch -d`/`git push origin --delete`로 정리 가능.

### 2-5. 그레이스풀 서버 셧다운 (브랜치 `fix/graceful-server-shutdown`, merge 완료)
- **문제**: 조금만 안 써도(브라우저 탭이 백그라운드로 밀려도) localhost 서버가 꺼짐.
- **원인**: 기존엔 하트비트가 오래 끊기면 워치독이 서버를 죽이는 단순한 타임아웃 방식이었는데, Chrome이 백그라운드 탭의 `setInterval`을 강하게 스로틀링해서 "탭은 열려있는데 하트비트만 안 오는" 상황이 실제 탭 종료로 오인됨.
- **해결**: "탭이 실제로 사라질 때"(`pagehide`)만 명시적으로 `navigator.sendBeacon('/api/heartbeat/leaving')`으로 신호를 보내고, 서버는 이 신호 후 `_LEAVING_GRACE`(8초) 안에 새 하트비트가 없어야만 종료. leaving 신호 자체가 안 오는 극단적 상황(강제종료 등) 대비 `_SAFETY_TIMEOUT`(30분)을 최후 안전장치로 유지.
- `server/main.py`, `frontend/common.js` 수정. curl 스크립트 + 실제 Chrome 탭으로 검증 완료.

### 2-6. "풀고 있는 문제만" 필터 (브랜치 `feat/in-progress-filter`, merge 완료)
- 드래프트 파일(`drafts/{id}.json`)이 남아있는 문제만 목록에서 필터링.
- `server/routers/drafts.py`에 `list_draft_ids()` 추가, `server/db.py::get_problems()`에 `in_progress_only`/`draft_ids` 파라미터 추가, `ProblemSummary.in_progress` 필드 추가.
- 프론트: 기존 즐겨찾기 필터와 동일한 패턴으로 버튼/뱃지 추가.

### 2-7. 유저 레벨 시스템 (브랜치 `feat/user-level-system`, merge 완료)
- solved.ac처럼 푼 문제 난이도를 경험치로 환산해 누적, 1~30 레벨/티어로 표시.
- `GET /api/stats/level` 신규, `/stats` 페이지에 레벨 배지+진행률 바+레벨업 히스토리 추가.
- 설계·공식·트러블슈팅은 `docs/user-level-system.md`에 상세 기록. (`/stats.html` 아닌 `/stats`가 정식 라우트인 점, 프론트 수정 후 하드리프레시 필요했던 점 등)

### 2-8. 브랜치 정리 (2026-08-22)
- 이미 main에 merge된 로컬 브랜치 `feat/in-progress-filter`, `feat/user-level-system`, `fix/graceful-server-shutdown` 삭제 완료.
- origin의 `feature/ai-counterexample-fallback`, `feature/favorites-drafts`, `feature/testcase-ac-integration`도 전부 main에 이미 병합된 상태(merge-base 확인 결과 unique 커밋 0개) — 원격 삭제는 시도했으나 auto-mode 권한 정책에 막혀 보류 중. 필요하면 사용자가 직접:
  ```bash
  git push origin --delete feature/ai-counterexample-fallback feature/favorites-drafts feature/testcase-ac-integration
  ```
- **`harness` 브랜치는 의도적으로 정리 대상에서 제외**. `main`과 58커밋 갈라져 있고, 자체적으로 6개의 고유 커밋에 상당한 미병합 작업이 있음 (아래 3번 섹션 참고). 사용자에게 병합 방식(전체 merge / cherry-pick / 보류)을 물었고 **"일단 보류"**로 확정 — 다음에 다시 논의 필요.

### 2-9. 하우스키핑 3종 (브랜치 `chore/housekeeping-fixes`)
문서에 계속 "알려진 이슈"로만 적혀 있던 것들을 실제로 고침:
1. **`requirements.txt` 누락 패키지 추가** — `anthropic==0.120.0`, `httpx==0.28.1`, `python-dotenv==1.2.2` 추가 (현재 venv에 설치된 버전 그대로 고정). 이 파일은 UTF-16(BOM) 인코딩인데, pip이 BOM을 보고 자동으로 인코딩을 감지해서 읽기 때문에 문제없이 동작함 — 굳이 UTF-8로 바꿀 필요는 없어서 그대로 유지.
2. **`testcases/` gitignore 정리** — `.gitignore`에 `testcases/` 추가, 이미 커밋돼 있던 7개 파일(`testcases/1010.json` 등)은 `git rm --cached`로 추적만 해제 (디스크의 실제 파일은 그대로 남아있음, 삭제 아님).
3. **`index.html` 헤더에 유저 레벨 미니 배지 추가** — `GET /api/stats/level`을 새로 fetch해서 "Lv.11 Gold V" 같은 pill을 로고 옆에 표시. 기존 `.stats-link`와 같은 톤의 스타일, 티어별 색상은 `stats.html`의 `.level-badge`와 동일한 CSS 변수(`--gold` 등) 재사용.

Chrome으로 실제 렌더링 확인 완료 (하드리프레시 후 정상 표시).

---

## 3. 현재 브랜치/커밋 상태

- `main`, `harness` 두 개 로컬 브랜치만 존재. `main`은 origin과 동기화됨.
- **`harness` 브랜치에 미병합 상태로 존재하는 중요한 작업** (2026-08-22 기준, `main`과 merge-base `abe6fd486`에서 갈라짐, harness 고유 커밋 6개):
  - `scripts/regression_test.py` — 백준 저장 풀이 전체 회귀 테스트 스크립트 (이전에 "다음에 개발하면 좋을 것"으로 제안했던 것과 동일한 아이디어가 이미 구현되어 있음)
  - `server/execution.py` — 코드 실행 하네스 코어 (격리 강화)
  - `docs/decisions/`, `docs/failures/`, `docs/domain/glossary.md` — 의사결정/트러블슈팅/용어집 지식 저장소
  - `pyproject.toml` + ruff 린터 설정, `tools/`로 런처 스크립트 정리, 제출 탭 결과 카드 UI 고도화
  - **충돌 위험**: `server/db.py`, `server/routers/problems.py`, `server/main.py` 등 main에서도 활발히 수정된 핵심 파일과 겹쳐서, merge 시 자동 병합이 안 되고 수동 충돌 해결이 필요할 것으로 예상됨. 사용자가 "일단 보류"를 선택해 아직 손대지 않음.
- **주의**: 이번 세션 중 한 번 다른 컴퓨터(`C:\Users\허민엽\...` 경로)에서 `git push`가 non-fast-forward로 거부된 적 있음 — 원인은 이 컴퓨터에서 먼저 8개 커밋을 push했기 때문. `git pull origin main` 후 재push로 해결됨. **여러 컴퓨터를 오가며 작업할 땐 항상 시작 전에 `git pull`부터 하는 습관 필요.**

---

## 4. 아키텍처 요약 (CLAUDE.md 대비 추가 상세)

- **백엔드**: FastAPI + SQLite. 라우터는 `server/routers/`에 `problems.py`(검색/상세/즐겨찾기/통계/유저레벨), `run.py`(코드 실행), `testcases.py`(AI 테케 생성/채점), `counterexample.py`(testcase.ac 연동 + AI 반례 폴백), `drafts.py`(임시저장), `solutions.py`(백준 폴더에 실제 저장) 로 나뉨.
- **서버 생명주기**: `server/main.py`의 하트비트(`/api/heartbeat`)+워치독 스레드가 브라우저 탭이 열려있는 동안만 서버를 살려둠 (2-5 참고). `frontend/common.js`가 주기적 하트비트 + `pagehide` 시 `sendBeacon`으로 종료 신호 전송.
- **유저 레벨**: `server/db.py::get_user_level()`이 `solved_at` 순서로 풀이 이력을 시뮬레이션해 경험치·레벨·레벨업 히스토리를 매 요청마다 계산 (별도 저장 테이블 없음). 상세는 `docs/user-level-system.md`.
- **DB 마이그레이션 패턴**: `server/db.py`의 `_migrate(conn)`이 `get_conn()`을 호출할 때마다 실행됨. 컬럼 존재 여부를 `PRAGMA table_info`로 체크하고 없으면 `ALTER TABLE ... ADD COLUMN`. 새 컬럼 추가할 때 이 패턴 그대로 따라가면 됨.
- **JSON 파일 캐시 패턴**: `testcases/{id}.json`(AI 생성 테케), `testcases/{id}_ref.json`(AI 반례 폴백용 정답코드+생성기 캐시), `drafts/{id}.json`(임시저장) 전부 동일한 "problem_id 기준 파일 하나" 패턴.
- **프론트**: 순수 JS + Monaco Editor(CDN). 공통 스타일/유틸은 `frontend/common.css`, `common.js`. 페이지별로 `index.html/css`(목록), `problem.html/css`(풀이), `stats.html/css`(통계) 분리.
- **디자인 토큰**: `common.css`의 `:root`에 `--bg`, `--surface`, `--accent`, `--ok`, `--err`, `--tle` 등 정의. 다크 테마 전용, 라이트 모드 없음.

---

## 5. 알아둬야 할 잡음/함정

- ~~`requirements.txt`에 `anthropic`/`httpx`/`python-dotenv` 패키지가 빠져있음~~ → 2-9에서 수정 완료 (2026-08-22).
- ~~`testcases/` 폴더가 사실 gitignore 안 되어 있음~~ → 2-9에서 수정 완료 (2026-08-22).
- **`e.currentTarget`은 `await` 이후 `null`이 된다.** `index.html`의 `toggleFavorite(e, id)`에서 겪은 실제 버그. 이벤트 디스패치가 끝나면 브라우저가 `currentTarget`을 비운다. `async` 이벤트 핸들러에서 `e.currentTarget`을 쓸 거면 **`await` 하기 전에, 함수 맨 위에서 동기적으로** 로컬 변수에 캡처해야 한다.
- **git `reset --soft`는 브랜치에 고유 커밋이 없을 때 위험할 수 있음.** 예전 세션에서 `feature/*` 브랜치가 `main`과 트리가 다른 상태에서 `git reset --soft main`을 했더니 수백 개 파일이 스푸리어스하게 staged deletion으로 표시된 적 있음. 브랜치에 합칠 고유 커밋이 없으면 `reset`/`rebase` 대신 그냥 `git merge`를 쓰는 게 안전.
- **AI 코드 실행 관련 보안 경계**: `POST /api/run`과 AI 반례 폴백의 입력 생성기 실행은 전부 로컬 subprocess 기반이고 별도 샌드박스가 없다 (`CLAUDE.md`에도 명시됨). 로컬 전용 도구라는 전제.
- **`/stats` 페이지 경로는 `/stats.html`이 아니라 `/stats`.** `frontend/stats.html`은 정적 파일로 직접 서빙되는 게 아니라 `server/main.py`의 `@app.get("/stats")` 핸들러가 `FileResponse`로 반환하는 것. `/stats.html`로 접속하면 404.
- **프론트 CSS/JS 수정 후 브라우저에 반영이 안 되면 십중팔구 캐시 문제.** 서버 재시작만으로는 부족하고 `Ctrl+Shift+R` 하드 리프레시가 필요했던 경우가 반복됨 (즐겨찾기 기능, 유저 레벨 시스템 검증 때 둘 다 겪음).
- **`git push origin --delete <branch>`는 auto-mode 권한 정책에 막힐 수 있음.** 원격 브랜치 삭제는 "허용됨" 목록에 없어서 사용자가 직접 실행해야 하는 경우가 있었음 (2-8 참고).

---

## 6. 사용자(허민엽)의 작업 스타일 / 명시적 요청 사항

- **새 기능이나 UI 리디자인 작업 전에는 항상 한국어로 구현 계획을 먼저 보고하고 확인받은 뒤 코드를 작성할 것.** (두 번 강조됨 — 조용히 구현부터 시작하면 안 됨.)
- 큰 작업 시작 전에 "먼저 커밋 & 푸시하고 시작해" 같은 요청이 있었음 — feature 작업 전에 기존 변경사항을 먼저 커밋/푸시하는 흐름을 선호.
- 여러 대의 컴퓨터(이 컴퓨터, `허민엽` 계정 PC 등)를 오가며 작업 중이라 **브랜치/커밋 동기화 상태에 특히 민감**함. push 거부 같은 상황이 실제로 발생했음.
- git 작업 시 `reset`/`rebase`류 destructive 명령보다 일반 `merge`를 선호.

---

## 7. 진행 중이거나 다음에 이어갈 작업

### 7-0. `harness` 브랜치 반영 방식 결정 (보류 중, 최우선 후보)
2-8/섹션 3 참고. `scripts/regression_test.py`, `server/execution.py`, `docs/decisions|failures|domain/` 등 이미 완성된 작업이 `harness`에 잠들어 있음. `main`과 58커밋 갈라졌고 핵심 서버 파일이 겹쳐서 merge 시 수동 충돌 해결이 필요할 전망. 사용자가 "일단 보류"를 선택했으니, 다시 논의할 때 세 가지 선택지(전체 merge / 필요한 파일만 cherry-pick / 계속 보류) 중 고르는 것부터 시작.

### 7-1. CSS 정리 (보고만 하고 아직 미착수, 사용자 확인 대기 중)
"css적으로 좀 고칠부분은?" 질문에 대한 답변으로 아래 항목들을 리포트했음. 아직 어떤 것부터 할지 확답은 못 받은 상태:

1. `--purple` 변수가 `common.css` `:root`에 실제로 선언된 적 없이 `var(--purple, #a78bfa)` fallback으로만 `problem.css` 전역에서 쓰이는 중 → `:root`에 정식 선언 필요.
2. 즐겨찾기 노란색(`#facc15`)이 변수화 안 되고 `index.css`/`problem.css`에 하드코딩 중복 → `--favorite` 변수 추가 권장.
3. `.fav-star` 규칙 + `@keyframes fav-pop`이 `index.css`와 `problem.css`에 완전 중복 선언됨 → `common.css`로 이동해 통합.
4. "풀었던 문제만"(체크박스+라벨 스타일)과 "즐겨찾기만"(pill 버튼 스타일) 필터 UI 톤이 서로 안 맞음 → 같은 스타일로 통일 권장.
5. 버튼 스타일(`#gen-tc-btn`, `#find-ce-btn`, `#save-solution-btn` 등)이 전부 ID 셀렉터로 padding/border/font-size를 반복 선언 → 공통 `.btn` 베이스 클래스 + modifier 클래스 구조로 리팩터 권장.
6. `#prob-desc`에서 텍스트 색이 `var(--text)` 대신 하드코딩된 `#ccc`.
7. 페이지네이션 현재 버튼(`.pg-btn.cur`) 배경이 `#1a3a3a` 하드코딩, `--accent` 기반 `color-mix`로 바꾸면 테마 변경에 유연해짐.

우선순위 제안: 1·2·3(변수/중복 정리) → 4(필터 톤 통일) → 5(버튼 리팩터) → 6·7은 사소함.

### 7-2. 이전 UI 전체 리뷰에서 나온 미착수 항목
("UI 전체적으로 검토해주고 더 디벨롭할 부분 보고해"에 대한 답변 중 아직 미착수)
- 문제 목록 정렬 옵션 (난이도순/번호순 등)
- 즐겨찾기 우선 정렬 / 즐겨찾기 개수 요약 표시
- ~~목록 카드에 "임시저장 존재함" 표시~~ → 2-6에서 "풀고 있는 문제만" 필터 + 뱃지로 구현 완료
- "⏱ 성능 테스트" 기능 (TLE 전용 스트레스 테스트) — 아이디어 단계, 구체적 설계는 아직 없음
- ~~`index.html` 헤더에 유저 레벨 배지 상시 노출~~ → 2-9에서 구현 완료

### 7-3. `PLAN.md` 문서 드리프트 — 2026-08-22에 해소됨
과거엔 `PLAN.md`가 API 목록/디렉토리 구조 등에서 실제 구현과 어긋나 있었음. 2026-08-22 세션에서 `CLAUDE.md`/`PLAN.md`/이 문서를 전부 현재 구현 상태 기준으로 갱신 완료 (목표 기능 8~13번, API 목록, 디렉토리 구조, 미결사항 표 등). 앞으로 새 기능을 merge할 때마다 세 문서를 같이 갱신하는 습관이 필요.
