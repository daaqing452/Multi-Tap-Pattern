import numpy as np
import matplotlib.pyplot as plt

# block, tech
pm = np.array([[0.690, 0.221], [0.690, 0.253], [0.691, 0.253], [0.656, 0.257],
	[0.694, 0.259], [0.681, 0.262], [0.673, 0.264], [0.620, 0.259]])
pe = np.array([[0.188, 0.091], [0.159, 0.055], [0.143, 0.048], [0.141, 0.050],
	[0.178, 0.058], [0.171, 0.054], [0.165, 0.058], [0.147, 0.054]])

rm = np.array([[2.092, 2.230], [2.036, 2.316], [2.134, 2.200], [1.848, 2.107],
	[2.449, 2.832], [1.806, 2.467], [1.761, 2.281], [1.739, 1.913]])
re = np.array([[0.571, 0.887], [0.681, 0.585], [0.935, 0.675], [0.541, 0.619],
	[0.888, 0.944], [0.493, 1.053], [0.622, 0.948], [0.667, 0.616]])

te = np.array([[0.711, 0.953], [0.785, 0.597], [1.019, 0.662], [0.563, 0.602],
	[0.943, 0.979], [0.537, 1.066], [0.642, 0.978], [0.670, 0.614]])

fig, ax = plt.subplots()

x = np.array(list(range(1, 9)))
a1 = ax.errorbar(x, pm[:,1], fmt='.-', color='#1f77b4')
a2 = ax.errorbar(x, pm[:,0], fmt='.-', color='#ff7f0e')
a3 = ax.errorbar(x, rm[:,1], fmt='o-', color='#1f77b4')
a4 = ax.errorbar(x, rm[:,0], fmt='o-', color='#ff7f0e')
a5 = ax.errorbar(x, pm[:,1]+rm[:,1], fmt='x-', color='#1f77b4')
a6 = ax.errorbar(x, pm[:,0]+rm[:,0], fmt='x-', color='#ff7f0e')
ax.set_ylabel('Time (s)')

# x = [1]
# a1 = ax.errorbar(x, [1], fmt='.-', color='#1f77b4')
# a2 = ax.errorbar(x, [1], fmt='.-', color='#ff7f0e')
# a3 = ax.errorbar(x, [1], fmt='o-', color='#1f77b4')
# a4 = ax.errorbar(x, [1], fmt='o-', color='#ff7f0e')
# a5 = ax.errorbar(x, [1], fmt='x-', color='#1f77b4')
# a6 = ax.errorbar(x, [1], fmt='x-', color='#ff7f0e')
# ax.legend([a1, a2, a3, a4, a5, a6], ['PT Multi-Tap', 'PT Handwriting', 'RT Multi-Tap', 'RT Handwriting', 'TT Multi-Tap', 'TT Handwriting'], loc='lower right')
# ax.set_xticks([1,2,3,4,5])

ax.set_xticklabels(['xx', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'])
plt.show()