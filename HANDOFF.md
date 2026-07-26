# HANDOFF.md

다른 컴퓨터에서 이어서 개발하기 위한 인수인계 문서. 2026-07-26 기준 최신 상태.
`CLAUDE.md`(프로젝트 규칙)와 `PLAN.md`(원래 설계 문서)는 그대로 유효하며, 이 문서는 "지금까지 뭘 했고 다음에 뭘 할지"에 집중한다.

---

## 1. 새 컴퓨터에서 시작하는 법

```bash
git clone https://github.com/hmy7788/ps.git
cd ps
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
pip install anthropic           # ⚠️ requirements.txt에 빠져있음 (아래 5번 참고)

# SQLite 인덱스 생성 (최초 1회, 시간 소요 — all_problems/ 스캔)
python scripts/build_index.py

# .env 파일 생성 (AI 테케 생성 기능 쓰려면 필수)
echo ANTHROPIC_API_KEY=sk-ant-... > .env

# 서버 실행
uvicorn server.main:app --reload --port 8000
```

`problems.db`, `testcases/*.json`(AI 생성분), `drafts/`는 전부 gitignore 대상이라 새 컴퓨터에는 없다.
- `problems.db`는 `build_index.py`로 재생성.
- `testcases/`, `drafts/`는 로컬 캐시라 없어도 기능은 동작하고, 쓰면서 다시 쌓인다 (단, `testcases/2167.json`, `testcases/15649_ref.json`처럼 실수로 커밋된 것들은 git에 남아있음 — 8번 참고).

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

---

## 3. 현재 브랜치/커밋 상태

- `main`이 유일한 활성 브랜치, origin과 동기화됨.
- 최근 커밋 흐름(위→최신): 즐겨찾기+드래프트 merge → AI 반례 폴백 merge → BaekjoonHub 자동 커밋 다수(N과 M 시리즈 등) → 다른 컴퓨터에서의 병합 커밋.
- **주의**: 이번 세션 중 한 번 다른 컴퓨터(`C:\Users\허민엽\...` 경로)에서 `git push`가 non-fast-forward로 거부된 적 있음 — 원인은 이 컴퓨터에서 먼저 8개 커밋을 push했기 때문. `git pull origin main` 후 재push로 해결됨. **여러 컴퓨터를 오가며 작업할 땐 항상 시작 전에 `git pull`부터 하는 습관 필요.**

---

## 4. 아키텍처 요약 (CLAUDE.md 대비 추가 상세)

- **백엔드**: FastAPI + SQLite. 라우터는 `server/routers/`에 `problems.py`(검색/상세/즐겨찾기), `run.py`(코드 실행), `testcases.py`(AI 테케 생성/채점), `counterexample.py`(testcase.ac 연동 + AI 반례 폴백), `drafts.py`(임시저장), `solutions.py`(백준 폴더에 실제 저장) 로 나뉨.
- **DB 마이그레이션 패턴**: `server/db.py`의 `_migrate(conn)`이 `get_conn()`을 호출할 때마다 실행됨. 컬럼 존재 여부를 `PRAGMA table_info`로 체크하고 없으면 `ALTER TABLE ... ADD COLUMN`. 새 컬럼 추가할 때 이 패턴 그대로 따라가면 됨.
- **JSON 파일 캐시 패턴**: `testcases/{id}.json`(AI 생성 테케), `testcases/{id}_ref.json`(AI 반례 폴백용 정답코드+생성기 캐시), `drafts/{id}.json`(임시저장) 전부 동일한 "problem_id 기준 파일 하나" 패턴.
- **프론트**: 순수 JS + Monaco Editor(CDN). 공통 스타일/유틸은 `frontend/common.css`, `common.js`. 페이지별로 `index.html/css`(목록), `problem.html/css`(풀이), `stats.html/css`(통계) 분리.
- **디자인 토큰**: `common.css`의 `:root`에 `--bg`, `--surface`, `--accent`, `--ok`, `--err`, `--tle` 등 정의. 다크 테마 전용, 라이트 모드 없음.

---

## 5. 알아둬야 할 잡음/함정

- **`requirements.txt`에 `anthropic` 패키지가 빠져있음.** AI 테케 생성(`testcases.py`)과 AI 반례 폴백(`counterexample.py`) 둘 다 `import anthropic`을 함수 내부에서 지연 임포트하는데, 정작 패키지 목록에는 없다. 새 컴퓨터에서 `pip install -r requirements.txt`만 하면 이 기능들이 `ModuleNotFoundError`로 죽는다. `pip install anthropic`을 별도로 해줘야 함. (원인이 뭔지는 불명 — `pip freeze`로 requirements.txt를 만들었는데 그 시점에 가상환경에 anthropic이 없었거나, 나중에 추가 설치했는데 requirements.txt를 갱신 안 한 것으로 추정.)
- **`testcases/` 폴더가 사실 gitignore 안 되어 있음.** `CLAUDE.md`에는 "testcases/는 gitignore 대상"이라고 적혀 있지만 실제 `.gitignore`에는 `testcases/` 룰이 없고, `testcases/2167.json`, `testcases/15649_ref.json` 등이 이미 git에 커밋되어 있다. CLAUDE.md 작성 당시 의도와 실제 상태가 어긋난 상태. 이번 세션에서 고치지는 않았음 — 만약 의도대로 로컬 전용으로 만들고 싶으면 `.gitignore`에 `testcases/` 추가하고 이미 커밋된 파일들은 `git rm --cached`로 내려야 함 (사용자 확인 필요한 작업이라 보류함).
- **`e.currentTarget`은 `await` 이후 `null`이 된다.** `index.html`의 `toggleFavorite(e, id)`에서 겪은 실제 버그. 이벤트 디스패치가 끝나면 브라우저가 `currentTarget`을 비운다. `async` 이벤트 핸들러에서 `e.currentTarget`을 쓸 거면 **`await` 하기 전에, 함수 맨 위에서 동기적으로** 로컬 변수에 캡처해야 한다.
- **git `reset --soft`는 브랜치에 고유 커밋이 없을 때 위험할 수 있음.** 예전 세션에서 `feature/*` 브랜치가 `main`과 트리가 다른 상태에서 `git reset --soft main`을 했더니 수백 개 파일이 스푸리어스하게 staged deletion으로 표시된 적 있음. 브랜치에 합칠 고유 커밋이 없으면 `reset`/`rebase` 대신 그냥 `git merge`를 쓰는 게 안전.
- **AI 코드 실행 관련 보안 경계**: `POST /api/run`과 AI 반례 폴백의 입력 생성기 실행은 전부 로컬 subprocess 기반이고 별도 샌드박스가 없다 (`CLAUDE.md`에도 명시됨). 로컬 전용 도구라는 전제.

---

## 6. 사용자(허민엽)의 작업 스타일 / 명시적 요청 사항

- **새 기능이나 UI 리디자인 작업 전에는 항상 한국어로 구현 계획을 먼저 보고하고 확인받은 뒤 코드를 작성할 것.** (두 번 강조됨 — 조용히 구현부터 시작하면 안 됨.)
- 큰 작업 시작 전에 "먼저 커밋 & 푸시하고 시작해" 같은 요청이 있었음 — feature 작업 전에 기존 변경사항을 먼저 커밋/푸시하는 흐름을 선호.
- 여러 대의 컴퓨터(이 컴퓨터, `허민엽` 계정 PC 등)를 오가며 작업 중이라 **브랜치/커밋 동기화 상태에 특히 민감**함. push 거부 같은 상황이 실제로 발생했음.
- git 작업 시 `reset`/`rebase`류 destructive 명령보다 일반 `merge`를 선호.

---

## 7. 진행 중이거나 다음에 이어갈 작업

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
- 목록 카드에 "임시저장 존재함" 표시
- "⏱ 성능 테스트" 기능 (TLE 전용 스트레스 테스트) — 아이디어 단계, 구체적 설계는 아직 없음

### 7-3. `PLAN.md`의 원래 설계 (별개 트랙, 진행 여부 불명확)
`PLAN.md`에 있는 `selected_problems/` 기반 대규모 재구성 플랜(레벨 6~20 전체 선별, `scripts/select_problems.py` 등)은 이번 세션에서 손대지 않았음. 현재 웹앱은 그 설계와 다르게 `all_problems/`를 SQLite 인덱스로 직접 서빙하는 방식으로 이미 굴러가고 있어서, `PLAN.md`가 최신 아키텍처를 반영 못 하고 있을 가능성이 있음 — 다음에 정리가 필요할 수도 있는 문서.
