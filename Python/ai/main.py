import numpy as np

def act(x, d=False):
   import act
   if d:
      return act.sigmoid_D(x)
   return act.sigmoid(x)

input_data = np.array([
   [1, 0, 0, 0],
   [0, 1, 0, 0],
   [0, 0, 1, 1],
   [0, 1, 1, 0],
   [1, 1, 1, 0],
   [1, 0, 1, 0],
])

output_data = np.array([[1, 1, 0, 1, 0, 1]]).T

weight = [
   2 * np.random.random((4,5)) - 1,
   2 * np.random.random((5,5)) - 1,
   2 * np.random.random((5,5)) - 1,
   2 * np.random.random((5,1)) - 1,
]

for i in range(0, 100000):
   output = [
      input_data # [6, 3]
   ]
   for a in range(len(weight)):
      output.append(act(output[a].dot(weight[a])))

   delta0 = (output_data - output[4]) * act(output[4], d=True) # [6, 1] * [6, 1] = [6. 1]
   delta1 = delta0.dot(weight[3].T) * act(output[3], d=True) # [6. 10] . [10, 1]
   delta2 = delta1.dot(weight[2].T) * act(output[2], d=True) # [6. 10] . [10, 1]
   delta3 = delta2.dot(weight[1].T) * act(output[1], d=True)

   weight[3] += output[3].T.dot(delta0)
   weight[2] += output[2].T.dot(delta1)
   weight[1] += output[1].T.dot(delta2)
   weight[0] += output[0].T.dot(delta3)

print(output[-1])
output = [
   np.array([[0, 0, 1, 0]])
]
for i in range(4):
   output.append(act(output[i].dot(weight[i])))
print(output[-1])

class Node():
   def __init__(self, i, o):
      self.weight = 2 * np.random.random((i, o)) - 1

   def predict(self, data):
      return act(np.dot(data, self.weight))

   def train(self, data, target):
      output = self.predict(data)
      error = target - output
      delta = error * act(output, true)
      self.weight += data.T.dot(delta)
