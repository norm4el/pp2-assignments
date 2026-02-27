import re
y=input()
x=re.fullmatch("a.*b$", y)
print(bool(x))
