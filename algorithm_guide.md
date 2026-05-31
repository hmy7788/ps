# 🧠 코딩테스트 알고리즘 & 자료구조 완벽 정리

---

## 📦 자료구조 (Data Structure)

### 1. 배열 (Array)
- **특징**: 인덱스로 빠른 접근 O(1), 삽입/삭제 느림 O(n)
- **언제 씀**: 순서 있는 데이터 저장, 인덱스 접근 필요할 때
- **파이썬**: `list`

```python
arr = [1, 2, 3, 4, 5]
arr[0]        # 접근 O(1)
arr.append(6) # 끝에 삽입 O(1)
arr.insert(2, 10) # 중간 삽입 O(n)
```

---

### 2. 스택 (Stack)
- **특징**: 후입선출 (LIFO)
- **언제 씀**: 괄호 검사, 뒤로가기, 수식 계산, DFS
- **파이썬**: `list` (append/pop)

```python
stack = []
stack.append(1)  # push
stack.append(2)
stack.pop()      # pop → 2 (마지막 원소)
```

**대표 문제 유형**
- 올바른 괄호
- 주식 가격
- 탑

---

### 3. 큐 (Queue)
- **특징**: 선입선출 (FIFO)
- **언제 씀**: BFS, 순서대로 처리
- **파이썬**: `collections.deque` (list보다 빠름)

```python
from collections import deque
queue = deque()
queue.append(1)   # enqueue
queue.append(2)
queue.popleft()   # dequeue → 1 (첫 번째 원소)
```

**⚠️ 주의**: `list.pop(0)`은 O(n), `deque.popleft()`는 O(1)

---

### 4. 해시 (Hash)
- **특징**: key-value 저장, 탐색/삽입/삭제 평균 O(1)
- **언제 씀**: 빠른 탐색, 중복 제거, 카운팅
- **파이썬**: `dict`, `set`, `collections.Counter`

```python
# dict
d = {}
d['apple'] = 3
d.get('banana', 0)  # 없으면 기본값 0

# Counter (카운팅에 유용)
from collections import Counter
c = Counter([1, 1, 2, 3, 3, 3])
# Counter({3: 3, 1: 2, 2: 1})

# set (중복 제거)
s = set([1, 1, 2, 3])
# {1, 2, 3}
```

**대표 문제 유형**
- 전화번호 목록
- 위장
- 베스트앨범

---

### 5. 힙 (Heap)
- **특징**: 최솟값/최댓값을 O(log n)으로 꺼내기
- **언제 씀**: 우선순위 큐, 다익스트라, K번째 최솟값
- **파이썬**: `heapq` (기본이 최소 힙)

```python
import heapq

# 최소 힙
heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)
heapq.heappop(heap)  # → 1 (최솟값)

# 최대 힙 (음수로 변환)
heapq.heappush(heap, -3)
-heapq.heappop(heap)  # → 3 (최댓값)
```

---

### 6. 트리 (Tree)
- **특징**: 계층적 자료구조, 사이클 없음
- **언제 씀**: 계층 구조 표현, 탐색

```
       1
      / \
     2   3
    / \
   4   5
```

**이진 탐색 트리 (BST)**
- 왼쪽 < 부모 < 오른쪽
- 탐색 평균 O(log n)

---

### 7. 그래프 (Graph)
- **특징**: 노드(정점) + 간선으로 구성
- **표현 방법**: 인접 리스트, 인접 행렬

```python
# 인접 리스트 (일반적으로 더 효율적)
graph = {
    1: [2, 3],
    2: [1, 4],
    3: [1],
    4: [2]
}

# 인접 행렬 (노드 수 적을 때)
n = 5
graph = [[0] * n for _ in range(n)]
graph[0][1] = 1  # 0 → 1 연결
```

---

## 🔍 알고리즘 (Algorithm)

### 1. BFS (너비 우선 탐색)
- **핵심**: deque + visited 배열
- **언제 씀**: **최단거리** (장애물 있는 격자), 레벨 탐색
- **시간복잡도**: O(V + E)

```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        print(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

**격자 BFS 템플릿**
```python
from collections import deque

def bfs(grid, start_r, start_c):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    queue = deque([(start_r, start_c, 0)])  # (행, 열, 거리)
    visited[start_r][start_c] = True
    
    dr = [-1, 1, 0, 0]  # 상하좌우
    dc = [0, 0, -1, 1]
    
    while queue:
        r, c, dist = queue.popleft()
        
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                visited[nr][nc] = True
                queue.append((nr, nc, dist + 1))
```

**⚠️ 핵심 포인트**
- 장애물 있음 → BFS 필수
- 장애물 없음 → 맨해튼 거리로 대체 가능!

---

### 2. DFS (깊이 우선 탐색)
- **핵심**: 재귀 or 스택
- **언제 씀**: 경우의 수, 조합, 백트래킹
- **주의**: `sys.setrecursionlimit` 설정

```python
import sys
sys.setrecursionlimit(10000)

def dfs(graph, node, visited):
    visited.add(node)
    print(node)
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

**백트래킹 템플릿**
```python
def backtrack(current, choices):
    if 종료_조건:
        결과_저장()
        return
    
    for choice in choices:
        if 유효한_선택:
            선택(choice)
            backtrack(current + [choice], choices)
            취소(choice)  # 백트래킹
```

---

### 3. 이분탐색 (Binary Search)
- **핵심**: left, right, mid 포인터
- **언제 씀**: 정렬된 배열에서 빠른 탐색
- **시간복잡도**: O(log n)
- **힌트**: "최솟값/최댓값을 구하라" → 이분탐색

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# 파이썬 내장
import bisect
bisect.bisect_left(arr, target)   # target 이상인 첫 번째 인덱스
bisect.bisect_right(arr, target)  # target 초과인 첫 번째 인덱스
```

---

### 4. 완전탐색

#### 순열 (Permutation)
- **언제 씀**: 순서가 중요한 경우, 여러 목적지 최소거리
- **주의**: N! → N ≤ 10일 때만 가능

```python
from itertools import permutations

arr = [1, 2, 3]
for perm in permutations(arr):
    print(perm)  # (1,2,3), (1,3,2), (2,1,3) ...
```

#### 조합 (Combination)
- **언제 씀**: 순서 상관없이 N개 중 K개 선택

```python
from itertools import combinations

arr = [1, 2, 3, 4]
for comb in combinations(arr, 2):
    print(comb)  # (1,2), (1,3), (1,4), (2,3) ...
```

#### 부분집합 (Subset)
```python
from itertools import combinations

arr = [1, 2, 3]
for r in range(len(arr) + 1):
    for subset in combinations(arr, r):
        print(subset)
```

---

### 5. 정렬 (Sort)
- **파이썬 기본**: Tim Sort O(n log n)

```python
arr = [3, 1, 4, 1, 5]

# 기본 정렬
arr.sort()           # 오름차순
arr.sort(reverse=True)  # 내림차순

# key 사용
arr.sort(key=lambda x: x[1])       # 두 번째 원소 기준
arr.sort(key=lambda x: (-x[1], x[0]))  # 두 번째 내림차순, 첫 번째 오름차순
```

---

### 6. 그리디 (Greedy)
- **언제 씀**: 현재 최선 = 전체 최선일 때
- **주의**: 항상 최적해 보장 안 함, 반례 확인 필수

```python
# 회의실 배정 예시
meetings = [(1,4), (3,5), (0,6), (5,7), (3,8)]
meetings.sort(key=lambda x: x[1])  # 종료 시간 기준 정렬

count = 0
end_time = 0
for start, end in meetings:
    if start >= end_time:
        count += 1
        end_time = end
```

---

### 7. 동적 프로그래밍 (DP)
- **언제 씀**: 큰 문제 → 작은 문제, 같은 계산 반복
- **핵심**: 점화식 세우기

```python
# 피보나치 (메모이제이션)
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

# 계단 오르기 (Bottom-up)
def stairs(n):
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

---

### 8. 다익스트라 (Dijkstra)
- **언제 씀**: 가중치 있는 그래프 최단경로
- **주의**: 음수 간선 사용 불가
- **시간복잡도**: O((V + E) log V)

```python
import heapq

def dijkstra(graph, start, n):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    heap = [(0, start)]  # (거리, 노드)
    
    while heap:
        d, node = heapq.heappop(heap)
        
        if d > dist[node]:
            continue
        
        for neighbor, weight in graph[node]:
            new_dist = dist[node] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    
    return dist
```

---

### 9. 유니온 파인드 (Union-Find)
- **언제 씀**: 연결 여부 확인, 사이클 감지, 그룹 분류

```python
def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])  # 경로 압축
    return parent[x]

def union(parent, a, b):
    a = find(parent, a)
    b = find(parent, b)
    if a != b:
        parent[b] = a

# 사용법
n = 5
parent = list(range(n + 1))  # [0, 1, 2, 3, 4, 5]
union(parent, 1, 2)
union(parent, 2, 3)
find(parent, 1) == find(parent, 3)  # True → 연결됨
```

---

### 10. 위상정렬 (Topological Sort)
- **언제 씀**: 순서가 있는 작업 처리 (선수과목, 작업 순서)
- **조건**: DAG (방향 비순환 그래프)

```python
from collections import deque

def topological_sort(n, graph, in_degree):
    queue = deque([i for i in range(1, n+1) if in_degree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return result
```

---

## 📐 자주 쓰는 수학 공식

```python
# 소수 판별 O(√n)
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

# 에라토스테네스의 체 (여러 소수 한 번에)
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    return [i for i in range(2, n+1) if is_prime[i]]

# GCD / LCM
from math import gcd
lcm = lambda a, b: a * b // gcd(a, b)

# 맨해튼 거리 (장애물 없는 격자)
dist = abs(x1 - x2) + abs(y1 - y2)
```

---

## 📊 시간복잡도 & 우선순위 정리

| 우선순위 | 알고리즘/자료구조 | 시간복잡도 | 코테 빈도 |
|---------|-----------------|-----------|---------|
| ⭐⭐⭐ | BFS/DFS | O(V+E) | 매우 높음 |
| ⭐⭐⭐ | 해시 | O(1) | 매우 높음 |
| ⭐⭐⭐ | 완전탐색 (순열/조합) | O(N!) | 높음 |
| ⭐⭐ | 정렬 | O(N log N) | 높음 |
| ⭐⭐ | 이분탐색 | O(log N) | 높음 |
| ⭐⭐ | 그리디 | O(N log N) | 중간 |
| ⭐⭐ | DP | O(N²) | 중간 |
| ⭐ | 다익스트라 | O((V+E) log V) | 낮음 |
| ⭐ | 유니온 파인드 | O(α(N)) | 낮음 |
| ⭐ | 위상정렬 | O(V+E) | 낮음 |

---

## 💡 코테 꿀팁

```
격자 맵 + 장애물 있음    → BFS
격자 맵 + 장애물 없음    → 맨해튼 거리
여러 목적지 최소거리      → 순열 완탐 + 맨해튼 거리
"최솟값/최댓값을 구하라"  → 이분탐색 의심
목적지 10개 이하         → 순열 완탐 가능
목적지 20개 이하         → DP + 비트마스킹
목적지 100개 이상        → 근사 알고리즘 (TSP)
연결 여부 확인           → 유니온 파인드
순서 있는 작업           → 위상정렬
현재 최선 = 전체 최선    → 그리디
```