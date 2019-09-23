import numpy as np
import matplotlib.pyplot as plt
import time
import os
import pickle
import sys
from sklearn import svm, neighbors
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import confusion_matrix
from utils import *

def get_raw_data_per_file(filename):
	a, l = pickle.load(open(filename, 'rb'))
	raw_acc.append(a)
	raw_lab.append(l)

def dump_to_plain():
	global raw_acc, raw_lab, spl2
	f = open('plain.txt', 'w')
	raw_acc = raw_acc.swapaxes(1, 2)
	f.write(str(raw_acc.shape[0]) + ' ' + str(raw_acc.shape[1]) + ' ' + str(raw_acc.shape[2]) + '\n')
	for i in range(raw_acc.shape[0]):
		for j in range(raw_acc.shape[1]):
			for k in range(raw_acc.shape[2]):
				f.write(str(raw_acc[i, j, k]) + ' ')
	f.write('\n')
	for i in range(raw_lab.shape[0]):
		f.write(str(raw_lab[i]) + ' ')
	f.write('\n')
	f.write(str(len(spl2)))
	for i in range(len(spl2)):
		f.write(' ' + str(spl2[i]))
	f.write('\n')
	f.close()
	print('dump complete')

dset = 'v/'
usernames = [dset+'cs60', dset+'czy60', dset+'fjy60', dset+'gyz60', dset+'lgh60', dset+'lyq60',
	dset+'lzp60', dset+'plh60', dset+'rj60', dset+'xcn60', dset+'ycy60', dset+'yzc60']
if len(sys.argv) >= 2:
	usernames = [sys.argv[1]]
raw_acc = []
raw_lab = []
for username in usernames:
	filename = 'pickle/' + username + '.pkl'
	if os.path.isfile(filename):
		get_raw_data_per_file(filename)
spl = [len(i) for i in raw_lab]
print('user size:', spl)
raw_acc = np.concatenate(raw_acc, axis=0)
raw_lab = np.concatenate(raw_lab, axis=0)

if len(sys.argv) > 2 and sys.argv[1] == 'all':
	candidates = list(range(34))
else:
	candidates = [0, 1, 2, 4, 9, 10, 11, 12, 13, 18, 19, 20, 23, 24, 25, 26, 27]
	candidates = [0, 1, 2, 4, 9, 10, 11, 19, 21, 25, 26, 27]
	# candidates = [0, 9, 10, 19, 26]
new_raw_acc = []
new_raw_lab = []
prev_i = 0
prev_len = 0
j = 0
spl2 = []
for i in range(raw_acc.shape[0] + 1):
	if i - prev_i == spl[j]:
		prev_i = i
		j += 1
		spl2.append(len(new_raw_lab) - prev_len)
		prev_len = len(new_raw_lab)
	if i == raw_acc.shape[0]: break
	if raw_lab[i] in candidates:
		new_raw_acc.append(raw_acc[i])
		new_raw_lab.append(raw_lab[i])
print('spl2:', spl2)
raw_acc = np.array(new_raw_acc)
raw_lab = np.array(new_raw_lab)

print('raw_acc size:', raw_acc.shape)
print('raw_lab size:', raw_lab.shape)
print(raw_lab)

# spl2 = spl
dump_to_plain()