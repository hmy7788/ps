def is_prime(n):
    if n == 0 or n == 1:
        return False
    
    for i in range(2, n):
        if n % i == 0: return False
    return True


def dfs(current_str, visited, numbers, result_set):
    if current_str != "":
        result_set.add(int(current_str))
    
    for i in range(len(numbers)):
        if visited[i] == 0:
            visited[i] = 1
            dfs(current_str+numbers[i], visited, numbers, result_set)
            visited[i] = 0


def solution(numbers):
    n = len(numbers)
    result_set = set()
    visited = [0 for _ in range(n)]
    cnt = 0
    
    dfs("", visited, numbers, result_set)
    # print(result_set)
    
    for num in result_set:
        if is_prime(num): cnt += 1
    
    return cnt