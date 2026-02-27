import re

y=input()

x=re.split(r"(?=[A-Z])", y)

print(x)