from pydantic import BaseModel
from typing import Any


class ProblemSummary(BaseModel):
    id: int
    title: str
    level: int
    tags: list[str]
    time_limit: str
    memory_limit: str
    accepted_user_count: int | None
    solved: int = 0


class Sample(BaseModel):
    input: str
    output: str


class ProblemDetail(ProblemSummary):
    description: str
    input_desc: str
    output_desc: str
    samples: list[Sample]
    average_tries: float | None
    solved_at: str | None = None


class ProblemListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: list[ProblemSummary]


class RunRequest(BaseModel):
    code: str
    stdin: str = ""
    time_limit: str = "5 초"  # 원본 time_limit 문자열


class RunResponse(BaseModel):
    status: str          # "OK" | "TLE" | "ERROR"
    stdout: str
    stderr: str
    elapsed_ms: float | None
    time_limit_ms: float  # Python 환산 제한 (원본 × 3)
    raw_time_limit: str   # 원본 문자열 (표시용)
