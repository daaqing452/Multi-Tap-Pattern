from utils import *
import pickle
import sys

patterns = [
	'2-0-2', 	'3-0-3',	'4-0-4',	 '5-0-5', 		'23-0-23',
	'34-0-34',	'45-0-45',	'234-0-234', '345-0-345',	'2345-0-2345',
	'2-3',		'3-2',		'2-4', 		 '4-2',			'2-5',
	'5-2',		'3-4',		'4-3', 		 '2-3-4',		'4-3-2',
	'2-4-3',	'3-2-4',	'3-4-2', 	 '4-2-3',		'2-3-2',
	'3-2-3',	'2-4-2',	'4-2-4', 	 '2-5-2',		'5-2-5',
	'3-4-3',	'4-3-4'
]

a, l = pickle.load(open(sys.argv[1], 'rb'))
print(a.shape, l.shape)
for k in range(0, a.shape[0], 2):
	plt.figure()
	plt.subplot(221)
	plt.plot(a[k,:,0:3])
	plt.subplot(223)
	plt.plot(a[k,:,3:6])
	print(patterns[l[k]])
	plt.subplot(222)
	plt.plot(a[k+1,:,0:3])
	plt.subplot(224)
	plt.plot(a[k+1,:,3:6])
	print(patterns[l[k+1]])
	plt.show()