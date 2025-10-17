s = input().upper()
d = dict()
for i in s:
    if(i not in d.keys()): d[i] = 1
    else: d[i] += 1

max_value = -1
max_key = 0
flag = True
for k, v in d.items():
    if(max_value < v):
        max_value = v
        max_key = k
for k, v in d.items():
    if(max_key != k and max_value == v): flag = False
if(flag): print(max_key)
else: print('?')