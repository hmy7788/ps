from collections import deque

def BFS(land, label, y, x, group_id):
    dq = deque()
    dq.append((y, x))
    label[y][x] = group_id
    N, M = len(land), len(land[0])
    cnt = 1
    
    while dq:
        cy, cx = dq.popleft()
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = cy+dy, cx+dx
            if 0 <= ny < N and 0 <= nx < M:
                if land[ny][nx] == 1 and label[ny][nx] == 0:
                    label[ny][nx] = group_id
                    dq.append((ny, nx))
                    cnt += 1
    return cnt


def solution(land):
    N, M = len(land), len(land[0])
    label = [[0 for _ in range(M)] for _ in range(N)]
    size, group_id = {}, 0
    max_cnt = float('-inf')
    
    for x in range(M):
        for y in range(N):
            if land[y][x] == 1 and label[y][x] == 0:
                group_id += 1
                cnt = BFS(land, label, y, x, group_id)
                size[group_id] = cnt
                

    for x in range(M):
        oils = set()
        cnt = 0
        for y in range(N):
            if label[y][x] != 0:
                oils.add(label[y][x])
        for o in oils:
            cnt += size[o]
        if max_cnt < cnt:
            max_cnt = cnt
    
    return max_cnt