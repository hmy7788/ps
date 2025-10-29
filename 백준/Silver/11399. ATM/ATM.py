N = int(input())
delay_times = list(map(int, input().split()))
delay_times.sort()
accum_sum = [delay_times[0]]

for i in range(1, N):
    accum_sum.append(accum_sum[i-1] + delay_times[i])

print(sum(accum_sum))