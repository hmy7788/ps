def solution(array, height):
    cnt = 0
    for h in array:
        if h > height:
            cnt += 1
    return cnt