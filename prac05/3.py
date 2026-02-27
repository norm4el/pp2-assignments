import re
y=input()
x=re.fullmatch("[a-z]+_[a-z]+", y)
print(x)
