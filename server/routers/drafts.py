import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api")

DRAFTS_DIR = Path(__file__).resolve().parent.parent.parent / "drafts"
DRAFTS_DIR.mkdir(exist_ok=True)


def _draft_path(problem_id: int) -> Path:
    return DRAFTS_DIR / f"{problem_id}.json"


def list_draft_ids() -> set[int]:
    """드래프트가 남아있는 problem_id 집합 (풀고 있는 문제 필터용)."""
    return {int(p.stem) for p in DRAFTS_DIR.glob("*.json") if p.stem.isdigit()}


class DraftRequest(BaseModel):
    code: str


@router.get("/problems/{problem_id}/draft")
def get_draft(problem_id: int):
    p = _draft_path(problem_id)
    if not p.exists():
        return {"exists": False}
    return {"exists": True, **json.loads(p.read_text(encoding="utf-8"))}


@router.post("/problems/{problem_id}/draft")
def save_draft(problem_id: int, req: DraftRequest):
    data = {
        "code": req.code,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    _draft_path(problem_id).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return {"saved": True, "updated_at": data["updated_at"]}


@router.delete("/problems/{problem_id}/draft")
def delete_draft(problem_id: int):
    _draft_path(problem_id).unlink(missing_ok=True)
    return {"deleted": True}
