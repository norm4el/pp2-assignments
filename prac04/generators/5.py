def inverse(N):
    for i in range(N, -1, -1):
        yield i

n= int(input())

for s in inverse(n):
    print(s)