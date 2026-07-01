from math import comb
import sys

data=sys.stdin.read().split()
idx=0
T=int(data[idx])
idx+=1

for _ in range(T):
    N,M=int(data[idx]),int(data[idx+1]);idx+=2
    print(comb(M,N))