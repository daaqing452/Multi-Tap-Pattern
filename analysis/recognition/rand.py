import random
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

if len(sys.argv) >= 4 and sys.argv[3] == 'all':
	candidates = list(range(len(patterns)))
else:
	candidates = [0, 1, 2, 4, 9, 10, 11, 12, 13, 18, 19, 20, 23, 24, 25, 26, 27]
	candidates = [0, 1, 2, 4, 9, 10, 11, 19, 21, 25, 26, 27]

a = candidates
username = sys.argv[1]
place = sys.argv[2]
f = open('order/order-' + username + '-' + place + '.txt', 'w')
for i in range(10):
	random.shuffle(a)
	s = 'order ' + str(i) + '\n'
	for j in range(len(a)):
		s += patterns[a[j]] + '\t'
		if len(patterns[a[j]]) <= 7: s += '\t'
		if j % 5 == 4: s += '\n'
	print(s + '\n')
	f.write(str(a) + '\n')
f.close()
