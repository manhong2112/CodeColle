from numpy import exp, array, random, dot
traning_set_inputs = array([[1, 0, 1], [1, 1, 1], [1, 0, 0], [0, 1, 1], [0, 1, 0]])
traning_set_outputs = array([[1], [1], [0], [1], [0]])
random.seed(1)
synaptic_weights = 2 * random.random((3, 1)) - 1
for iteration in range(20000):
    output = 1 / (1 + exp(-(dot(traning_set_inputs, synaptic_weights))))
    synaptic_weights += dot(traning_set_inputs.T, (traning_set_outputs - output) * output * (1 - output))
print(1 / (1 + exp(-(dot(array([1, 1, 1]), synaptic_weights)))))
print(1 / (1 + exp(-(dot(array([0, 1, 0]), synaptic_weights)))))
print(1 / (1 + exp(-(dot(array([1, 0, 0]), synaptic_weights)))))