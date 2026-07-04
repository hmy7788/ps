def solution(array, commands):
    answer = []
    
    for cmd in commands:
        i = cmd[0]-1
        j = cmd[1]-1
        k = cmd[2]-1
        slice_list = array[i:j+1]
        sort_list = sorted(slice_list)
        answer.append(sort_list[k])
    
    return answer