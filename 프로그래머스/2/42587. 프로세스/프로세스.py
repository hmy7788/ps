def solution(priorities, location):
    count = 0
    while(True):
        print(f'{priorities}, {location}, {count}')
        if(priorities[0] == max(priorities)):
            if(location == 0):
                return count+1
            priorities.pop(0)
            count += 1
            location -= 1
        else:
            priorities.append(priorities.pop(0))
            if(location == 0):
                location = len(priorities)-1
            else:
                location -= 1