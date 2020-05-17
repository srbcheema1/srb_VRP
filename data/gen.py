from random import randint
import sys

n = 30
if(len(sys.argv) == 2):
	n = int(sys.argv[1])

pt_set = set()
for _ in range(n):
	a = randint(1,50)
	b = randint(1,50)
	while((a,b) in pt_set):
		a = randint(1,50)
		b = randint(1,50)
	pt_set.add((a,b))
	print(a,b)