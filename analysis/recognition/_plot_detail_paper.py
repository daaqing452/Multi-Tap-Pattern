import matplotlib.pyplot as plt
from utils import *
import numpy as np
import wave
import math
import sys
import pickle

seg = None
ignores = [30,]
insert = []

def read():
	filename = 'log-pat*3'
	if len(sys.argv) >= 2:
		filename = sys.argv[1]
	acc, att, gyr, qua = read_file2(filename)
	acc = acc[:,1:]
	gyr = gyr[:,1:]
	acc = acc[20:]
	gyr = gyr[20:]
	return acc, gyr

acc, gyr = read()
s0 = [840, 930]
s1 = [1110, 1200]
acc0 = acc[s0[0]:s0[1]]
gyr0 = gyr[s0[0]:s0[1]]
acc1 = acc[s1[0]:s1[1]]
gyr1 = gyr[s1[0]:s1[1]]

fig, ax = plt.subplots(2, 2)
tick_size = 9
y_label_size = 12
x_label_size = 14

ax[0][0].set_ylim(-0.8, 0.8)
ax[0][1].set_ylim(-0.8, 0.8)
ax[1][0].set_ylim(-2, 2)
ax[1][1].set_ylim(-2, 2)
ax[0][0].set_ylabel('Accelerometer', size=y_label_size)
ax[1][0].set_ylabel('Gyroscope', size=y_label_size)
ax[1][0].set_xlabel('2345-0-2345', size=x_label_size)
ax[1][1].set_xlabel('2-3', size=x_label_size)

ax[0][0].xaxis.set_ticks_position('top')
ax[0][1].xaxis.set_ticks_position('top')
for tick in ax[0][0].xaxis.get_major_ticks():
	tick.label.set_fontsize(tick_size)
for tick in ax[0][1].xaxis.get_major_ticks():
	tick.label.set_fontsize(tick_size)
ax[1][0].set_xticks([])
ax[1][1].set_xticks([])


ax[0][0].set_yticks([])
ax[1][0].set_yticks([])
ax[0][1].yaxis.set_ticks_position('right')
ax[1][1].yaxis.set_ticks_position('right')
for tick in ax[0][1].yaxis.get_major_ticks():
	tick.label.set_fontsize(tick_size)
for tick in ax[1][1].yaxis.get_major_ticks():
	tick.label.set_fontsize(tick_size)

ax[0][0].plot(acc0)
ax[0][1].plot(acc1)
ax[1][0].plot(gyr0)
r0, = ax[1][1].plot(gyr1[:,0])
r1, = ax[1][1].plot(gyr1[:,1])
r2, = ax[1][1].plot(gyr1[:,2])
ax[1][1].legend([r0, r1, r2], ['X', 'Y', 'Z'], loc='lower right')

plt.show()