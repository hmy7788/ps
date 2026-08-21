def is_prime(p):
    for i in range(2, p):
        if p % i == 0: return False
    return True

def solution(nums):
    n = len(nums)
    cnt = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                p = nums[i] + nums[j] + nums[k]
                # print(p)
                if is_prime(p):
                    cnt += 1
    
    return cnt