from srblib import Tabular

a = Tabular()
a.load_json('data/out.json')

summ = [0,0,0,0]
mint = [0,0,0,0]
for row in a:
	summ[0] += row[2]
	summ[1] += row[3]
	summ[2] += row[4]
	summ[3] += row[5]

	minn = min(row[2],row[3],row[4],row[5])
	if(minn == row[2]): mint[0] += 1
	if(minn == row[3]): mint[1] += 1
	if(minn == row[4]): mint[2] += 1
	if(minn == row[5]): mint[3] += 1

n = len(a) - 1
avg = [x/n for x in summ]
print("SA","ACO","ACO-SA","Kmean-SA")
print(*avg)
print(*mint)