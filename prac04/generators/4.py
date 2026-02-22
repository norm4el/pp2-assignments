def Squares(a, b):
    for i in range(a, b+1):
        yield i*i

a, b = map(int, input().split())

for s in Squares(a,b):
    print(s)