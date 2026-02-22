def Evenn(N):
    for i in range(0, n+1):
        if (i%2==0):
            yield i

n=int(input())
k=0

for s in Evenn(n):
    
    if k==0:
        print(s, end="", sep="")
        k+=1
    else:
        print(", ", s, end="", sep="")