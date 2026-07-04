def solution(phone_book):
    phone_book.sort()
    n = len(phone_book)
    for i in range(n-1):
        m = len(phone_book[i])
        if phone_book[i] == phone_book[i+1][:m]:
            return False
    return True