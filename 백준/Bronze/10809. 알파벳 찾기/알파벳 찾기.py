S = input()
l = ['-1' for _ in range(26)]
alpha = 'abcdefghijklmnopqrstuvwxyz'

for i in range(len(S)):
    if(l[alpha.index(S[i])] == '-1'):
        l[alpha.index(S[i])] = str(S.index(S[i]))
print(' '.join(l))

# a b  c  d e  f  g  h  i j k  l  m n o p   q  r  s  t  u  v  w  x  y  z
# 1 0 -1 -1 2 -1 -1 -1 -1 4 3 -1 -1 7 5 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1