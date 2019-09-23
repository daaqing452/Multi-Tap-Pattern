import matplotlib.pyplot as plt
import numpy as np

x = np.array([1,2,3,4,5])
y = np.array([
	[98.33, 1.25, 0,    0.42, 4.87],
	[97.92, 1.53, 0,    0.55, 5.42],
	[98.19, 1.39, 0,    0.42, 4.45],
	[97.92, 1.39, 0,    0.69, 5.28],
	[93.34, 3.33, 0.55, 2.77, 5.69],
	])

fig, ax = plt.subplots()
ax.set_ylim(80, 107)
r1 = ax.bar(x, y[:,0], width=0.5)
r2 = ax.bar(x, y[:,1], width=0.5, bottom=y[:,0])
r3 = ax.bar(x, y[:,2], width=0.5, bottom=y[:,0]+y[:,1])
r4 = ax.bar(x, y[:,3], width=0.5, bottom=y[:,0]+y[:,1]+y[:,2])
r5 = ax.bar(x, y[:,4], width=0.5, bottom=y[:,0]+y[:,1]+y[:,2]+y[:,3])
ax.set_xticklabels(['xx', 'BR1', 'BR2', 'BR3', 'BL', 'BI'])
ax.legend([r1, r2, r3, r4, r5], ['Success', 'Touch Error', 'Temporal Error', 'Spatial Error', 'Conscious Error'], loc='lower right', facecolor='white')

plt.show()