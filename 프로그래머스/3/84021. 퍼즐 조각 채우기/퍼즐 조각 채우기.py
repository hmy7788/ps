from collections import deque

def bfs(maps, v, y, x, mode):
    dq = deque()
    dq.append((y, x))
    v[y][x] = 1
    size = len(v)
    points = []
    
    while dq:
        p = dq.popleft()
        cy, cx = p[0], p[1]
        points.append((cy, cx))
        
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = cy+dy, cx+dx
            
            if mode == 1:
                if 0 <= ny < size and 0 <= nx < size and maps[ny][nx] == 1 and v[ny][nx] == 0:
                    dq.append((ny, nx))
                    v[ny][nx] = 1
            else:
                if 0 <= ny < size and 0 <= nx < size and maps[ny][nx] == 0 and v[ny][nx] == 0:
                    dq.append((ny, nx))
                    v[ny][nx] = 1
                    
    return points


def normalization(point):
    min_y = min(p[0] for p in point)
    min_x = min(p[1] for p in point)
    
    normalized = [(y - min_y, x - min_x) for y, x in point]
    
    return sorted(normalized)


def get_all_rotated_points(points):
    rotations = []
    curr = points
    
    for _ in range(4):
        rotations.append(curr)
        rotated = [(x, -y) for y, x in curr]
        curr = normalization(rotated)
    
    return rotations


def solution(game_board, table):
    size = len(game_board)
    v1 = [[0] * size for _ in range(size)]
    v2 = [[0] * size for _ in range(size)]
    blocks = []
    blanks = []
    answer = 0
    
    for y in range(size):
        for x in range(size):
            if game_board[y][x] == 0 and v1[y][x] == 0:
                blanks.append(bfs(game_board, v1, y, x, 0))
            if table[y][x] == 1 and v2[y][x] == 0:
                blocks.append(bfs(table, v2, y, x, 1))
                
    blanks = [normalization(b) for b in blanks]
    blocks = [normalization(b) for b in blocks]
    
    used_blocks = [False] * len(blocks)
        
    for b1 in blanks:
        b1s = get_all_rotated_points(b1)
        
        for i, b2 in enumerate(blocks):
            if not used_blocks[i] and len(b1) == len(b2):
                if b2 in b1s:
                    answer += len(b2) 
                    used_blocks[i] = True
                    break

    return answer