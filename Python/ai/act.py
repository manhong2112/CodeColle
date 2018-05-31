import numpy as np

def ReLU(x):
   return np.maximum(x, 0)

def clippedReLU(x, bound=1):
   return np.maximum(0, np.where(x > bound, bound, x))

def ReLU_D(x):
   return (x > 0).astype(int)

def LeakyReLU(x):
   a = np.where(x > 0, x, x * 0.01)
   np.maximum(a, 0, a)
   return a

def LeakyReLU_D(x):
   return np.where(x > 0, 1, 0.01)

def clippedLeakyReLU(x, bound=1):
   a = np.where(x > 0, x, x * 0.01)
   a = np.where(a > bound, bound, a)
   np.maximum(a, 0, a)
   return a

def tanh(x):
   return np.tanh(x)

def tanh_D(x):
    return 1.0 - np.tanh(x)**2

def sigmoid(x):
   return 1 / (1 + np.exp(-x))

def sigmoid_D(x):
   return x * (1 - x)
