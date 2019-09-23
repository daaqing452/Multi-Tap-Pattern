import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from utils import *
from make_data import candidates

classes = ['2-0-2', '3-0-3', '4-0-4', '5-5', '23-0-23', '34-34', '45-45', '234-234', '345-345', '2345-0-2345', '2-3', '3-2', '2-4', '4-2', '2-5', '5-2', '3-4', '4-3', '2-3-4', '4-3-2', '2-4-3', '3-2-4', '3-4-2', '4-2-3', '2-3-2', '3-2-3', '2-4-2', '4-2-4', '2-5-2', '5-2-5', '3-4-3', '4-3-4']
show_classes = [classes[i] for i in candidates]

def load_cm():
	f = open('cm.txt', 'r')
	n = int(f.readline())
	res = []
	test_label = []
	for i in range(n):
		arr = f.readline().split(' ')
		res.append(int(arr[0]))
		test_label.append(int(arr[1]))
	f.close()
	return np.array(res), np.array(test_label)

def plot_res():
	print('acc = ', 1 - len(np.nonzero(res != test_label)[0]) / res.shape[0])
	cm = confusion_matrix(res, test_label)
	print(cm.shape)
	plot_confusion_matrix(cm, show_classes, axis_rotated=True, normalize=True)
	plt.show()


res, test_label = load_cm()
plot_res()