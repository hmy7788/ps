# 1 x : push x
# 2 : pop / 없으면 -1
# 3 : len
# 4 : empty / 있으면 0 없으면 1
# 5 : top / 없으면 -1

stack = []

def push(a):
    stack.append(a)

def pop():
    if(len(stack) == 0):
        print(-1)
    else:
        print(stack.pop())

def length():
    print(len(stack))

def empty():
    if(len(stack) == 0):
        print(1)
    else:
        print(0)

def top():
    if(len(stack) == 0):
        print(-1)
    else:
        print(stack[-1])

def solution():
    l = list(map(int,sys.stdin.readline().split()))
    if(l[0] == 1):
        push(l[1])
    elif(l[0] == 2):
        pop()
    elif(l[0] == 3):
        length()
    elif(l[0] == 4):
        empty()
    else:
        top()

import sys

n = int(sys.stdin.readline())
for i in range(n):
    solution()