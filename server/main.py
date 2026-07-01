from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from server.routers.problems import router as problems_router
from server.routers.run import router as run_router
from server.routers.testcases import router as testcases_router
from server.routers.solutions import router as solutions_router

app = FastAPI(title="PS Platform", version="0.1.0")

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

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/", response_class=FileResponse)
    def index():
        return str(FRONTEND_DIR / "index.html")

    @app.get("/problem", response_class=FileResponse)
    def problem():
        return str(FRONTEND_DIR / "problem.html")
