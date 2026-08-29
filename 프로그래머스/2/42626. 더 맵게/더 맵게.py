import heapq as hq

def is_all_check(scoville, K):
    for s in scoville:
        if s < K:
            return False
    return True

def solution(scoville, K):
    cnt = 0
    hq.heapify(scoville)
    
    while len(scoville) != 1:
        if is_all_check(scoville, K):
            return cnt
        
        first = hq.heappop(scoville)
        second = hq.heappop(scoville)
        hq.heappush(scoville, first + 2*second)
        
        cnt += 1
        
    if scoville[0] >= K:
        return cnt
    return -1