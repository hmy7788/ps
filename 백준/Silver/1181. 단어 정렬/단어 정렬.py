N = int(input())
s = []

for _ in range(N):
    word = input()
    if word not in s:
        s.append(word)

s.sort()
s.sort(key=lambda x: len(x))
print('\n'.join(s))