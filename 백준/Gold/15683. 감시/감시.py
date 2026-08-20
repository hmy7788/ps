directions = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}

cam_options = {
    1: [['up'], ['down'], ['left'], ['right']],
    2: [['up', 'down'], ['left', 'right']],
    3: [['up','right'], ['right','down'], ['down','left'], ['left','up']],
    4: [['down','left','right'], ['up','left','right'], ['up','down','right'], ['up','down','left']],
    5: [['up', 'down', 'left', 'right']]
}


def collect_cameras(maps, N, M):
    cameras = []
    for i in range(N):
        for j in range(M):
            if maps[i][j] in cam_options:
                cameras.append((i, j, maps[i][j]))
    return cameras


def mark_direction(grid, i, j, dy, dx, N, M):
    y, x = i+dy, j+dx
    while 0 <= y < N and 0 <= x < M:
        if grid[y][x] == 6: break
        if grid[y][x] == 0: grid[y][x] = '#'

        y += dy
        x += dx
    
from itertools import product
import copy

def solution(N, M, maps):
    cameras = collect_cameras(maps, N, M)
    all_options = [cam_options[cam_type] for (i, j, cam_type) in cameras]
    min_blind = float('inf')

    for combo in product(*all_options):
        temp = copy.deepcopy(maps)

        for (i, j, cam_type), choosen_dirs in zip(cameras, combo):
            for d in choosen_dirs:
                dy, dx = directions[d]
                mark_direction(temp, i, j, dy, dx, N, M)
        
        blind_count = sum(row.count(0) for row in temp)
        min_blind = min(min_blind, blind_count)
    
    return min_blind
    


N, M = map(int, input().split())
maps = []
for _ in range(N):
    maps.append(list(map(int, input().split())))

print(solution(N, M, maps))