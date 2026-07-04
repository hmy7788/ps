from collections import deque

def bfs(G):
    v = [0 for _ in range(len(G)+1)]
    v[1] = 1
    dq = deque()
    dq.append([1, G[1]])
    while dq:
        info = dq.popleft()
        start_node, end_nodes = info[0], info[1]
        
        for end_node in end_nodes:
            if v[end_node] == 0:
                v[end_node] = v[start_node] + 1
                dq.append([end_node, G[end_node]])
    return v


def solution(n, edge):
    G = {i: [] for i in range(1, n+1)}
    
    for e in edge:
        n1, n2 = e[0], e[1]
        G[n1].append(n2)
        G[n2].append(n1)
        
    v = bfs(G)
    max_dist = float('-inf')
    cnt = 0
    for i in range(2, n+1):
        dist = v[i]
        if max_dist < dist:
            max_dist = dist
            cnt = 1
        elif max_dist == dist:
            cnt += 1
            
    return cnt
    
    