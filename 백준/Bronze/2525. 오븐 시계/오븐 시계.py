def h_m_to_m(h, m):
    return h * 60 + m

def m_to_h_m(m):
    return (m//60)%24, m % 60

h, m = map(int, input().split())
c = int(input())
m = h_m_to_m(h, m)
h, m = m_to_h_m(m+c)
print(h, m)