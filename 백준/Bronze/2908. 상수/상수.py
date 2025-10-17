A, B = input().split()
reverse_A = ''
reverse_B = ''
for i in range(2, -1, -1):
    reverse_A += A[i]
    reverse_B += B[i]

reverse_A = int(reverse_A)
reverse_B = int(reverse_B)
if(reverse_A > reverse_B): print(reverse_A)
else: print(reverse_B)