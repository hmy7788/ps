# 유저 레벨 시스템 (solved.ac 스타일)

브랜치: `feat/user-level-system`

## 목표

`/stats` 페이지에 "내가 지금 몇 레벨인가"를 solved.ac처럼 보여준다.
문제 난이도(1~30 스케일, Bronze~Ruby)를 그대로 재사용해서 유저 레벨도 같은 스케일로 표현한다.

## 설계

### EXP(경험치) 공식

- 문제 하나를 풀면 얻는 경험치: `exp = 10 × (문제레벨 ^ 1.5)`
  - 난이도가 높을수록 훨씬 많이 받도록 지수(1.5)를 줌
- 페널티: 내 현재 레벨보다 5 이상 낮은 문제는 경험치 10%만 인정 (`PENALTY_GAP=5`, `PENALTY_MULT=0.1`)
  - 이미 넘어선 쉬운 문제만 반복해서 레벨업하는 것을 막기 위함 (solved.ac도 유사한 감쇠가 있다고 알려짐)

### 레벨업에 필요한 누적 경험치

- `필요경험치(L) = 30 × (L ^ 2.5)`
- 레벨이 올라갈수록 요구량이 가파르게 증가 (레벨 30 만렙까지 존재)

### 레벨 → 티어 라벨 변환

- 1~30을 5단위로 끊어서 Bronze/Silver/Gold/Platinum/Diamond/Ruby, 각 구간 안에서 V→I 순으로 라벨링
- 예: 레벨 1 = Bronze V, 레벨 5 = Bronze I, 레벨 11 = Gold V

### 계산 범위 및 방식

- 이 프로젝트의 DB(`problems` 테이블)는 애초에 레벨 6~20(Silver~Platinum)만 선별 아카이빙되어 있음 (`CLAUDE.md` 참고) → 유저 레벨도 자연히 이 범위에서 푼 문제만 반영됨
- 별도 저장 테이블 없이, 요청 시점에 `solved=1`인 문제를 `solved_at` 오름차순(널이면 뒤로, 그다음 id 순)으로 정렬해 시뮬레이션 → 누적 경험치와 "언제 몇 레벨을 찍었는지" 히스토리를 동시에 계산
- 상수(`EXP_BASE_MULT=10`, `LEVEL_THRESHOLD_MULT=30`)는 실제 이 프로젝트의 현재 풀이 이력(52문제, Silver 위주 + Gold 소수)을 넣어보고 "막 Gold 진입" 정도가 나오도록 보정한 값

## 구현 파일

| 파일 | 변경 내용 |
|---|---|
| `server/db.py` | `level_label()`, `level_class()`, `get_user_level()` 추가 (EXP 계산 및 레벨업 히스토리 시뮬레이션) |
| `server/routers/problems.py` | `GET /api/stats/level` 엔드포인트 추가 |
| `frontend/stats.html` | "내 레벨" 박스 추가 (레벨 배지 + 진행률 바 + 레벨업 히스토리), `renderLevel()` / `tierClassOf()` 추가 |
| `frontend/stats.css` | `.level-badge`, `.level-progress-wrap`, `.levelup-history` 등 스타일 추가 (기존 `--bronze`/`--silver`/... CSS 변수 재사용) |

## API

```
GET /api/stats/level

{
  "level": 11,
  "label": "Gold V",
  "class": "gold",
  "exp": 12472.7,
  "cur_threshold": 12039.3,
  "next_threshold": 14964.9,
  "progress_pct": 14.8,
  "level_up_history": [
    { "level": 11, "label": "Gold V", "at": "2026-08-21T...", "problem_id": 11003 },
    ...
  ]
}
```

## 테스트

- `python -c "from server.db import get_conn, get_user_level; ..."` 로 실제 DB에 대해 직접 계산 → Level 11 / Gold V / 진행률 14.8% (풀이 이력상 자연스러운 값인지 눈으로 확인)
- 로컬 서버 기동 후 `curl /api/stats/level` 응답 확인
- Chrome으로 `/stats` 페이지 접속해 레벨 배지·진행률 바·레벨업 히스토리·기존 히트맵/태그/최근풀이 섹션이 모두 정상 렌더링되는지 확인 (회귀 없음)

## 구현 중 이슈 및 해결

### 1. `/stats.html`로 접속 시 404

- **증상**: 테스트하려고 `http://localhost:8000/stats.html`로 접속했더니 `{"detail":"Not Found"}`
- **원인**: `server/main.py`에 등록된 라우트는 `/stats`이지 `/stats.html`이 아님 (`frontend/stats.html`은 `FileResponse`로 서빙되는 정적 파일이 아니라 `@app.get("/stats")` 핸들러가 반환하는 파일)
- **해결**: `/stats`로 접속

### 2. 새 CSS/JS가 반영 안 됨 (브라우저 캐시)

- **증상**: `stats.html`/`stats.css`를 수정하고 서버 재시작 후 접속했는데 레벨 배지 박스가 스타일 없이(배경/테두리 없이, 좌측 정렬로) 깨져서 렌더링됨
- **원인**: Chrome이 이전 버전의 정적 파일(css)을 캐시해서 새 스타일이 적용 안 됨 (이전 세션에서도 한 번 겪었던 동일 패턴)
- **해결**: `Ctrl+Shift+R` 하드 리프레시 → 정상 렌더링 확인

## 향후 확장 아이디어 (미구현)

- ~~`index.html` 헤더에 작은 레벨 배지 상시 표시~~ → 2026-08-22, `docs/housekeeping-fixes.md` 참고해 구현 완료
- 레벨업 시 토스트/애니메이션 연출
- EXP 공식 상수를 설정 파일로 분리해 사용자가 직접 튜닝 가능하게
