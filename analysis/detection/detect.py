import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import random
import sys
import time
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import confusion_matrix
from utils import *

W = 60

def get_raw_data_per_file(filename):
	a, l = pickle.load(open(filename, 'rb'))
	raw_acc.append(a[::1])
	raw_label.append(l[::1])

# read tap
base_dir = '../recognition/pickle/'
datasets = [base_dir+'h/', base_dir+'v/']
raw_acc = []
raw_label = []
for dataset in datasets:
	filenames = os.listdir(dataset)
	for filename in filenames:
		if filename == '.DS_Store': continue
		get_raw_data_per_file(dataset + filename)
raw_acc = np.concatenate(raw_acc, axis=0)
raw_label = np.concatenate(raw_label, axis=0)
print('tap:', raw_label.shape[0])

# read noise
f_noise = 'log-20190813-140435-WatchL.txt'
f_noise = 'log-20190916-181651-WatchL.txt'
nacc, att, ngyr, que = read_file2(f_noise)

n_noise = raw_acc.shape[0] * 10
noise_len = min(nacc.shape[0], 100000)
data_noise = []
label_noise = []
for i in range(n_noise):
	x = random.randint(W//2, noise_len - W//2 - 1)
	data_noise.append( np.concatenate((nacc[x-W//2:x+W//2, 1:4], ngyr[x-W//2:x+W//2, 1:4]), axis=1) )
	label_noise.append(0)
data_noise = np.array(data_noise)
label_noise = np.array(label_noise)


def energy(x):
	e = 0
	for i in range(x.shape[0]):
		e += np.linalg.norm(x[i])
	return math.sqrt(e)

def zero_cross_rate(x):
	a = (x>0.1).astype(int)
	b = (x<-0.1).astype(int)
	c = a[1:] - b[:-1]
	n = x.shape[0] - 1
	return (n-len(np.nonzero(c-2)[0]) + n-len(np.nonzero(c+2)[0])) / (n+1)

def get_feature_axis(f, x):
	f.append(x.max())
	f.append(x.min())
	f.append(x.mean())
	f.append(x.std())
	f.append(energy(x))
	f.append(zero_cross_rate(x))

def get_feature(x):
	f = []
	for i in range(6):
		get_feature_axis(f, x[:, i])
	return f

data = np.concatenate((raw_acc, data_noise), axis=0)
label = np.concatenate(((raw_label > 0).astype(int), label_noise), axis=0)
feature = np.array([get_feature(data[i]) for i in range(data.shape[0])])

clf = svm.SVC()
# seed = int(time.time() * 1000000) % 2176783647
# cv = ShuffleSplit(n_splits=10, test_size=0.1, random_state=seed)
# score = cross_val_score(clf, feature, label, cv=cv)
# print(score)
# print(score.mean())

n = label.shape[0]
arr = list(range(n))
random.shuffle(arr)
feature = np.array([feature[arr[i]] for i in range(n)])
label = np.array([label[arr[i]] for i in range(n)])
ps = []
rs = []
for i in range(10):
	l = int(n/10*i)
	r = int(n/10*(i+1))
	feature_train = np.concatenate((feature[:l], feature[r:]), axis=0)
	label_train = np.concatenate((label[:l], label[r:]), axis=0)
	feature_test = feature[l:r]
	label_test = label[l:r]
	clf.fit(feature_train, label_train)
	pred = clf.predict(feature_test)
	tp = fp = fn = 0
	fps = []
	for i in range(label_test.shape[0]):
		if label_test[i] == 1 and pred[i] == 1: tp += 1
		if label_test[i] == 1 and pred[i] == 0: fn += 1
		if label_test[i] == 0 and pred[i] == 1:
			fp += 1
			# fps.append(data[i])
	ps.append( tp / (tp + fp) )
	rs.append( tp / (tp + fn) )
print(ps, np.array(ps).mean())
print(rs, np.array(rs).mean())

# fps = np.array(fps)
# print(fps.shape)
# f = open('noise.txt', 'w')
# f.write(str(fps.shape[0]) + ' ' + str(fps.shape[1]) + ' ' + str(fps.shape[2]) + '\n')
# for i in range(fps.shape[0]):
# 	for j in range(fps.shape[1]):
# 		for k in range(fps.shape[2]):
# 			f.write(str(fps[i, j, k]) + ' ')
# f.write('\n')
# f.close()
