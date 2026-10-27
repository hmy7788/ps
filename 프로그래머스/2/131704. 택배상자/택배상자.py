def solution(order):
    stack = []
    result = 0
    idx = 0
    
    for box in range(1, len(order)+1):
        if box == order[idx]:
            idx += 1
            result += 1
        else:
            stack.append(box)
            
        while stack and stack[-1] == order[idx]:
            stack.pop()
            idx += 1
            result += 1
            
    return result