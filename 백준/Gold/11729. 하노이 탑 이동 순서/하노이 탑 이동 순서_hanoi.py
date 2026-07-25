def hanoi(a, b, n):
    if n == 1:
        print(a, b)
        return
    
    hanoi(a, 6-a-b, n-1)
    print(a, b)
    hanoi(6-a-b, b, n-1)

K = int(input())
print(2**K-1)
hanoi(1, 3, K)