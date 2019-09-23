import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import math

f = open('subjective.csv', 'r')
a = [[[], [], [], [], []], [[], [], [], [], []]]
line = f.readline()
while True:
	line = f.readline()
	if len(line) == 0: break
	if line[-1] == '\n': line = line[:-1]
	arr = line.split(',')
	user = int(arr[0])
	group = int(arr[1])
	con = int(arr[3])
	und = int(arr[4])
	a[0][group].append(con)
	a[1][group].append(und)
f.close()

x = np.arange(1, 3)
fig, ax = plt.subplots()
colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd']
group_name = ['Double', '2-Sequential', '2-Sequential Chord', '3-Sequential', 'Alternate']

for j in range(len(group_name)):
	b0 = np.array(a[0][j])
	b1 = np.array(a[1][j])
	b0 = b0.reshape((1, b0.shape[0]))
	b1 = b1.reshape((1, b1.shape[0]))
	b = np.concatenate((b0, b1), axis=0)
	plt.bar(x+j*0.15, b.mean(axis=1), yerr=b.std(axis=1), width=0.15, label=group_name[j], color=colors[j])
plt.legend(loc='lower right', ncol=2, fontsize=12)
# ax.set_ylim(0, 5.9)
plt.yticks(size=15)
ax.set_xticks(x+0.3)
ax.set_xticklabels(['Comfort', 'Understandability'], fontsize=15)
plt.show()
