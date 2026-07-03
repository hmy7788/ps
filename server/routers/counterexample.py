import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api")

TESTCASE_AC_BASE = "https://api.testcase.ac"


class FindCounterexampleRequest(BaseModel):
    code: str


@router.post("/problems/{problem_id}/find-counterexample")
async def find_counterexample(problem_id: int, req: FindCounterexampleRequest):
    async with httpx.AsyncClient(timeout=15) as client:
        try:
            detail_res = await client.get(
                f"{TESTCASE_AC_BASE}/api/problems/boj/{problem_id}"
            )
        except httpx.RequestError as e:
            raise HTTPException(502, f"testcase.ac 연결 실패: {e}")

        if detail_res.status_code == 404:
            return {"registered": False}
        if detail_res.status_code != 200:
            raise HTTPException(502, f"testcase.ac 오류: {detail_res.status_code}")

        detail = detail_res.json()
        has_generators = bool(detail.get("generators") or detail.get("testcases") or detail.get("singlegens"))
        if not detail.get("correctCodes") or not has_generators:
            return {"registered": False}

        try:
            stress_res = await client.post(
                f"{TESTCASE_AC_BASE}/api/problems/boj/{problem_id}/stress",
                json={"targetCode": req.code, "targetCodeLang": "python3"},
                timeout=100,
            )
        except httpx.RequestError as e:
            raise HTTPException(502, f"testcase.ac 연결 실패: {e}")

    if stress_res.status_code == 429:
        raise HTTPException(429, "testcase.ac 요청 한도를 초과했습니다. 잠시 후 다시 시도하세요.")
    if stress_res.status_code != 200:
        detail_msg = stress_res.json().get("detail", stress_res.text) if stress_res.headers.get("content-type", "").startswith("application/json") else stress_res.text
        raise HTTPException(502, f"testcase.ac 오류: {detail_msg}")

    return {"registered": True, **stress_res.json()}
