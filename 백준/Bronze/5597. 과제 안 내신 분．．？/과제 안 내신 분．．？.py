l = {i+1: 'x' for i in range(30)}
no_hw = []

for _ in range(28):
    n = int(input())
    l[n] = 'o'

for k, v in l.items():
    if(v == 'x'): no_hw.append(k)

print(no_hw[0])
print(no_hw[1])