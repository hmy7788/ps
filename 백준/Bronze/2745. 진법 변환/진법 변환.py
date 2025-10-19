digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
N, B = input().split()
B = int(B)

decimal_value = 0
idx = len(N)-1
for i in N:
    decimal_value += digits.index(i)*(B**idx)
    idx -= 1
print(decimal_value)

# print(int(N, B))