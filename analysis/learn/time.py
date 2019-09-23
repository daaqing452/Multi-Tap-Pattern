import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import math

n_user = 12
n_block = 5
n_t = 6
l_first = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
group_name = ['Double', '2-Sequential', '2-Sequential Chord', '3-Sequential', 'Alternate']
d_all = {}

def analysis_taps(group, pattern, taps):
	pattern = pattern.replace('-0-', '-')
	stap = len(pattern) - pattern.count('-')
	if stap != len(taps):
		return -1, -1, [], [], [], []

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

	itis = []
	itvs = []
	tds = []
	wtis = []
	prev_down_t = 0
	prev_up_t = 0
	start_t = 1e20
	end_t = -1e20
	for i in range(len(subpatterns)):
		subpattern = subpatterns[i]
		min_down_t = 1e20
		max_down_t = -1e20
		max_up_t = -1e20
		c = []
		for j in range(start[i], start[i+1]):
			min_down_t = min(min_down_t, taps[j][0])
			max_down_t = max(max_down_t, taps[j][0])
			max_up_t = max(max_up_t, taps[j][1])
			tds.append(taps[j][1] - taps[j][0])
		wtis.append(max_down_t - min_down_t)
		start_t = min(start_t, min_down_t)
		end_t = max(end_t, max_up_t)
		if i > 0:
			itis.append(min_down_t - prev_down_t)
			itvs.append(min_down_t - prev_up_t)
		prev_down_t = max_down_t
		prev_up_t = max_up_t
	return end_t - start_t, max_down_t - start_t, itis, itvs, tds, wtis


def read_analyze_file(filename):
	f = open('data/analysisData/' + filename, 'r')
	tg = [[[] for k in range(n_t)] for j in range(len(group_name))]
	taps = []
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
					if len(arr[0]) == 1 and len(arr[1]) == 1:
						group = 1
					else:
						group = 2
				elif arr[1] == '0':
					group = 0
				elif arr[0] == arr[2]:
					group = 4
				else:
					group = 3
				print(pattern, group)
			else:
				t0, t1, t2, t3, t4, t5 = analysis_taps(group, pattern, taps)
				if t0 > 0:
					tg[group][0].append(t0)
					tg[group][1].append(t1)
					tg[group][2].extend(t2)
					tg[group][3].extend(t3)
					tg[group][4].extend(t4)
					tg[group][5].extend(t5)
				taps = []
		else:
			taps.append([int(arr[1])/1000, int(arr[4])/1000])
	f.close()
	return tg

def plot_t_sub(t, x, i):
	ax = plt.subplot(1, n_t, i+1)
	ps = []
	for j in range(len(group_name)):
		p,  = ax.plot(x, t[:, j, i])
		ps.append(p)
	ax.set_xticks(x)
	ax.set_xticklabels(['r1', 'r2', 'r3', 'l', 'inv'])
	plt.legend(ps, group_name, loc='upper right')

def plot_t(t, title):
	plt.figure(title)
	x = list(range(1, n_block+1))
	for i in range(n_t):
		plot_t_sub(t, x, i)
	plt.show()

f = open('time.csv', 'w')
f.write('name,block,group,t0,t1,t2,t3,t4\n')
tall = [[[[] for k in range(n_t)] for j in range(len(group_name))] for i in range(5)]
for u in range(n_user):
	order = list(range(n_block))
	if l_first[u] == 0:
		order[3] = 4
		order[4] = 3
	for i in range(5):
		tg = read_analyze_file(str(u) + '_' + str(order[i]) + 'Analyze.txt')
		for j in range(len(group_name)):
			f.write(str(u)+','+str(i)+','+str(j))
			for k in range(n_t):
				f.write(','+str(np.array(tg[j][k]).mean()))
				tall[i][j][k].extend(tg[j][k])
			f.write('\n')
f.close()

err = np.zeros((5, len(group_name), n_t))
for i in range(5):
	for j in range(len(group_name)):
		for k in range(n_t):
			now = np.array(tall[i][j][k])
			tall[i][j][k] = now.mean()
			err[i, j, k] = now.std()
tall = np.array(tall)
x = np.arange(1, 6)
for k in range(n_t):
	if not (k == 0 or k == 2 or k == 4): continue
	fig, ax = plt.subplots()
	# plt.subplot(2, 2, k+1)
	colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd']
	for j in range(len(group_name)):
		plt.bar(x+j*0.15, tall[:, j, k], yerr=err[:, j, k], width=0.15, label=group_name[j], color=colors[j])
	plt.legend(loc='upper right', ncol=2, fontsize=9)
	ax.set_xticks(x+0.3)
	ax.set_xticklabels(['BR1', 'BR2', 'BR3', 'BL', "BI"])
plt.show()