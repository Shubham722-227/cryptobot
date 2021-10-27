import numpy as np
import matplotlib.pyplot as plt


x = np.array([1, 2, 4, 2, 1])
y = np.array([1, 2, 3, 4, 5])

x = np.gradient(x)

print(x)

plt.plot(y, x)
plt.show()
