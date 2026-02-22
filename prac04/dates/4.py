from datetime import datetime
с= "%Y-%m-%d %H:%M:%S"

d1_str = input()
d2_str = input()

d1=datetime.strptime(d1_str, с)
d2= datetime.strptime(d2_str, с)

diff=abs((d2 - d1).total_seconds())
print( int(diff))