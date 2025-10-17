l = []
for _ in range(10):
    l.append(int(input())%42)
# print(len(set(l)))

c = 0
for i in range(10):
    flag = True
    for j in range(i+1, 10):
        if(l[i] == l[j]):
            flag = False
            break
    if(flag == False):
        continue
    else:
        c += 1
print(c)