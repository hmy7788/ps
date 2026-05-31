# 유니온 파인드 (Union-Find / Disjoint Set)

**언제 씀**: 연결 여부 확인, 사이클 감지, 그룹 분류  
**시간복잡도**: O(α(N)) — 사실상 O(1)

---

## 핵심 패턴

```python
def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])  # 경로 압축
    return parent[x]

def union(parent, a, b):
    a, b = find(parent, a), find(parent, b)
    if a != b:
        parent[b] = a

# 초기화
n = 5
parent = list(range(n + 1))  # [0, 1, 2, 3, 4, 5]

# 연결 여부 확인
find(parent, 1) == find(parent, 3)  # True → 같은 그룹
```

---

## 추천 문제

### ✅ 푼 문제
- 없음

### ⬜ 풀어야 할 문제
- [ ] 섬 연결하기 (Lv.3)
- [ ] 순위 (Lv.3)
