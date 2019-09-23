import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import math

n_user = 12
n_block = 5
n_t = 2
l_first = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
group_name = ['double', '2-seq-sin', '2-seq-mul', '3-seq', 'alter']
d_all = {}

def print_error(s, pattern, info):
	print(s + ': ' + pattern + '   ' + info)

def sort_coordinate(c):
	for i in range(len(c)):
		for j in range(i+1, len(c)):
			if c[i][0] > c[j][0]:
				temp = c[i]
				c[i] = c[j]
				c[j] = temp

def evaluate(group, pattern, taps, flag=False):
	pattern = pattern.replace('-0-', '-')
	stap = len(pattern) - pattern.count('-')
	if stap != len(taps):
		print('wrong tap number', pattern, str(stap) + ' ' + str(len(taps)))
		return [1]

	subpatterns = pattern.split('-')
	start = [0,]
	for subpattern in subpatterns:
		start.append(start[-1] + len(subpattern))

	for i in range(len(taps)):
		for j in range(i+1, len(taps)):
			if taps[i][0] > taps[j][0]:
				temp = taps[i]
				taps[i] = taps[j]
				taps[j] = temp

	re = []
	wti = -1e20
	iti = 1e20
	prev_down_t = 0
	wrong_c = None
	finger = [None, None, None, None, None, None]
	for i in range(len(subpatterns)):
		subpattern = subpatterns[i]
		min_start_t = 1e20
		max_start_t = -1e20
		c = []
		for j in range(start[i], start[i+1]):
			min_start_t = min(min_start_t, taps[j][0])
			max_start_t = max(max_start_t, taps[j][0])
			if flag:
				c.append([-taps[j][2], -taps[j][3]])
			else:
				c.append([taps[j][2], taps[j][3]])
		wti = max(wti, max_start_t - min_start_t)
		iti = min(iti, min_start_t - prev_down_t)
		prev_down_t = max_start_t

		sort_coordinate(c)
		for j in range(len(subpattern)):
			x = int(subpattern[j])
			for k in range(2, x):
				if finger[k] != None and (finger[k][0] > c[j][0]):
					wrong_c = 'seg='+str(i)+' fin='+str(x)+' '+str(finger[2:])+' '+str(c)
			for k in range(x+1, 6):
				if finger[k] != None and (finger[k][0] < c[j][0]):
					wrong_c = 'seg='+str(i)+' fin='+str(x)+' '+str(finger[2:])+' '+str(c)
		for j in range(len(subpattern)):
			x = int(subpattern[j])
			finger[x] = c[j]

	if iti < wti * 2:
		print_error('wti > iti', pattern, str(wti) + ' ' + str(iti))
		re.append(2)

	if wrong_c is not None:
		print_error('wrong_pos', pattern, str(wrong_c))
		re.append(3)

	return re

def read_analyze_file(filename, tgroup, idx):
	f = open('data/analysisData/' + filename, 'r')
	taps = []
	cnt = np.zeros((5, 4))
	while True:
		line = f.readline()
		if len(line) == 0: break
		arr = line[:-1].split(' ')
		if len(arr) == 1:
			if len(arr[0]) > 1:
				pattern = arr[0][1:]
				if not pattern in d_all: d_all[pattern] = np.zeros((n_t))
				arr = pattern.split('-')
				if len(arr) == 2:
					if len(arr[1]) == 1:
						group = 1
					else:
						group = 2
				elif arr[1] == '0':
					group = 0
				elif arr[0] == arr[2]:
					group = 4
				else:
					group = 3
			else:
				res = evaluate(group, pattern, taps, idx==3)
				if len(res) >= 2: print('oh my julia!!!!!!!!!!!!!!!!!!!!!!')
				for re in res: cnt[group, re] += 1
				if len(res) == 0: cnt[group, 0] += 1
				taps = []
		else:
			taps.append([int(arr[1])/1000, int(arr[4])/1000, (int(arr[2])+int(arr[5]))//2, (int(arr[3])+int(arr[6]))//2])
	f.close()
	return cnt

f = open('error_u.csv', 'w')
f.write('name,block,group,yes,err1,err2,err3\n')
cnt_all = np.zeros((5, 5, 4))
for u in range(n_user):
	order = list(range(n_block))
	if l_first[u] == 0:
		order[3] = 4
		order[4] = 3
	tu = []
	cnt_u = np.zeros((5, 5, 4))
	for i in range(5):
		print('user:', u, '   file:', i)
		tgroup = [[] for j in range(len(group_name))]
		cnt_u[i] = read_analyze_file(str(u) + '_' + str(order[i]) + 'Analyze.txt', tgroup, i)
	cnt_all += cnt_u

	for i in range(n_block):
		for j in range(5):
			f.write(str(u)+','+str(i)+','+str(j))
			for k in range(4):
				f.write(','+str(cnt_u[i, j, k]))
			f.write('\n')
print(cnt_all)
f.close()
