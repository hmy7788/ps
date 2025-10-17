s = input()
flag = True
for i in range(len(s)):
    j = len(s)-i-1
    if(s[i] != s[j]):
        flag = False
        break
if(flag): print(1)
else: print(0)