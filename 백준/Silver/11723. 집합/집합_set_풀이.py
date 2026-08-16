M = int(input())
S = set()

for _ in range(M):
    cmd = input().split()

    if len(cmd) == 1:
        if cmd[0] == 'all':
            S = {i for i in range(1, 21)}
        elif cmd[0] == 'empty':
            S = set()

    else:
        c, i = cmd[0], int(cmd[1])

        if c == 'add':
            S.add(i)
        elif c == 'remove':
            if i in S:
                S.remove(i)
        elif c == 'check':
            if i in S:
                print(1)
            else:
                print(0)
        elif c == 'toggle':
            if i in S:
                S.remove(i)
            else:
                S.add(i)