from numpy import array
import matplotlib.pyplot as plt

#data = np.random.randn(10, 10)
data = array([x for x in range(100)]).reshape((10, 10))
data[0, 0] = 100

#fig = plt.figure()

plt.imshow(data, cmap='jet', interpolation='nearest')

#plt.imshow(data, cmap='jet', interpolation='nearest')

plt.show()
