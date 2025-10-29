import sys

def Checking_Parenthesis_String(ps):
    stack = []
    for s in ps:
        if(s == '('): stack.append(s)
        else:
            if(len(stack) == 0): return 'NO'
            else: stack.pop()
    if(len(stack) == 0): return 'YES'
    else: return 'NO'

input = sys.stdin.readline
N = int(input())

for _ in range(N):
    ps = input().rstrip()
    print(Checking_Parenthesis_String(ps))