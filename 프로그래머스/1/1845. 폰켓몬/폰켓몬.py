# n = len(nums) // 2
# m = len(set(nums))
# return min(len(nums) // 2, len(set(nums)))

def solution(nums):
    num_dict = {}
    check = set()
    n = len(nums)
    count = 0
    
    for key in nums:
        if(key in num_dict):
            num_dict[key] += 1
        else:
            num_dict[key] = 1
    
    for no in num_dict:
        if(no not in check and count < len(nums) // 2):
            check.add(no)
            count += 1
    return count