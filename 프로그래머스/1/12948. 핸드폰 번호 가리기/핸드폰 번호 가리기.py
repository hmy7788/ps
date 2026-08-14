def solution(phone_number):
    back = phone_number[-4:]
    front = phone_number[:-4]
    
    return '*'*len(front) + back