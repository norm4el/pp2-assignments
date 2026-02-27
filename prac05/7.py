import re
y=input()
def Up(m):
    return m.group(1).upper()
x=re.sub(r"_([a-z])", Up, y )
print(x)
