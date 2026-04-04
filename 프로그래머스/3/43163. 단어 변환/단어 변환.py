from collections import deque

def is_change(s1, s2):
    n = len(s1)
    same_cnt = 0
    
    for i in range(n):
        if s1[i] == s2[i]:
            same_cnt += 1

    diff_cnt = n - same_cnt
    if diff_cnt == 1:
        return True
    else:
        return False

    
cnt = 0
def dfs(G, start_node, visited, target, words):
    if target == words[start_node]:
        return cnt
    
    visited[start_node] = 1
    for n in G[start_node]:
        if visited[n] == 1:
            return
        cnt += 1
        dfs(G, n, visited, target, words)
    
    return cnt
    
    
def bfs(G, visited, target, words):
    dq = deque()
    dq.append(G[0])
    
    while dq:
        nodes = dq.popleft()
        next_nodes = nodes[0]
        prev_node = nodes[1]
        for n in next_nodes:
            if visited[n] == 0:
                visited[n] = visited[prev_node] + 1
                dq.append(G[n])
                if words[n] == target:
                    return visited[n]-1


def solution(begin, target, words):
    if target not in words:
        return 0
    
    words.insert(0, begin)
    n = len(words)
    G = {i:[[], i] for i in range(n)}
    visited = [0 for _ in range(n)]
    visited[0] = 1
    
    # print(G)
    
    for i in range(n):
        for j in range(n):
            if i == j: continue
            if is_change(words[i], words[j]):
                G[i][0].append(j)
    
#     print(G)
#     print(bfs(G, visited, target, words))
    
    return bfs(G, visited, target, words)