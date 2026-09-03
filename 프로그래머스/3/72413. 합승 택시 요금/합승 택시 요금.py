def get_floyd_dist(n, fares):
    dist = [[float('inf') for _ in range(n+1)] for _ in range(n+1)]
    
    for i in range(n+1):
        dist[i][i] = 0
    
    for c, d, f in fares:
        dist[c][d] = f
        dist[d][c] = f
    
    for t in range(1, n+1):
        for i in range(1, n+1):
            for j in range(1, n+1):
                dist[i][j] = min(dist[i][j], dist[i][t]+dist[t][j])
                
    return dist

def solution(n, s, a, b, fares):
    dist = get_floyd_dist(n, fares)
    
    min_cost = float('inf')
    
    for p in range(1, n+1):
        total_cost = min(dist[s][p]+dist[p][a]+dist[p][b],
                         dist[s][a]+dist[s][b])
        if min_cost > total_cost:
            min_cost = total_cost
    
    return min_cost