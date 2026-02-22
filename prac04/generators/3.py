def Iterr(N):
    for i in range(0, N+1):
        if (i%3==0 and i%4==0):
            yield i

n=int(input())

for s in Iterr(n):
    print(s)