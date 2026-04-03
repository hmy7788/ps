orders = []

def check_max_cnt(orders, k, dungeons):
    max_cnt = -1
    
    for o in orders:
        cnt = 0
        current_k = k
        for idx in o:
            if current_k >= dungeons[idx][0]:
                current_k -= dungeons[idx][1]
                cnt += 1
            else:
                break
                
        if max_cnt < cnt:
            max_cnt = cnt
    
    return max_cnt


def dfs(current_path, n, visited):
    if len(current_path) == n:
        orders.append(current_path[:])
        return
    
    for i in range(n):
        if visited[i] == 0:
            visited[i] = 1
            current_path.append(i)
            dfs(current_path, n, visited)
            current_path.pop()
            visited[i] = 0

            
def solution(k, dungeons):
    n = len(dungeons)
    visited = [0] * n
    dfs([], n, visited)
    
    return check_max_cnt(orders, k, dungeons)