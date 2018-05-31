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

output_data = np.array([[1, 0, 0, 0, 1, 1]]).T # [6, 1]

weight = [
   2 * np.random.random((4, 1)) - 1,
]

for i in range(0, 200000):
   output = [
      input_data # [6, 4]
   ]
   output.append(act(output[0].dot(weight[0]))) # [6, 4] . [0]

   delta0 = (output_data - output[1]) * act(output[1], d=True) # [6, 1] * [6, 1] = [6. 1]

   weight[0] += output[0].T.dot(delta0)

print(output[-1])
output = [
   np.array([[0, 0, 1, 0]])
]
output.append(act(output[0].dot(weight[0])))
print(output[-1])
