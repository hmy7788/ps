def solution(diffs, times, limit):
    def check(level):
        used_time = 0
        for i, (d, t) in enumerate(zip(diffs, times)):
            if level >= d:
                used_time += t
            else:
                cur = times[i]
                prev = times[i-1]
                used_time += (cur+prev)*(d-level) + cur
                
        return used_time <= limit
    
    left, right = 1, max(diffs)
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        
        if check(mid):
            answer = mid
            right = mid-1
        else:
            left = mid+1
    
    return answer