from collections import deque

def sliding_min(arr, window_size):
    dq, result = deque(), []
    for i, v in enumerate(arr):
        while dq and arr[dq[-1]] >= v:
            dq.pop()
        dq.append(i)
        while dq[0] <= i-window_size:
            dq.popleft()
        result.append(arr[dq[0]])
    return result[window_size-1:]
        
def make_T(arr):
    n, m = len(arr), len(arr[0])
    arr_T = []
    for i in range(m):
        result = []
        for j in range(n):
            result.append(arr[j][i])
        arr_T.append(result)
    return arr_T

def find_max_value(arr):
    max_i, max_j, max_value = 0, 0, float('-inf')
    n, m = len(arr), len(arr[0])
    
    for i in range(m):
        for j in range(n):
            if arr[j][i] > max_value:
                max_value = arr[j][i]
                max_i, max_j = i, j
    
    return [max_i, max_j]

def solution(m, n, h, w, drops):
    maps = [[float('inf')]*n for _ in range(m)]
    for i, (r, c) in enumerate(drops):
        maps[r][c] = i+1
        
    mid_arr = []
    for m in maps:
        mid_arr.append(sliding_min(m, w))
    
    mid_arr_T = make_T(mid_arr)
        
    end_arr = []
    for maT in mid_arr_T:
        end_arr.append(sliding_min(maT, h))
    
    result = find_max_value(end_arr)
    
    return result