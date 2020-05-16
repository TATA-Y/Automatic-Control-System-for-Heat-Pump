import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


x = [20, 24, 27, 33, 40, 45, 50, 55, 60]
y = [0.6, 0.72, 0.78, 0.86, 0.89, 0.88, 0.86, 0.84, 0.82]
x = np.array(x)
y = np.array(y)
f1 = np.polyfit(x, y, 3)
print('f1 is :\n', f1)
p1 = np.poly1d(f1)
print('p1 is :\n', p1)
yvals = np.polyval(f1, x)
plot1 = plt.plot(x, y, 's', label='original point')
plot2 = plt.plot(x, yvals, 'r', label='polyfit')
plt.xlabel('T out')
plt.ylabel('efficiency')
plt.legend(loc=4)
plt.title('Temperature Vs efficiency')
plt.show()
