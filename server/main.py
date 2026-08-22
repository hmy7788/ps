import os
import threading
import time
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from server.db import get_conn, sync_solved_from_fs
from server.routers.problems import router as problems_router
from server.routers.run import router as run_router
from server.routers.testcases import router as testcases_router
from server.routers.solutions import router as solutions_router
from server.routers.counterexample import router as counterexample_router
from server.routers.drafts import router as drafts_router
from server.routers.custom_problems import router as custom_problems_router

ROOT = Path(__file__).resolve().parent.parent

app = FastAPI(title="PS Platform", version="0.1.0")


_last_heartbeat: float | None = None
_leaving_since: float | None = None
_active_requests: int = 0
_LEAVING_GRACE = 8          # 초 - pagehide 신호 후 이 시간 내에 새 heartbeat가 없으면 진짜로 닫힌 것으로 판단
_SAFETY_TIMEOUT = 30 * 60   # 초 - pagehide 신호 자체가 안 온 경우(강제종료 등) 대비 최후 안전장치


@app.post("/api/heartbeat")
def heartbeat():
    global _last_heartbeat, _leaving_since
    _last_heartbeat = time.time()
    _leaving_since = None  # 새 페이지가 떴다는 뜻이므로 종료 예약 취소 (같은 사이트 내 이동 케이스)
    return {"ok": True}


@app.post("/api/heartbeat/leaving")
def heartbeat_leaving():
    global _leaving_since
    _leaving_since = time.time()
    return {"ok": True}


@app.middleware("http")
async def track_requests(request, call_next):
    global _active_requests
    _active_requests += 1
    try:
        return await call_next(request)
    finally:
        _active_requests -= 1


def _watchdog():
    time.sleep(30)  # 첫 연결 대기
    while True:
        time.sleep(1)
        if _active_requests > 0:
            continue  # 요청 처리 중이면 카운트 안 함
        now = time.time()
        if _leaving_since and now - _leaving_since > _LEAVING_GRACE:
            print("[watchdog] 브라우저 탭 종료 감지 - 서버 종료")
            os._exit(0)
        if _last_heartbeat and now - _last_heartbeat > _SAFETY_TIMEOUT:
            print("[watchdog] 하트비트 장시간 없음(안전장치) - 서버 종료")
            os._exit(0)


@app.on_event("startup")
def startup_sync():
    conn = get_conn()
    n = sync_solved_from_fs(conn, ROOT)
    if n:
        print(f"[sync] {n}개 문제 solved 동기화 완료")
    conn.close()
    t = threading.Thread(target=_watchdog, daemon=True)
    t.start()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(problems_router)
app.include_router(run_router)
app.include_router(testcases_router)
app.include_router(solutions_router)
app.include_router(counterexample_router)
app.include_router(drafts_router)
app.include_router(custom_problems_router)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/", response_class=FileResponse)
    def index():
        return str(FRONTEND_DIR / "index.html")

    @app.get("/problem", response_class=FileResponse)
    def problem():
        return str(FRONTEND_DIR / "problem.html")

    @app.get("/stats", response_class=FileResponse)
    def stats_page():
        return str(FRONTEND_DIR / "stats.html")

    @app.get("/create", response_class=FileResponse)
    def create_page():
        return str(FRONTEND_DIR / "create.html")
