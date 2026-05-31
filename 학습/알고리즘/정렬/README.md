# 정렬 (Sort)

**언제 씀**: 순서 기준 처리, 이분탐색 전처리, 그리디 기반  
**시간복잡도**: Python Tim Sort O(N log N)

---

## 핵심 패턴

```python
arr.sort()                              # 오름차순
arr.sort(reverse=True)                  # 내림차순
arr.sort(key=lambda x: x[1])           # 두 번째 원소 기준
arr.sort(key=lambda x: (-x[1], x[0])) # 복합 기준 (내림, 오름)

# 문자열 정렬 주의: "10" < "9" (사전순)
# 숫자처럼 정렬하려면 int 변환 또는 key=int
```

---

## 추천 문제

### ✅ 푼 문제
- [x] K번째수 (Lv.1)
- [x] 가장 큰 수 (Lv.2) — 커스텀 정렬

### ⬜ 풀어야 할 문제
- [ ] H-Index (Lv.2)
