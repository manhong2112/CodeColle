import numpy as np

def ReLU(x):
   return np.vectorize(lambda a: max(0, a))(x)

def ReLU_D(x):
   return np.vectorize(lambda a: 0 if a < 0 else 1)(x)

def sigmoid(x):
   return 1 / (1 + np.exp(-x))

def sigmoid_D(x):
   return x * (1 - x)

def clippedReLU(x, clipped=1):
   return np.vectorize(lambda a: min(1, max(0, a)))(x)

input_data = np.array([
   [1, 0, 1, 0, 1],
   [1, 1, 0, 0, 1],
   [0, 0, 1, 0, 1],
   [1, 1, 1, 1, 1],
   [0, 0, 0, 0, 1],
   [1, 0, 0, 0, 1],
   [0, 1, 0, 0, 1],
   [0, 0, 1, 0, 1],
   ])
output_data = np.array([[0, 1, 0, 1, 0, 0, 1, 0]]).T

weight = 2 * np.random.random((5, 1)) - 1

for i in range(100000):
   output = ReLU(np.dot(input_data, weight))
   loss = output_data - output
   weight += np.dot(input_data.T, loss * ReLU_D(output))

clippedReLU(np.dot(np.array([1, 0, 1, 0, 1]), weight))
