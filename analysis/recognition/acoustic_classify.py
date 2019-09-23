import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import time
from python_speech_features import mfcc, logfbank, delta
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import confusion_matrix

fs = 44100

def get_raw_data_per_file(filename):
	a, w, l = pickle.load(open(filename, 'rb'))
	raw_acc.append(a)
	raw_wav.append(w)
	raw_label.append(l)

dataset_names = ['vr']
raw_acc = []
raw_wav = []
raw_label = []
for dataset_name in dataset_names:
	for i in range(10):
		# filename = 'pickle2/' + dataset_name + '-' + str(i) + '.pkl'
		filename = 'pickle/' + dataset_name + '/' + dataset_name + str(i) + '.pkl'
		if os.path.isfile(filename):
			get_raw_data_per_file(filename)
raw_acc = np.concatenate(raw_acc, axis=0)
raw_wav = np.concatenate(raw_wav, axis=0)
raw_label = np.concatenate(raw_label, axis=0)
print('raw_acc size:', raw_acc.shape)
print('raw_wav size:', raw_wav.shape)
print('raw_label size:', raw_label.shape)
print(len(set(raw_label)), ':', set(raw_label))


n = raw_label.shape[0]
data = []
label = raw_label
for i in range(n):
	if i % 10 == 0:
		print("making features " + str(i))
	feature_mfcc = mfcc(raw_wav[i], fs, winlen=1, nfft=fs)
	feature_mfcc_d = delta(feature_mfcc, 2)
	feature_mfcc_dd = delta(feature_mfcc_d, 2)
	f_mfcc = np.column_stack((feature_mfcc, feature_mfcc_d, feature_mfcc_dd))[0]
	data.append(f_mfcc)

clf = svm.SVC()
seed = int(time.time() * 1000000) % 2176783647
cv = ShuffleSplit(n_splits=10, test_size=0.1, random_state=seed)
score = cross_val_score(clf, data, label, cv=cv)
print(score)
print(score.mean())