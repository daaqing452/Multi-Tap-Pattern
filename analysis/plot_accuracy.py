import matplotlib.pyplot as plt
import numpy as np

x = np.array([0, 1, 2, 3])
acc = np.array([[91.5, 67.4, 98.3, 90.3], [92.1, 56.0, 98.0, 82.8]])
std = np.array([[5.5, 0, 1.9, 0], [7.1, 0, 3.0, 0]])
w = 0.4

tick_size = 12
label_size = 14

fig, ax = plt.subplots()
plt.grid(True)
b1 = ax.bar(x+w*0, acc[0], yerr=std[0], width=w)
b2 = ax.bar(x+w*1, acc[1], yerr=std[1], width=w)
ax.legend([b1,b2], ['Table', 'HMD'], loc='lower right', fontsize=label_size)
ax.set_xticks(x+w*0.5)
plt.yticks(size=tick_size)
ax.set_xticklabels(['User-specific', 'General', 'User-specific', 'General'], size=tick_size)
plt.title('12 patterns                          5 patterns', size=label_size)
# fig.set_size_inches(6, 3)
plt.show()