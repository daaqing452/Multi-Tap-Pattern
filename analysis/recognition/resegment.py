import numpy as np
import pickle
from utils import *
import sys
import os

def read(filename):
	acc, att, gyr, qua = read_file2(filename)
	acc = acc[:,1:]
	gyr = gyr[:,1:]
	acc = acc[20:]
	gyr = gyr[20:]
	return acc, gyr

name = sys.argv[1]
filenames = os.listdir('data/' + name)
filenames.sort()
w = int(sys.argv[2])
for k in range(len(filenames)):
	filename = filenames[k]
	if filename == '.DS_Store':
		continue
	print(k, filename)
	acc, gyr = read('data/' + name + '/' + filename)
	idxs = pickle.load(open('labelseg/' + name + '/' + filename[:-4] + '.pkl', 'rb'))
	acc_list = []
	for i in idxs:
		acc_list.append( np.concatenate( (acc[i-w//2:i+w//2], gyr[i-w//2:i+w//2]), axis=1 ) )
	acc_list = np.array(acc_list)
	pickle.dump(acc_list, open(str(k) + '.pkl', 'wb'))
