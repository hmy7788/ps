import heapq

def solution(jobs):
    jobs.sort(key=lambda x : x[0])
    current_time, HD, n = 0, 0, len(jobs)
    heap, result = [], []
    i = 0
    
    while len(result) < n:
        while i <= n-1 and jobs[i][0] <= current_time:
            request_time, excute_time = jobs[i][0], jobs[i][1]
            process = [excute_time, request_time, i]
            heapq.heappush(heap, process)
            i += 1
        
        if HD and HD[3] == current_time:
            result.append(HD)
            HD = 0
            
        if not HD and heap and heap[0][1] <= current_time:
            process = heapq.heappop(heap)
            process.append(current_time + process[0])
            HD = process
        
        current_time += 1
    
    hap = 0
    for r in result:
        hap += r[3]-r[1]
    return hap // len(result)