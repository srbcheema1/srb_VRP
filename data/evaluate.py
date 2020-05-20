from srblib import Tabular

a = Tabular()
a.load_json('data/out.json')

summ = [0,0,0,0]
mint = [0,0,0,0]
time = [0,0,0,0]

for row in a:
	summ[0] += row[3]
	summ[1] += row[5]
	summ[2] += row[7]
	summ[3] += row[9]

	time[0] += row[4]
	time[1] += row[6]
	time[2] += row[8]
	time[3] += row[10]

	minn = min(row[3],row[5],row[7],row[9])
	if(minn == row[3]): mint[0] += 1
	elif(minn == row[5]): mint[1] += 1
	elif(minn == row[7]): mint[2] += 1
	elif(minn == row[9]): mint[3] += 1

n = len(a) - 1
avg = [round(x/n,2) for x in summ]
time = [round(x/n,2) for x in time]

b = Tabular([["Prop","SA","ACO","ACO-SA","Kmean-SA"],["avg cost"] + avg,["avg time"] + time,["min times"] + mint])
print(b)