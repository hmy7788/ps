# 코드 실행 에러 메시지가 "서버 오류"로 뭉개지는 버그 수정

브랜치: `fix/subprocess-stderr-encoding`

## 증상

`/api/run`으로 틀린 코드(`IndexError`, `NameError` 등)를 돌리면 실제 에러 메시지 대신
브라우저에 이런 게 떴다:

```
서버 오류: Unexpected token 'I', "Internal S"... is not valid JSON
```

실제 원인(`IndexError` 등)은 전혀 안 보이고, 사용자 입장에선 "왜 틀렸는지" 알 방법이 없었음.

## 재현

```python
l = [1]
print(l[1])
```
이 코드를 `/api/run`에 넣으면 서버가 200이 아니라 **500 Internal Server Error**(평문 텍스트)를
돌려줬다. `problem.html`의 `runOne()`은 응답이 항상 JSON일 거라 가정하고 `res.json()`을
호출하는데, 평문 "Internal Server Error"를 JSON으로 파싱하려다 실패 → 그 파싱 에러 메시지가
그대로 화면에 뜬 것. 즉 사용자가 본 메시지는 "IndexError가 났다"는 정보가 아니라
"서버 응답을 못 읽었다"는 완전히 다른 종류의 실패였다.

## 근본 원인

1. `server/routers/run.py`, `server/utils.py`가 사용자 코드를 `subprocess.run([PYTHON, tmp_path], ..., encoding="utf-8")`으로 실행하고 자식 프로세스의 stdout/stderr를 **엄격하게(strict)** UTF-8로 디코딩하고 있었다.
2. 하지만 Windows에서 자식 파이썬 프로세스는 (별도 설정이 없으면) 콘솔 기본 코드페이지 — 이 환경에선 cp949 — 로 표준출력/에러를 인코딩해서 내보낸다.
3. 코드가 에러를 내면 트레이스백 첫 줄에 **임시 스크립트의 절대경로**가 찍히는데, 이 컴퓨터의 Windows 계정명이 한글(`한국전파진흥협회`)이라 그 경로 문자열 자체가 cp949로 인코딩된 상태로 나온다.
4. 부모 프로세스(FastAPI 서버)가 이걸 UTF-8로 엄격 디코딩하려다 `UnicodeDecodeError`가 **`subprocess`의 백그라운드 reader 스레드 안에서** 발생 → 예외가 조용히 삼켜지고 `result.stderr`가 `None`으로 돌아옴.
5. `RunResponse.stderr: str` (Pydantic)이 `None`을 거부 → `ValidationError` → FastAPI가 처리 못 하고 500 반환.

정리하면: **`IndexError`가 났다는 사실 자체는 정상적으로 감지됐는데, 그 에러 메시지를 부모 프로세스가 읽어오는 단계에서 인코딩 문제로 통째로 유실된 것.** 임시파일 경로에 한글이 섞이는 이 환경에서는 사실상 모든 런타임 에러에서 재현되는 문제였다.

## 이미 한 번 겪었던 문제

`harness` 브랜치(`main`엔 미병합, 별도 실행 하네스 리팩터링 작업)에서 정확히 같은 버그를
먼저 겪고 문서화해뒀다: `docs/failures/002-isolated-mode-ignores-pythonioencoding.md`.
거기서 검증된 해결책을 그대로 가져와 적용했다.

## 해결

`server/routers/run.py`, `server/utils.py` 두 곳의 `subprocess.run` 호출에:

1. **`-X utf8`** 플래그를 자식 프로세스 커맨드에 추가 — Python을 UTF-8 모드로 강제 실행해서, 로케일/콘솔 코드페이지와 무관하게 자식 프로세스 자신도 UTF-8로 출력하게 만든다.
   ```python
   subprocess.run([PYTHON, "-X", "utf8", str(tmp_path)], ...)
   ```
2. **`errors="replace"`** 를 디코딩 옵션에 추가 — `-X utf8`을 거쳐도 100% 신뢰하지 않고, 혹시 디코딩 안 되는 바이트가 남아있어도 예외 대신 대체문자(`�`)로 채워서 절대 크래시하지 않게 하는 안전망.
   ```python
   subprocess.run(..., text=True, encoding="utf-8", errors="replace", ...)
   ```

## 검증

- `curl`로 직접 `/api/run` 호출: `IndexError`/`NameError` 코드 모두 200 OK + 정상적인 트레이스백 문자열 확인 (수정 전엔 500이었음).
- 한글을 출력하고 나서 에러가 나는 코드(`print("안녕"); print(l[1])`)도 `stdout`/`stderr` 둘 다 깨지지 않고 정상 디코딩됨을 확인.
- 실제 Chrome 브라우저로 `/problem?id=1074`에서 에디터에 위 재현 코드를 넣고 "실행" → 화면에 `IndexError: list index out of range` 트레이스백이 정상적으로 표시되는 것 확인 (이전엔 "서버 오류: ... is not valid JSON"만 떴음).

## 남아있는 개선 여지 (미구현)

- 트레이스백에 찍히는 임시파일 절대경로(`C:\Users\한국전~1\AppData\Local\Temp\tmpXXXX.py`)는 사용자에게 의미 없는 정보 — `harness`의 `_clean_traceback_paths()`처럼 파일명만 남기고 정리하면 더 깔끔해짐.
- `/api/problems/{id}/submit`(채점) 경로도 내부적으로 `server/utils.py::run_one`을 공유하므로 이번 수정으로 같이 고쳐졌지만, 별도로 다시 검증하진 않음.
