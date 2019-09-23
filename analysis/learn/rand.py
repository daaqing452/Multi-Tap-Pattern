import random
import sys

n_block = 7

patterns = [
	'2-0-2', 	'3-0-3',	'4-0-4',	 '5-0-5', 		'23-0-23',
	'34-0-34',	'45-0-45',	'234-0-234', '345-0-345',	'2345-0-2345',
	'2-3',		'3-2',		'2-4', 		 '4-2',			'2-5',
	'5-2',		'3-4',		'4-3', 		 '2-3-4',		'4-3-2',
	'2-4-3',	'3-2-4',	'3-4-2', 	 '4-2-3',		'2-3-2',
	'3-2-3',	'2-4-2',	'4-2-4', 	 '2-5-2',		'5-2-5',
	'3-4-3',	'4-3-4'
]

a = list(range(len(patterns)))
username = sys.argv[1]
f = open('order-' + username + '.txt', 'w')
for i in range(n_block):
	random.shuffle(a)
	s = 'order ' + str(i) + '\n'
	for j in range(len(a)):
		s += patterns[a[j]] + '\t'
		if len(patterns[a[j]]) <= 7: s += '\t'
		if j % 5 == 4: s += '\n'
	print(s + '\n')
	f.write(str(a) + '\n')
f.close()
