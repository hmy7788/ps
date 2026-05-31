def dequeue(remain_time):
    count = 0
    while(remain_time and remain_time[0] == 0):
        count += 1
        remain_time.pop(0)
    return remain_time, count
    
def solution(progresses, speeds):
    answer = []
    remain_time = []
    n = len(progresses)
    
    for i in range(n):
        remain_work = 100 - progresses[i]
        remain_time.append(remain_work // speeds[i])
        
        if(remain_work % speeds[i] > 0):
            remain_time[i] += 1
    
    while(len(remain_time) != 0):
        working_time = remain_time[0]
        
        for i in range(len(remain_time)):
            if(remain_time[i] - working_time < 0):
                remain_time[i] = 0
            else:
                remain_time[i] -= working_time
                
        print(remain_time)
        remain_time, count = dequeue(remain_time)
        answer.append(count)
        
    return answer