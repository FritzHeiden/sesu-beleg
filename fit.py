import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt

data = np.genfromtxt( 'xy.csv', names=None, skip_header=1, delimiter=',' )
xyData = np.transpose(data)

xvals = xyData[0]
yvals = xyData[1]

fit = np.poly1d( np.polyfit( xvals, yvals, 3 ) ) # 3rd argument is the order of the polynomial
print(fit)

plt.plot( xvals, yvals, 'bo' )
plt.plot( xvals, fit(xvals), 'k-' )
plt.show()

