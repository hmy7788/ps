def solution(n, control):
    for cmd in control:
        if cmd == 'w': n += 1
        elif cmd == 's': n -= 1
        elif cmd == 'd': n += 10
        elif cmd == 'a': n -= 10
    return n