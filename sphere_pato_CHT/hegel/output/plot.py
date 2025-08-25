import numpy as np
import matplotlib.pyplot as plt


X = np.loadtxt('L2_convergence_NS.dat')


plt.figure()
plt.plot(X[:, 0], X[:, 1], label='L1')
plt.plot(X[:, 0], X[:, 2], label='L2')
plt.plot(X[:, 0], X[:, 3], label='L3')
plt.plot(X[:, 0], X[:, 4], label='L4')
plt.legend()
plt.show()

