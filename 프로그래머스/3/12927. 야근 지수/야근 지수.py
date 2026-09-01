import heapq as hq

def solution(n, works):
    heap = []
    
    for w in works:
        heap.append((-w, w))
    
    hq.heapify(heap)
    
    for _ in range(n):
        if heap:
            w = hq.heappop(heap)[1]
            w -= 1
            if w != 0:
                hq.heappush(heap, (-w, w))
    
    print(heap)
    
    if heap:
        total = 0
        for w1, w2 in heap:
            total += w2 ** 2
        return total
    return 0