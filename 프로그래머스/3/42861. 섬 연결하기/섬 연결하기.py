def find(p, x):
    if p[x] != x:
        p[x] = find(p, p[x])
    return p[x]

def union(p, n1, n2):
    root_n1 = find(p, n1)
    root_n2 = find(p, n2)
    
    if root_n1 < root_n2:
        p[root_n2] = root_n1
    else:
        p[root_n1] = root_n2

def solution(n, costs):
    costs.sort(key=lambda x : x[2])
    p = [i for i in range(n)]
    min_dist = 0
    edge_cnt = 0
    
    for edge in costs:
        if edge_cnt == n-1:
            break
        else:
            n1, n2, dist = edge
            if find(p, n1) != find(p, n2):
                union(p, n1, n2)
                min_dist += dist
                edge_cnt += 1
                
    return min_dist