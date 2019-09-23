import numpy as np
import matplotlib.pyplot as plt
import sys

PLOT_USER = False
NSTD = 3
users = ['lyq', 'ycy', 'plh', 'xcn', 'lzp', 'yzc']
ges2tap = ['ycy-ges-day1', 'plh-ges-day1', 'yzc-ges-day1']
tap2ges = ['ycy-tap-day2']
special = ['yzc-tap-day1']
day2ignore = []
n_block = 4
n_cmd = 12

def read_memory(filename):
	f = open(filename, 'r')
	order = []
	times = []
	while True:
		line = f.readline()
		if len(line) == 0: break
		arr = line[:-1].split(' ')
		t = float(arr[0])
		op = arr[1]
		if op == 'start':
			t0 = t
		elif op == 'order':
			order.append( eval(' '.join(arr[2:])) )
		elif op == 'trial':
			times.append(t - t0)
	f.close()
	return times, order

def read_touch_tap(filename):
	f = open(filename, 'r')
	tap = []
	label = []
	while True:
		line = f.readline()
		if len(line) == 0: break
		arr = line[:-1].split(' ')
		op = arr[0]
		if op == 'start':
			t0 = float(arr[1])
		elif op == 'tap':
			tap.append([(float(arr[1]) - t0) / 1000, (float(arr[4]) - t0) / 1000])
		elif op == 'mark' or op == 'yes' or op == 'no':
			label.append([op])
	f.close()
	return tap, label

def read_touch_ges(filename):
	f = open(filename, 'r')
	ges = []
	label = []
	while True:
		line = f.readline()
		if len(line) == 0: break
		arr = line[:-1].split(' ')
		op = arr[0]
		if op == 'start':
			t0 = float(arr[1])
		if op == 'down':
			now = []
		elif op == 'up':
			ges.append( [now[0], now[-1]] )
		elif op == 'ges':
			now.append((float(arr[1]) - t0) / 1000)
		elif op == 'mark' or op == 'yes' or op == 'no':
			label.append([op])
	f.close()
	return ges, label

def get_perform_time(touch, tag):
	n_touch = len(touch)
	i = 0
	tinv_t = []
	while i < n_touch:
		j = i + 1
		while j < n_touch and touch[j][0] - touch[i][0] < 1: j += 1
		mint = 1e20
		maxt = -1e20
		for k in range(i, j):
			mint = min(mint, touch[k][0])
			maxt = max(maxt, touch[k][1])
		tinv_t.append(maxt - mint)
		i = j
	if tag == 'yzc-tap-day1':
		tinv_t = [0] * 13 + tinv_t
	if tag == 'fjy-ges-day1':
		tinv_t += [0]
	return np.array(tinv_t)

def get_reaction_time(touch, times, tag):
	n_touch = len(touch)
	p = 0
	react = []
	if tag == 'yzc-tap-day1':
		for i in range(n_touch): touch[i][0] += 200.742892
	for i in range(n_block * n_cmd * 2 - 1):
		now = []
		while p < n_touch and touch[p][0] > times[i] and touch[p][0] < times[i+1]:
			now.append(touch[p][0])
			p += 1
		if i % 2 == 0:
			if len(now) == 0:
				print('error tap 1', i)
				react.append(0)
			else:
				react.append(now[0] - times[i])
		else:
			if len(now) > 0:
				print('error tap 2', i)
	return np.array(react)

def remove_3std(a):
	while True:
		mean = a.mean()
		std = a.std()
		flag = False
		aa = []
		for i in range(a.shape[0]):
			if a[i] > mean + NSTD * std:
				flag = True
			else:
				aa.append(a[i])
		a = np.array(aa)
		if not flag: break
	return a

def split_block(a, a2, tag):
	mean = a2.mean()
	std = a2.std()
	ret = []
	for i in range(n_block):
		now = []
		for j in range(i * n_cmd, (i+1) * n_cmd):
			if a[j] > mean + NSTD * std:
				pass
			else:
				now.append(a[j])
		now = np.array(now)
		now.sort()

		print(tag, now)
		
		ret.append([now.mean(), now.std()])
	return np.array(ret)


if len(sys.argv) > 1:
	PLOT_USER = True
	users = [sys.argv[1]]


data = np.zeros((len(users), 2, 2, 8, 2))
for u in range(len(users)):
	user = users[u]
	for d in range(1, 3):
		print(d, user)
		if d == 2 and user in day2ignore: continue

		fname_t = user + '-tap-day' + str(d)
		fname_g = user + '-ges-day' + str(d)
		times_t, order_t = read_memory('data/' + user + '/memory-' + fname_t + '.txt')
		times_g, order_g = read_memory('data/' + user + '/memory-' + fname_g + '.txt')

		if fname_t in tap2ges:
			touch_t, label_t = read_touch_ges('data/' + user + '/touch-' + fname_t + '.txt')
		else:
			touch_t, label_t = read_touch_tap('data/' + user + '/touch-' + fname_t + '.txt')
		
		if fname_g in ges2tap:
			touch_g, label_g = read_touch_tap('data/' + user + '/touch-' + fname_g + '.txt')
		else:
			touch_g, label_g = read_touch_ges('data/' + user + '/touch-' + fname_g + '.txt')

		per_t = get_perform_time(touch_t, fname_t)
		per_g = get_perform_time(touch_g, fname_g)
		per_t2 = remove_3std(per_t)
		per_g2 = remove_3std(per_g)
		if PLOT_USER:
			plt.figure(user)
			plt.subplot(421)
			plt.hist(per_t, bins=20)
			plt.subplot(422)
			plt.hist(per_t2, bins=20)
			plt.subplot(423)
			plt.hist(per_g, bins=20)
			plt.subplot(424)
			plt.hist(per_g2, bins=20)

		rea_t = get_reaction_time(touch_t, times_t, fname_t)
		rea_g = get_reaction_time(touch_g, times_g, fname_g)
		rea_t2 = remove_3std(rea_t)
		rea_g2 = remove_3std(rea_g)
		if PLOT_USER:
			plt.subplot(425)
			plt.hist(rea_t, bins=20)
			plt.subplot(426)
			plt.hist(rea_t2, bins=20)
			plt.subplot(427)
			plt.hist(rea_g, bins=20)
			plt.subplot(428)
			plt.hist(rea_g2, bins=20)

		if per_t.shape[0] != 48: print(user + ' per_t error:', per_t.shape)
		if per_g.shape[0] != 48: print(user + ' per_g error:', per_g.shape)
		if rea_t.shape[0] != 48: print(user + ' rea_t error:', rea_t.shape)
		if rea_g.shape[0] != 48: print(user + ' rea_g error:', rea_g.shape)
		data[u, 0, 0, (d-1)*4:d*4] = split_block(per_t, per_t2, str(d) + ' tap per')
		data[u, 0, 1, (d-1)*4:d*4] = split_block(per_g, per_g2, str(d) + ' ges per')
		data[u, 1, 0, (d-1)*4:d*4] = split_block(rea_t, rea_t2, str(d) + ' tap rea')
		data[u, 1, 1, (d-1)*4:d*4] = split_block(rea_g, rea_g2, str(d) + ' ges rea')

f = open('tmp.csv', 'w')
for b in range(8):
	for t in range(2):
		f.write(str(b+1) + ',' + ('tap' if t == 0 else 'gesture') + ',' + str(data[u, 0, t, b, 0]) + ',' + str(data[u, 1, t, b, 0]) + '\n')
f.close()

plt.figure('perform_reaction_time')
plt.subplot(221)
plt.plot(data[:, 0, 0, :, 0].mean(axis=0), color='black')
plt.plot(data[:, 0, 1, :, 0].mean(axis=0))
plt.subplot(222)
plt.plot(data[:, 0, 0, :, 0].T, color='black')
plt.plot(data[:, 0, 1, :, 0].T)
plt.subplot(223)
plt.plot(data[:, 1, 0, :, 0].mean(axis=0), color='black')
plt.plot(data[:, 1, 1, :, 0].mean(axis=0))
plt.subplot(224)
plt.plot(data[:, 1, 0, :, 0].T, color='black')
plt.plot(data[:, 1, 1, :, 0].T)

plt.show()