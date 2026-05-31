# 힙 (Heap / 우선순위 큐)

**언제 씀**: 최솟값/최댓값을 반복해서 꺼낼 때, K번째 값, 다익스트라  
**시간복잡도**: push/pop O(log N)

---

## 핵심 패턴

```
import heapq
heapq.heappush(heap, val)   # 최소 힙
heapq.heappop(heap)

# 최대 힙 → 값을 음수로 넣고 꺼낼 때 음수로 변환
heapq.heappush(heap, -val)
-heapq.heappop(heap)

# (우선순위, 값) 튜플로 넣으면 우선순위 기준 정렬
heapq.heappush(heap, (priority, val))
```

---

## 추천 문제

### ✅ 푼 문제
- [x] 더 맵게 (Lv.2)

### ⬜ 풀어야 할 문제
- [ ] 디스크 컨트롤러 (Lv.3)
- [ ] 이중우선순위큐 (Lv.3)
