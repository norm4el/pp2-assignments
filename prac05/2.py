import re
y=input()
x=re.fullmatch("abb+", y)
print(bool(x))
