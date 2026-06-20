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
            
            for n in nodes:
                if v[n] == 0:
                    v[n] = 1
                    dq.append(g[n])
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
        node1, node2 = edge[0], edge[1]
        g = copy.deepcopy(G)
        g[node1].remove(node2)
        g[node2].remove(node1)
        
        nw1_cnt = bfs(g, n, node1)
        nw2_cnt = bfs(g, n, node2)
        diff = abs(nw1_cnt - nw2_cnt)
        
        if diff == 0: return 0
        if min_diff > diff: min_diff = diff
            
    return min_diff