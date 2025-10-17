s = input()
c = 0
i = 0
change = ['c=', 'c-', 'dz=', 'd-', 'lj', 'nj', 's=', 'z=']
while(i < len(s)):
    if(i <= len(s)-2 and s[i] + s[i+1] in change):
        i += 2
    elif(i <= len(s)-3 and s[i] + s[i+1] + s[i+2] in change):
        i += 3
    else:
        i += 1
    c += 1
print(c)