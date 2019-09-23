import pickle
import numpy as np
import sys
import os

a = []
for i in range(10):
	filename = str(i) + '.pkl'
	if os.path.isfile(filename):
		a0 = pickle.load(open(filename, 'rb'))
		a.append(a0)

l = [
[25, 26, 9, 11, 2, 0, 21, 1, 10, 27, 4, 19],
[1, 21, 27, 19, 2, 0, 26, 9, 11, 25, 10, 4],
[25, 19, 4, 27, 26, 1, 0, 2, 9, 11, 10, 21],
[11, 19, 27, 1, 25, 21, 4, 2, 9, 10, 0, 26],
[26, 19, 25, 0, 1, 27, 10, 9, 11, 2, 21, 4],
[1, 26, 27, 0, 9, 25, 10, 11, 4, 21, 2, 19],
[2, 26, 11, 21, 9, 0, 10, 4, 1, 25, 19, 27],
[0, 19, 2, 1, 26, 9, 21, 25, 27, 10, 4, 11],
[25, 0, 9, 26, 11, 21, 1, 4, 27, 19, 2, 10],
[2, 4, 27, 19, 0, 9, 10, 26, 21, 11, 1, 25],
]

candidates = [0, 1, 2, 4, 9, 10, 11, 19, 21, 25, 26, 27]

new_a = []
new_l = []
for i in range(len(a)):
	aa = a[i]
	ll = l[i]
	if len(ll) != aa.shape[0]:
		print('not match')
	ai = []
	li = []
	for j in range(len(ll)):
		if ll[j] in candidates:
			ai.append(aa[j])
			li.append(ll[j])
	new_a.append(ai)
	new_l.append(li)

a = np.concatenate(new_a, axis=0)
l = np.concatenate(new_l, axis=0)

print(l)
print(a.shape)
print(l.shape)

pickle.dump((a,l), open('pickle/' + sys.argv[1] + '.pkl', 'wb'))