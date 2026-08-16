from itertools import product
from collections import deque

def bfs(infected, edge_type, graph):
    dq = deque()
    
    for i in infected:
        dq.append(graph[i])
    
    while dq:
        cn = dq.popleft()
        for nn, t in cn:
            if t == edge_type and nn not in infected:
                infected.add(nn)
                dq.append(graph[nn])
    
    return infected
    
def solution(n, infection, edges, k):
    graph = {i: [] for i in range(1, n+1)}
    cnt = 1
    
    for x, y, t in edges:
        graph[x].append((y, t))
        graph[y].append((x, t))
    
    for seq in product(['A', 'B', 'C'], repeat=k):
        infected = {infection}
        
        for edge_type in seq:
            if edge_type == 'A': edge_type = 1
            elif edge_type == 'B': edge_type = 2
            elif edge_type == 'C': edge_type = 3
            
            infected = bfs(infected, edge_type, graph)
            
        cnt = max(cnt, len(infected))
        
    return cnt