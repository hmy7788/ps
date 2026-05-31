# 다익스트라 (Dijkstra)

**언제 씀**: 가중치 있는 그래프에서 단일 출발점 최단경로  
**시간복잡도**: O((V + E) log V)  
**주의**: 음수 간선 사용 불가

---

## 핵심 패턴

```python
import heapq

def dijkstra(graph, start, n):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    heap = [(0, start)]  # (거리, 노드)

    while heap:
        d, node = heapq.heappop(heap)

        if d > dist[node]:  # 이미 더 짧은 경로 있으면 스킵
            continue

        for neighbor, weight in graph[node]:
            new_dist = dist[node] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return dist
```

---

## 추천 문제

### ✅ 푼 문제
- 없음

### ⬜ 풀어야 할 문제
- [ ] 합승 택시 요금 (Lv.3)
- [ ] 배달 (Lv.2)
