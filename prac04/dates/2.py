import datetime

t = datetime.date.today()
y= t - datetime.timedelta(days=1)
tom = t+ datetime.timedelta(days=1)

print(y)
print(t)
print(tom)