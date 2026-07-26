@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ================================
echo   PS Platform 초기 설정
echo ================================
echo.

:: Python 확인 (python → py 순서로 시도)
set PYTHON_CMD=
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
) else (
    py --version >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=py
    )
)
if "%PYTHON_CMD%"=="" (
    echo [오류] Python이 설치되어 있지 않거나 PATH에 없습니다.
    echo https://www.python.org 에서 설치 후 다시 실행하세요.
    echo [팁] 설치 시 "Add Python to PATH" 옵션을 반드시 체크하세요.
    pause
    exit /b 1
)
echo [확인] Python 발견: %PYTHON_CMD%

:: 가상환경 생성
if not exist ".venv" (
    echo [1/4] 가상환경 생성 중...
    %PYTHON_CMD% -m venv .venv
) else (
    echo [1/4] 가상환경이 이미 존재합니다. 건너뜁니다.
)

:: 패키지 설치
echo [2/4] 패키지 설치 중...
call .venv\Scripts\activate.bat
pip install fastapi uvicorn python-dotenv anthropic --quiet

:: .env 파일 생성
if not exist ".env" (
    echo [3/4] .env 파일 생성 중...
    echo ANTHROPIC_API_KEY=여기에_API_키_입력 > .env
    echo.
    echo  ** .env 파일이 생성됐습니다.
    echo  ** 메모장으로 .env 파일을 열어 API 키를 입력하세요.
    echo.
) else (
    echo [3/4] .env 파일이 이미 존재합니다. 건너뜁니다.
)

:: all_problems 확인 후 DB 빌드
if not exist "all_problems\problems" (
    echo [4/4] all_problems 폴더가 없습니다.
    echo       USB 또는 드라이브에서 all_problems 폴더를 이 경로에 복사 후
    echo       setup.bat을 다시 실행하세요.
    echo       경로: %~dp0all_problems
) else (
    echo [4/4] DB 인덱스 빌드 중... (수 분 소요)
    %PYTHON_CMD% scripts/build_index.py
    echo.
    echo  ** DB 빌드 완료!
)

echo.
echo ================================
echo   설정 완료! create_shortcut.vbs를
echo   더블클릭해서 바로가기를 만드세요.
echo ================================
echo.
pause
