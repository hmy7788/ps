def solution(numbers, target):
    cnt = 0
    
    def dfs(index, current_sum):
        nonlocal cnt
        if index == len(numbers):
            if current_sum == target:
                cnt += 1
            return
        # print(f'dfs({index}, {current_sum})')
        dfs(index+1, current_sum + numbers[index])
        dfs(index+1, current_sum - numbers[index])
    
    dfs(0, 0)
    
    return cnt