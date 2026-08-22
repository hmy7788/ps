# 하우스키핑 3종 (2026-08-22)

브랜치: `chore/housekeeping-fixes`

문서(`CLAUDE.md`/`HANDOFF.md`)에 여러 세션째 "알려진 이슈"로만 적혀있던 것들과, 이전에 제안했던 작은 UI 개선 하나를 실제로 처리한 기록.

## 1. `requirements.txt` 누락 패키지 추가

### 문제
`server/routers/testcases.py`, `server/routers/counterexample.py`가 `import anthropic`을, `counterexample.py`가 `import httpx`를, `server/main.py`가 `from dotenv import load_dotenv`를 쓰는데 정작 셋 다 `requirements.txt`엔 없었다. 새 컴퓨터에서 `pip install -r requirements.txt`만 하면 AI 테케 생성/AI 반례 폴백/testcase.ac 연동/`.env` 로딩이 전부 `ModuleNotFoundError`로 죽는 상태였음.

### 해결
현재 가상환경에 실제로 설치되어 있던 버전 그대로 고정해서 추가:
```
anthropic==0.120.0
httpx==0.28.1
python-dotenv==1.2.2
```
`pip install -r requirements.txt --dry-run`으로 정상 파싱/해결되는 것 확인.

### 알아두면 좋은 점
이 파일은 **UTF-16(BOM) 인코딩**이다 (`b'\xff\xfe...'`로 시작). 아마 PowerShell에서 `pip freeze > requirements.txt` 같은 리다이렉션으로 생성돼서 그런 것으로 추정. pip은 파일 앞의 BOM을 보고 인코딩을 자동 감지해서 읽기 때문에 문제없이 동작한다 — 굳이 UTF-8로 바꿀 필요 없어서 인코딩은 그대로 유지하고 내용만 수정함(Python에서 `encoding='utf-16'`으로 열고/써야 함).

## 2. `testcases/` 완전한 gitignore 처리

### 문제
`CLAUDE.md`에는 "`testcases/`는 gitignore 대상"이라고 적혀 있었지만 실제 `.gitignore`엔 규칙이 없었고, 예전에 실수로 커밋된 7개 파일(`testcases/1010.json`, `testcases/1012.json`, `testcases/1068.json`, `testcases/10826.json`, `testcases/1251.json`, `testcases/15649_ref.json`, `testcases/2167.json`)이 git에 그대로 남아있었다.

### 해결
- `.gitignore`에 `testcases/` 한 줄 추가
- `git rm --cached -r testcases/`로 위 7개 파일을 git 추적에서만 제외 (디스크의 실제 파일은 그대로 남아있음 — 삭제한 게 아니라 "이제부터 git이 안 쫓아간다"는 뜻)

### 확인
`git rm --cached` 이후 로컬 `testcases/` 폴더의 파일 개수가 그대로 7개인 것 확인 (데이터 유실 없음).

## 3. `index.html` 헤더에 유저 레벨 미니 배지

### 배경
`docs/user-level-system.md`의 "향후 확장 아이디어"로 남겨뒀던 항목. 이미 만들어둔 `GET /api/stats/level`을 그대로 재사용하면 되는 작은 작업.

### 구현
- `frontend/index.html`: 로고 옆에 `<a class="level-badge-mini" id="level-badge-mini" href="/stats">` 추가, `loadLevelBadge()`가 `/api/stats/level`을 fetch해서 `Lv.11 Gold V` 형태로 텍스트/색상 클래스(`lv.class`)를 채움. 실패해도 조용히 무시(배지는 부가 기능이라 에러로 목록 페이지 전체를 막으면 안 됨).
- `frontend/index.css`: `.level-badge-mini` 스타일 추가. 기존 `.stats-link`와 같은 톤(테두리+pill), 티어별 색상은 `stats.css`의 `.level-badge`와 동일하게 `--bronze`/`--silver`/`--gold`/`--platinum`/`--diamond`/`--ruby` CSS 변수 재사용.

### 테스트
로컬 서버 기동 → Chrome으로 `/` 접속 → 하드리프레시 후 헤더에 "Lv.11 Gold V" 금색 배지가 정상 표시되는 것 확인.

## 관련 문서
- `docs/user-level-system.md` — 유저 레벨 시스템 자체의 설계/API
- `HANDOFF.md` 2-9 — 세션 기록
- `CLAUDE.md`, `PLAN.md` — 위 이슈들을 "알려진 이슈"로 기록했던 문서, 이번에 최신 상태로 갱신됨
