import sys

def Checking_Parenthesis_String(ps):
    stack = []
    for s in ps:
        if(s == '(' or s == '['): stack.append(s)
        if(s == ')'):
            if(len(stack) == 0): return 'no'
            if(stack[-1] == '('): stack.pop()
            else: return 'no'
        elif(s == ']'):
            if(len(stack) == 0): return 'no'
            if(stack[-1] == '['): stack.pop()
            else: return 'no'
    if(len(stack) == 0): return 'yes'
    else: return 'no'

input = sys.stdin.readline
while(1):
    string = input().rstrip()
    if(string[0] == '.'): break
    print(Checking_Parenthesis_String(string))