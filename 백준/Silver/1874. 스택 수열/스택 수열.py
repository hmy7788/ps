def solution(n, targets):
    counter = 1
    stack = []
    result = []

    for t in targets:
        while True:
            if stack and stack[-1] == t:
                stack.pop()
                result.append('-')
                break
            else:
                if counter > n:
                    print('NO')
                    return
                stack.append(counter)
                counter += 1
                result.append('+')
        
    print('\n'.join(result))

n = int(input())
targets = []

for _ in range(n):
    targets.append(int(input()))

solution(n, targets)