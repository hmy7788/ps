def dfs(computers, i, visited):
    visited[i] = 1
    n = len(computers)
    
    for j in range(n):
        if i != j and computers[i][j] == 1 and visited[j] == 0:
            dfs(computers, j, visited)
    

def solution(n, computers):
    visited = [0 for _ in range(n)]
    cnt = 0
    
    for i in range(n):
        if visited[i] == 0:
            dfs(computers, i, visited)
            cnt += 1
            
    return cnt