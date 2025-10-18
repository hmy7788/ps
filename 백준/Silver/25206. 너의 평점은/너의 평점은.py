sum0 = 0
sum1 = 0
d = {'A+': 4.5,
     'A0': 4.0,
     'B+': 3.5,
     'B0': 3.0,
     'C+': 2.5,
     'C0': 2.0,
     'D+': 1.5,
     'D0': 1.0,
     'F': 0.0}

for _ in range(20):
    s = input().split()
    if(s[2] != 'P'):
        sum0 += float(s[1]) * d[s[2]]
        sum1 += float(s[1])
print(sum0 / sum1)