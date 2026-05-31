# 링크드 리스트 (Linked List)

**언제 씀**: 삽입/삭제가 빈번할 때, 순서 유지가 중요할 때  
**시간복잡도**: 접근 O(N), 삽입/삭제 O(1) (노드 위치 알 때)

---

## 핵심 패턴

```python
# Python에서는 직접 구현보다 deque 사용이 일반적
from collections import deque
dq = deque([1, 2, 3])
dq.appendleft(0)   # 앞 삽입 O(1)
dq.popleft()       # 앞 삭제 O(1)
dq.append(4)       # 뒤 삽입 O(1)
dq.pop()           # 뒤 삭제 O(1)

# 직접 구현 (단방향)
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
```

---

## 추천 문제

### ✅ 푼 문제
- 없음

### ⬜ 풀어야 할 문제
- [ ] 요격 시스템 (Lv.2)
- [ ] 주차 요금 계산 (Lv.2)
