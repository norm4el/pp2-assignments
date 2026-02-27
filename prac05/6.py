import re
y=input()
x=re.sub(r"[\s,\.]", ":", y )
print(x)
