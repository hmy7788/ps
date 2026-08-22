# 커스텀 문제(내가 만든 문제) 기능

브랜치: `feature/custom-problems`

## 개요

백준 아카이브 문제뿐 아니라, 사용자가 직접 문제를 만들어서 같은 화면(에디터/실행/제출)으로
풀어볼 수 있게 하는 기능. **통계·유저 레벨(EXP) 시스템과는 무관한 연습용** 문제로 취급한다.

## 설계 결정

### 1. 저장 위치 — `problems` 테이블에 그대로 저장
`all_problems/`는 원본 아카이브라 손댈 수 없으므로, 커스텀 문제는 파일이 아니라
`problems` 테이블에 `is_custom=1` 플래그를 붙여 저장한다. 이렇게 하면 검색/필터/상세조회/
실행/제출 API를 전부 그대로 재사용할 수 있다 (실제로 `generate-testcases`, `submit` 등은
DB의 문제 상세만 보고 동작하므로 코드 수정이 필요 없었다).

### 2. ID 충돌 방지 — 음수 ID
백준 문제 ID는 전부 양수이므로, 커스텀 문제는 `MIN(id)-1`로 계산한 **음수 ID**(-1, -2, ...)를
자동 발급한다. 별도 카운터 테이블 없이 기존 `id` 컬럼만으로 충돌 없이 구분된다.

### 3. XSS 방지 — 저장 시점에 이스케이프
`problem.json`의 `description`/`input`/`output`은 프론트에서 `innerHTML`로 그대로
렌더링된다. 백준 아카이브는 신뢰된 데이터라 안전했지만, 커스텀 문제는 사용자가 직접
입력한 텍스트이므로 **저장 전에 `html.escape()` 처리 후 문단 단위로 `<p>`/`<br>`만 붙여서
저장**한다 (`server/utils.py::render_custom_text`). 실제로 `<script>alert(1)</script>`를
설명에 넣고 저장 → 문제 페이지에서 그대로 텍스트로만 보이고 실행되지 않는 것을 확인했다.

수정 폼에 원본 텍스트를 다시 보여줘야 하므로, DB에 `raw_description`/`raw_input_desc`/
`raw_output_desc` 컬럼을 추가해 이스케이프 전 원문을 별도 보관한다 (표시용 HTML과
편집용 원문을 분리 저장 — 한쪽만 있으면 왕복 변환 과정에서 정보 손실이 생긴다).

### 4. 채점용 테스트케이스
생성 폼에서 "예제(샘플)"와 "히든 테스트케이스"를 분리 입력받는다.
- 히든 테케를 입력하면 그걸로, 비워두면 예제를 그대로 `testcases/{id}.json`에 저장해서
  **"제출" 탭이 별도 생성 없이 바로 동작**하게 한다.
- 기존 "🧪 채점용 테케 만들기"(AI 자동생성) 버튼도 그대로 동작한다 — 이 엔드포인트는
  DB의 문제 설명만 보고 Claude에게 테케를 만들어 달라고 요청하므로 커스텀/아카이브
  문제를 구분하지 않는다.

### 5. 레벨 필터 사각지대 → 6~20으로 제한
목록 페이지의 난이도 필터 체크박스는 Silver(6-10)/Gold(11-15)/Platinum(16-20)만 존재한다
(Bronze/Diamond/Ruby 없음). 커스텀 문제에 그 범위 밖 레벨을 허용하면 필터 UI에서 영영
찾을 수 없는 문제가 생기므로, **커스텀 문제 생성 시 난이도를 6~20으로 제한**했다
(`server/routers/custom_problems.py`의 `MIN_LEVEL`/`MAX_LEVEL`). 대신 레벨 범위와
무관하게 항상 찾을 수 있도록 "🛠 내가 만든 문제만" 필터 칩을 별도로 추가했다.

### 6. 통계/레벨 시스템에서 제외 (연습용)
사용자 요청에 따라 커스텀 문제를 풀어도 solved.ac 스타일 유저 레벨(EXP)이나 통계
페이지(히트맵/스트릭/태그·난이도 분포)에는 전혀 반영되지 않는다.
`server/db.py`의 `get_stats()`, `get_heatmap_and_streak()`, `get_user_level()` 세
함수의 SQL에 전부 `AND (is_custom IS NULL OR is_custom=0)` 조건을 추가해서 구현했다.

### 7. "백준에 저장" 기능 — 별도 폴더로 분리 (구현 중 발견한 문제)
처음엔 `server/routers/solutions.py::save_solution`을 그대로 뒀는데, 실제로 curl로
테스트해보니 커스텀 문제(id=-1)를 저장하면 `백준/Silver/-1. 제목/` 폴더가 생기면서
`https://www.acmicpc.net/problem/-1`라는 **존재하지 않는 링크가 박힌 README**까지
자동 생성되는 걸 확인했다. `백준/`는 실제 백준 아카이브 전용 폴더인데 연습용 커스텀
문제가 섞여 들어가는 건 원래 디렉터리 구조 규칙을 깨는 것이라 판단해서, 저장 위치를
분리했다:
- 실제 백준 문제(`id >= 0`): 기존 그대로 `백준/{등급}/{id}. {제목}/`
- 커스텀 문제(`id < 0`): `커스텀문제/{id}. {제목}/` (등급 폴더 없이 바로 한 단계),
  README도 acmicpc.net 링크 없는 별도 템플릿(`_build_readme_custom`) 사용

`list_solutions`/`last_solution`/`get_solution`/`save_solution` 네 곳에서 반복되던
"폴더 찾기" 로직을 `_candidate_folders(problem_id)` 헬퍼로 통합하면서 이 분기도 함께
처리했다. `커스텀문제/`는 `백준/`, `프로그래머스/`와 마찬가지로 사용자가 직접 작성한
콘텐츠이므로 `.gitignore` 대상이 아니다 (build 산출물/캐시가 아님).

## 구현 파일

- **`server/db.py`**: `is_custom`/`raw_description`/`raw_input_desc`/`raw_output_desc`
  컬럼 마이그레이션, `get_problems()`에 `custom_only` 필터, `next_custom_id()`,
  `create_custom_problem()`/`update_custom_problem()`/`delete_custom_problem()`/
  `get_custom_raw()`, 통계/레벨 쿼리에 `is_custom` 제외 조건 추가.
- **`server/models.py`**: `ProblemSummary.is_custom` 필드, `CustomProblemCreate` 모델.
- **`server/utils.py`**: `render_custom_text()` — XSS 방지용 이스케이프+문단 변환.
- **`server/routers/custom_problems.py`** (신규): `POST/PUT/DELETE /api/custom-problems`,
  `GET /api/custom-problems/{id}/edit` (수정 폼 프리필용, 원문 텍스트 + 히든 테케 반환).
- **`server/routers/problems.py`**: `GET /api/problems`에 `custom` 쿼리 파라미터 추가.
- **`server/routers/solutions.py`**: `_candidate_folders()` 헬퍼로 리팩터링, 커스텀
  문제는 `커스텀문제/` 폴더에 저장하도록 분기, `_build_readme_custom()` 추가.
- **`server/main.py`**: `custom_problems_router` 등록, `/create` 페이지 라우트 추가.
- **`frontend/create.html`/`create.css`** (신규): 문제 생성/수정 폼. 제목/난이도/시간·
  메모리 제한/태그/설명/입출력 형식 + 예제·히든 테케 반복 입력(추가/삭제) UI.
  `?id=` 쿼리 유무로 생성/수정 모드 전환.
- **`frontend/index.html`/`index.css`**: 헤더에 "🛠 문제 만들기" 링크, "🛠 내가 만든
  문제만" 필터 칩, 카드에 🛠 커스텀 배지.
- **`frontend/problem.html`/`problem.css`**: 헤더에 "✏️ 수정"/"🗑 삭제" 버튼 (커스텀
  문제일 때만 노출), 삭제 시 `confirm()` 후 `DELETE /api/custom-problems/{id}` 호출.

## API

| 메서드 | 경로 | 설명 |
|---|---|---|
| POST | `/api/custom-problems` | 커스텀 문제 생성 (음수 ID 자동 발급) |
| PUT | `/api/custom-problems/{id}` | 수정 (id<0인 것만 허용) |
| DELETE | `/api/custom-problems/{id}` | 삭제 (DB 행 + `testcases/{id}.json`) |
| GET | `/api/custom-problems/{id}/edit` | 수정 폼 프리필용 원문 데이터 |
| GET | `/api/problems?custom=1` | 커스텀 문제만 필터 |

## 검증

- curl로 XSS 페이로드(`<script>alert(1)</script>`)를 설명에 넣고 생성 → 상세 조회 시
  `&lt;script&gt;...&lt;/script&gt;`로 이스케이프된 것 확인.
- curl로 히든 테케 2개를 넣고 생성 → `/submit`에서 2/2 통과 확인.
- curl로 `/api/custom-problems/{id}/edit` 호출 → 원문(비이스케이프) 텍스트와 샘플과
  겹치지 않는 히든 테케만 정확히 돌아오는 것 확인.
- 실제 Chrome 브라우저: `/create`에서 폼 작성 → 생성 → `/problem?id=-1`로 리다이렉트 →
  설명에 스크립트 태그가 텍스트로만 표시(경고창 안 뜸) → "실행" 탭 1/1 통과 →
  "제출" 탭 1/1 통과 → "✏️ 수정" 버튼으로 편집 폼 진입 시 원문 그대로 프리필 확인 →
  목록 페이지에서 "내가 만든 문제만" 필터로 커스텀 배지 달린 카드 확인.
- `save-solution` 호출 시 `백준/` 대신 `커스텀문제/{id}. {제목}/`에 저장되고, 기존
  `백준/` 트리에는 영향이 없는 것을 확인 (초기 구현에서 이 문제를 발견해 수정함 — 위
  "6. 백준에 저장 기능" 항목 참고).
- 통계 API(`/api/stats`, `/api/stats/level`, `/api/stats/heatmap`)가 커스텀 문제 풀이를
  집계하지 않는 것을 확인 (풀기 전/후 유저 레벨·총 풀이수 불변).

## 남아있는 제약 (알고 있는 트레이드오프)

- 커스텀 문제 난이도는 6~20(Silver~Platinum)으로 제한된다. Bronze/Diamond/Ruby로
  만들고 싶다면 목록 페이지 레벨 필터 체크박스 그룹을 먼저 확장해야 한다.
- 히든 테케 없이 예제만으로 저장한 뒤 수정 화면에 들어가면 "히든 테케"란은 비어
  보인다 (예제와 내용이 같은 테케는 편집 화면에서 히든 테케로 다시 보여주지 않는
  휴리스틱 때문 — 의도된 동작).

## 후속 개선 (2차 작업)

사용자 피드백으로 아래 4가지를 추가 반영했다.

### 1. 문제 설명 — 마크다운 + HTML 문법 지원
기존 `render_custom_text()`(이스케이프 후 `<p>`로만 감싸는 방식)를
`render_custom_markdown()`으로 교체했다 (`server/utils.py`):
- `markdown` 패키지로 `#`/`**굵게**`/`- 목록`/코드블록/표 등 마크다운 문법을 실제
  HTML 태그로 변환 (`extensions=["fenced_code","tables","nl2br","sane_lists"]`).
- 원본 HTML 태그도 그대로 통과시키되(마크다운 라이브러리 기본 동작), `bleach.clean()`으로
  허용 목록(`MD_ALLOWED_TAGS`/`MD_ALLOWED_ATTRS`)에 없는 태그·속성은 제거해서 XSS를 막는다.
  `<script>`처럼 위험한 태그는 태그+내용째 제거되고, `onclick` 같은 위험 속성은 태그는
  남기고 속성만 제거된다.
- `requirements.txt`에 `markdown`, `bleach`(+의존성 `webencodings`) 추가 (UTF-16(BOM)
  인코딩 유지하며 파이썬으로 직접 갱신 — Write 도구로 직접 쓰면 인코딩이 깨짐).
- 설명뿐 아니라 입력/출력 형식 필드도 동일하게 마크다운을 지원한다 (같은 함수 재사용).

### 2. 태그 — 검색 가능한 select 드롭다운
기존 쉼표 구분 텍스트 입력을 목록 페이지의 태그 필터와 동일한 패턴(검색 입력 +
체크박스 목록)으로 교체했다 (`frontend/create.html`). `common.js`의 `sortTags()`/`tagKo()`를
그대로 재사용해서 태그 우선순위 정렬과 한글 라벨을 그대로 가져왔다.
선택된 태그는 별도 배열(`selectedTags`)로 관리하고, 체크박스 `onchange`가 아니라
개별 토글 함수(`toggleTagOption(tag)`)로 상태를 갱신하도록 만들어서, 검색어로 필터링된
상태에서 이전에 선택한(현재 화면에 안 보이는) 태그가 사라지는 버그를 피했다.

### 3. 커스텀 문제 제목의 "#-1" 표시 제거
음수 ID는 사용자에게 아무 의미가 없으므로, `problem.html`과 `index.html`에서
`is_custom`이면 `#{id}` 접두사를 붙이지 않도록 분기했다 (배지의 🛠 커스텀 표시로
이미 구분되므로 중복 정보이기도 했다).

### 4. 수정/삭제 UI 개선 — 아이콘 버튼 + 인라인 확인
기존엔 "✏️ 수정"/"🗑 삭제" 텍스트 버튼 + 브라우저 네이티브 `confirm()` 다이얼로그를
썼는데, 앱의 다른 부분(예: "백준에 저장"의 메모 입력 폼)은 전부 인라인 UI로
확인을 받는 것과 스타일이 어긋났다. 그래서:
- 버튼을 별 아이콘(`.fav-star`)과 같은 스타일의 아이콘 전용 버튼(✏️/🗑)으로 축소.
- 삭제 클릭 시 네이티브 `confirm()` 대신, 헤더 안에서 아이콘 버튼 자리를
  "삭제할까요? [삭제] [취소]" 인라인 문구로 바꿔치기하는 방식으로 변경
  (`custom-actions-default` ↔ `custom-actions-confirm` 토글).

#### 구현 중 발견한 버그: 드롭다운 팝오버가 안 보임
처음엔 삭제 확인 UI를 헤더 아래로 떨어지는 절대위치 팝오버(드롭다운 스타일)로
만들었는데, 실제로 클릭해도 화면에 전혀 나타나지 않았다. 원인은
`problem.css`의 `header { overflow: hidden; }` — 제목이 길어질 때 헤더 높이가
안 늘어나게 하려고 걸어둔 규칙인데, 이게 헤더 밖으로 삐져나오는 절대위치
팝오버까지 통째로 잘라버렸다. `position: fixed`로 바꿔 좌표를 계산하는 대신,
아예 팝오버를 없애고 헤더 같은 줄 안에서 버튼 자리를 확인 문구로 바꿔치기하는
"인라인 치환" 방식으로 재구현해서 해결했다 — 헤더의 flex 레이아웃을 그대로
타기 때문에 overflow:hidden과 무관하게 항상 보인다.

#### 구현 중 발견한 문제: 죽지 않은 이전 세션의 서버 프로세스
기능 구현 후 브라우저로 재검증하는 과정에서, 분명 최신 코드로 서버를
재시작했는데도 마크다운이 전혀 렌더링되지 않고 예전 방식(이스케이프+`<p>`감싸기)
그대로 나오는 현상을 겪었다. `netstat`로 확인해보니 이전 세션에서 종료했다고
생각했던 uvicorn 프로세스가 실제로는 여전히 포트 8000을 물고 있었고, 새로 띄운
프로세스는 "주소 사용 중" 에러로 조용히 실패한 상태였다 (백그라운드 실행이라
에러가 눈에 안 띔) — 그래서 curl/브라우저 테스트가 전부 옛날 프로세스에 붙어서
옛날 코드로 응답하고 있었다. `netstat -ano | grep :8000`으로 실제 PID를 찾아
강제 종료 후 재기동하니 바로 해결됐다. **교훈: 코드 수정 후 서버를 재시작할 때는
포트를 점유한 프로세스를 확인하고 확실히 종료했는지 검증할 것 (백그라운드
실행은 바인딩 실패를 조용히 삼킬 수 있음).**

### 5. (재수정) 수정/삭제 버튼을 아이콘 전용 → 아이콘+텍스트 칩 버튼으로 되돌림
2차 개선에서 만든 아이콘 전용 버튼(배경/테두리 없이 이모지만)은 실제로 써보니
"이상하다"는 피드백을 받았다. 원인을 다시 보니, 이 앱의 실제 액션 버튼들
(`💾 백준에 저장`, `🧪 채점용 테케 만들기`, `▶ 제출` 등, `#run-toolbar`/`#submit-toolbar`)은
전부 아이콘+텍스트 라벨을 갖춘 테두리 있는 칩 버튼(`background: var(--surface)`,
`border: 1px solid var(--border)`, `border-radius: 5px`)이었는데, 아이콘 전용
버튼은 이 관례에서 벗어나 배지들 사이에 맨 이모지만 떠 있는 것처럼 보였다.
`.icon-btn`을 없애고 `.custom-action-btn`(아이콘+"수정"/"삭제" 텍스트, 테두리 있는 칩)으로
교체해서 기존 액션 버튼과 시각적으로 통일했다. 삭제 확인 인라인 UI도 마찬가지로
`#save-memo-confirm`/`#save-memo-cancel` 패턴(확인=단색 배경 강조, 취소=테두리만)을
그대로 따르도록 다시 맞췄다.

### 6. 마크다운 렌더링 타이포/여백 보강
문제 설명이 마크다운으로 렌더링되기 시작했지만(개선 1), `problem.css`의 `#prob-desc`
스타일은 원래 백준 아카이브 HTML(주로 `<p>`/`<ul>`만 있음) 기준으로 만들어져 있어서
`<h1>~<h6>`, 인라인 `<code>`, `<blockquote>`, `<hr>`는 스타일이 전혀 없어 브라우저
기본값(여백이 문단 line-height 1.75와 안 어울림)으로 렌더링되고 있었다. 그래서
"빡빡하다"는 피드백이 나왔다. 다음을 추가/조정:
- `p`/`ul`/`ol`/`pre`/`blockquote` 하단 여백 8px → 14px, `li` 4px → 6px로 확대.
- `h1~h6` 스타일 신규 추가 (크기 축소: h1 1.4em/h2 1.25em/h3 1.1em, 여백 `4px 0 12px`).
- 인라인 `code`에 배경 chip 스타일 추가, `pre code`는 이중 배경 되지 않도록 리셋.
- `blockquote`에 왼쪽 테두리 + 흐린 텍스트색 추가.
- `#desc-body`/`#desc-input`/`#desc-output`의 마지막 자식 요소 `margin-bottom` 리셋
  (설명 영역 끝에 불필요한 여백이 남지 않도록).
이 스타일은 `#prob-desc` 전역에 적용되므로 실제 백준 아카이브 문제(원본 HTML에
`<code>`/제목 태그가 나오는 경우)에도 동일하게 적용된다.

### 검증 (2차)
- 마크다운(`#`, `**`, `-`, 코드블록)이 실제 `<h1>`/`<strong>`/`<ul><li>`로 렌더링되는 것을
  브라우저에서 시각적으로 확인.
- `<script>alert(1)</script>`과 `<b onclick="alert(2)">...</b>`를 설명에 넣어도 경고창이
  뜨지 않고, 후자는 굵은 텍스트만 남고 `onclick` 속성은 제거된 것을 확인.
- 태그 드롭다운에서 검색어를 바꿔가며 여러 태그를 선택해도 이전 선택이 유지되는 것,
  선택 개수 배지와 선택된 태그 미리보기 줄이 정확히 갱신되는 것을 확인.
- 커스텀 문제 상세/목록 페이지 모두에서 "#id" 표시가 사라진 것을 확인.
- 삭제 아이콘 클릭 → 인라인 확인 문구 표시 → "취소" 클릭 시 원래 아이콘으로
  복귀 → 실제 삭제까지 브라우저에서 확인.
