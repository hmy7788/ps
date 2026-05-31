# 이분탐색 (Binary Search)

**언제 씀**: 정렬된 배열, "최솟값/최댓값을 구하라"는 힌트, 파라메트릭 서치  
**시간복잡도**: O(log N)

---

## 핵심 패턴

```
"최소/최대를 구하라" → 답을 이분탐색으로 설정 후 조건 검사 (파라메트릭)
left, right = 0, max_value
while left <= right:
    mid = (left + right) // 2
    if 조건(mid): right = mid - 1  # 더 작은 값 탐색
    else:         left  = mid + 1

bisect_left(arr, x)   # x 이상인 첫 인덱스
bisect_right(arr, x)  # x 초과인 첫 인덱스
```

---

## 추천 문제

### ✅ 푼 문제
- [x] 입국심사 (Lv.3) — 파라메트릭 서치

### ⬜ 풀어야 할 문제
- [ ] 예산 (Lv.3)
- [ ] 징검다리 건너기 (Lv.3)
