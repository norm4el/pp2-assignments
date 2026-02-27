import re

y=input()

x=re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", y)
x=re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", x)

print(x)