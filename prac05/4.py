import re
y=input()
x=re.findall("[A-Z][a-z]+", y)
print(x)
