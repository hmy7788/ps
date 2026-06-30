import re


def parse_time_limit(raw: str) -> float:
    """'2 초', '1.5초', '3000ms' 등을 초(float)로 변환. 파싱 실패 시 5.0 반환."""
    if not raw:
        return 5.0
    raw_lower = raw.lower()
    match = re.search(r"[\d.]+", raw_lower)
    if not match:
        return 5.0
    value = float(match.group())
    if "ms" in raw_lower:
        return value / 1000
    return value  # 초 단위
