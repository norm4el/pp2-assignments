def Squarer(N):
    for i in range(1, N+1):
        yield i*i

n = int(input())

for s in Squarer(n):
    print(s)