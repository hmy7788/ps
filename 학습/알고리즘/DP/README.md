# 동적 프로그래밍 (DP)

**언제 씀**: 큰 문제를 작은 문제로 분할, 같은 계산이 반복될 때  
**시간복잡도**: 문제마다 다름 (보통 O(N²) 이하)

---

## 핵심 패턴

```
1. 점화식 세우기: dp[i] = f(dp[i-1], dp[i-2], ...)
2. 초기값 설정: dp[0], dp[1]
3. Bottom-up (반복문) 또는 Top-down (재귀 + 메모이제이션)

# Top-down (메모이제이션)
from functools import lru_cache
@lru_cache(maxsize=None)
def dp(n): ...

# Bottom-up
dp = [0] * (n + 1)
dp[0], dp[1] = ...
for i in range(2, n + 1):
    dp[i] = dp[i-1] + dp[i-2]
```

---

## 추천 문제

### ✅ 푼 문제
- 없음 (DP 문제 아직 미경험)

### ⬜ 풀어야 할 문제
- [ ] 정수 삼각형 (Lv.3) ← 시작하기 좋은 문제
- [ ] 등굣길 (Lv.3)
- [ ] N으로 표현 (Lv.3)
