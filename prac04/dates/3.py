from datetime import datetime

dt =datetime.now()
mc =dt.replace(microsecond=0)

print(dt)
print(mc)