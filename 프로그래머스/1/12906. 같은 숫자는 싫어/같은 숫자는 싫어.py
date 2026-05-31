def solution(arr):
    i = 1
    answer = [arr[0]]
    prev_value = arr[0]
    
    while(i <= len(arr)-1):
        if(prev_value != arr[i]):
            answer.append(arr[i])
            prev_value = arr[i]
        i += 1
    
    return answer