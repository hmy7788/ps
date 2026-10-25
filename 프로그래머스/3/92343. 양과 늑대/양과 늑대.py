from collections import defaultdict

def solution(info, edges):
    G = defaultdict(list)
    max_sheep = -1
    
    for n1, n2 in edges:
        G[n1].append(n2)
        
    def DFS(current_node, sheep, wolf, next_nodes):
        nonlocal max_sheep
        
        if info[current_node] == 0: sheep += 1
        else: wolf += 1
        
        if wolf >= sheep: return
    
        max_sheep = max(max_sheep, sheep)
        
        new_next_nodes = list(next_nodes)
        new_next_nodes.remove(current_node)
        new_next_nodes.extend(G[current_node])
        
        for next_node in new_next_nodes:
            DFS(next_node, sheep, wolf, new_next_nodes)
    
    DFS(0, 0, 0, [0])
    
    return max_sheep
    