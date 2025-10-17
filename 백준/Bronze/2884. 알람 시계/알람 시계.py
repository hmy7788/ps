def h_m_to_m(h, m):
    return h * 60 + m

def m_to_h_m(m):
    if(m < 0):
        return 23, 60+m
    return m // 60, m % 60

h, m = map(int ,input().split())
m = h_m_to_m(h, m)
h, m = m_to_h_m(m-45)
print(h, m)