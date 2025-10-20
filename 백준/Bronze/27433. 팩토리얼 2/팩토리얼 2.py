def factoiral(N):
    if(N == 1 or N == 0): return 1
    return N * factoiral(N-1)

print(factoiral(int(input())))