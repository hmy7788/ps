from collections import deque
import copy

def bfs(g, n, start_node):
        v = [0 for _ in range(n+1)]
        v[start_node] = 1
        cnt = 1
        dq = deque()
        dq.append(g[start_node])
        
        while dq:
            nodes = dq.popleft()
            
            for neighbor in nodes:
                if v[neighbor] == 0:
                    v[neighbor] = 1
                    dq.append(g[neighbor])
                    cnt += 1

        return cnt

def solution(n, wires):
    
    G = {i: [] for i in range(1, n+1)}
    
    for edge in wires:
        n1, n2 = edge[0], edge[1]
        G[n1].append(n2)
        G[n2].append(n1)
        
    min_diff = float('inf')
    for edge in wires:
        v1, v2 = edge[0], edge[1]
        # g = copy.deepcopy(G)    # deepcopy를 쓰면 느려진대
        G[v1].remove(v2)
        G[v2].remove(v1)
        
        nw1_cnt = bfs(G, n, v1)
        nw2_cnt = n - nw1_cnt
        diff = abs(nw1_cnt - nw2_cnt)
        
        G[v1].append(v2)
        G[v2].append(v1)
        
        if diff == 0: return 0
        if min_diff > diff: min_diff = diff
            
    return min_diff