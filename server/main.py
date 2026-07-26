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

ROOT = Path(__file__).resolve().parent.parent

app = FastAPI(title="PS Platform", version="0.1.0")


_last_heartbeat: float | None = None
_active_requests: int = 0
_HEARTBEAT_TIMEOUT = 30  # 초


@app.post("/api/heartbeat")
def heartbeat():
    global _last_heartbeat
    _last_heartbeat = time.time()
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
        time.sleep(5)
        if _active_requests > 0:
            continue  # 요청 처리 중이면 카운트 안 함
        if _last_heartbeat and time.time() - _last_heartbeat > _HEARTBEAT_TIMEOUT:
            print("[watchdog] 브라우저 연결 끊김 - 서버 종료")
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
