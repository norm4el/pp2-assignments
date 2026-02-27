import re

y=input()

x=re.sub("(?<!^)(?=[A-Z])", " ", y)
print(x)