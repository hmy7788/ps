# 위상정렬 (Topological Sort)

**언제 씀**: 순서가 있는 작업 처리 (선수과목, 작업 순서, 의존관계)  
**조건**: DAG (방향 비순환 그래프)  
**시간복잡도**: O(V + E)

---

## 핵심 패턴

```python
from collections import deque

def topological_sort(n, graph, in_degree):
    # in_degree[i]: 노드 i로 들어오는 간선 수
    queue = deque([i for i in range(1, n + 1) if in_degree[i] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # len(result) != n 이면 사이클 존재
    return result
```

---

## 추천 문제

### ✅ 푼 문제
- 없음

### ⬜ 풀어야 할 문제
- [ ] 선입 선출 스케줄링 (Lv.3)
- [ ] 동굴 탐험 (Lv.3)
