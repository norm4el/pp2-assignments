import re
y=input()
x=re.fullmatch("ab*", y)
print(bool(x))
