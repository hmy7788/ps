import heapq as hq

def checking(scoville, K):
    for s in scoville:
        if(s < K):
            return False
    return True

def solution(scoville, K):
    hq.heapify(scoville)
    count = 0
    while(len(scoville) != 1):
        if(checking(scoville, K)):
            return count
        else:
            m1 = hq.heappop(scoville)
            m2 = hq.heappop(scoville)
            hq.heappush(scoville, m1 + 2*m2)
            count += 1
        
    if(checking(scoville, K)):
        return count
    else:
        return -1
        