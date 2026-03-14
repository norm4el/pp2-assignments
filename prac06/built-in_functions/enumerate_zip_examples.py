names = ["ffff", "mega", "chel"]
scores = [90, 85, 95]

print("enumerate:")
for i, name in enumerate(names):
    print(i, name)

print("zip:")
for name, score in zip(names, scores):
    print(name, score)

x = "123"
print("type:", type(x))
print("is string:", isinstance(x, str))

a = int(x)
b = float(x)
c = str(456)

print(a, type(a))
print(b, type(b))
print(c, type(c))