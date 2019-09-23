import matplotlib.pyplot as plt
from utils import *
import numpy as np
import wave
import math
import sys
import pickle

seg = None
ignores = [30,]
insert = []

def read():
	filename = 'log-pat*3'
	if len(sys.argv) >= 2:
		filename = sys.argv[1]

	acc, att, gyr, qua = read_file2(filename)
	acc = acc[:,1:]
	gyr = gyr[:,1:]

	acc = acc[20:]
	gyr = gyr[20:]

	return acc, gyr

def segment():
	global acc, gyr, ignore

	ACC_THRES = 0.09
	SIG_LEN = 25
	WIN = 60
	first = -1
	last = -100

	n = acc.shape[0]
	cnt = 0
	seg = np.zeros(n)
	acc_list = []
	idx_list = []
	for i in range(20, n-20):
		if np.abs(acc[i]).max() > ACC_THRES:
			if i - last > SIG_LEN:
				first = i
			last = i
		else:
			if i - last >= SIG_LEN and first != -1:
				mid = (first+last)//2
				if last - first > WIN:
					print('larger than win!', i, first, last)

				sgl = mid - WIN // 2
				sgr = mid + WIN // 2
				
				if sgl < 0 or sgr > n:
					print('out of index', i, first, last)
					first = -1
					continue

				print('(', first, last, '), [', sgl, sgr, ']')

				flag = False
				for ignore in ignores:
					if sgl <= ignore and sgr >= ignore:
						flag = True
				if flag:
					print('ignore', i)
					first = -1
					continue

				seg[sgl:sgr] = np.ones(WIN)
				acc_list.append( np.concatenate((acc[sgl:sgr], gyr[sgl:sgr]), axis=1) )
				idx_list.append( mid )
				first = -1
				cnt += 1

	for i in insert:
		acc_list.append( np.concatenate((acc[i-WIN//2:i+WIN//2], gyr[i-WIN//2:i+WIN//2]), axis=1) )
		idx_list.append( i )
		seg[i-WIN//2:i+WIN//2] = np.ones(WIN)

	n = len(acc_list)
	for i in range(n):
		for j in range(i+1,n):
			if idx_list[i] > idx_list[j]:
				tmp = idx_list[i]
				idx_list[i] = idx_list[j]
				idx_list[j] = tmp
				tmp = acc_list[i]
				acc_list[i] = acc_list[j]
				acc_list[j] = tmp

	print('seg:', len(acc_list))
	if len(sys.argv) >= 3:
		output_filename = sys.argv[2]
	else:
		output_filename = '0.pkl'
	pickle.dump( np.array(acc_list), open(output_filename, 'wb') )
	pickle.dump( np.array(idx_list), open('labelseg' + sys.argv[1][4:-4] + '.pkl', 'wb') )
	return seg

def plot():
	global acc, gyr, seg
	plt.subplot(311)
	plt.plot(acc)
	plt.subplot(312)
	plt.plot(gyr)
	if seg is not None:
		plt.subplot(313)
		plt.plot(seg)
	plt.show()

acc, gyr = read()
seg = segment()
plot()