import heapq

def solution(operations):
    min_heap = []
    max_heap = []
    visited = [False] * 1000000
    ID = 0
    
    for op in operations:
        i, j = op.split()
        j = int(j)
        
        # 힙에 삽입
        if i == 'I':
            heapq.heappush(min_heap, (j, ID))
            heapq.heappush(max_heap, (-j, ID))
            visited[ID] = True
            ID += 1
        
        # 최대값 삭제
        elif i == 'D' and j == 1:
            while max_heap and visited[max_heap[0][1]] == False:
                heapq.heappop(max_heap)
            if max_heap:
                visited[max_heap[0][1]] = False
                heapq.heappop(max_heap)
        
        # 최소값 삭제
        elif i == 'D' and j == -1:
            while min_heap and visited[min_heap[0][1]] == False:
                heapq.heappop(min_heap)
            if min_heap:
                visited[min_heap[0][1]] = False
                heapq.heappop(min_heap)
        
    while max_heap and visited[max_heap[0][1]] == False:
        heapq.heappop(max_heap)
    while min_heap and visited[min_heap[0][1]] == False:
        heapq.heappop(min_heap)
    
    if max_heap and min_heap:
        return [-max_heap[0][0], min_heap[0][0]]
    else:
        return [0, 0]