from sklearn import svm
from sklearn import linear_model as lmdl
from sklearn import neural_network as nn
from sklearn import datasets
from sklearn import tree
from sklearn import neighbors
from sklearn import ensemble

mdls = [
   ("KNeighborsClassifier", neighbors.KNeighborsClassifier()),
   ("SVC", svm.SVC()),
   ("Linear SVC", svm.SVC(kernel='linear')),
   ("MLPClassifier", nn.MLPClassifier()),
   ("DecisionTreeClassifier", tree.DecisionTreeClassifier()),
   ("RandomForestClassifier", ensemble.RandomForestClassifier()), 
   ("AdaBoostClassifier", ensemble.AdaBoostClassifier()),
]

digits = datasets.load_digits()
data = digits.data[:1000]
target = digits.target[:1000]
predict = digits.data[1000:]
pTarget = digits.target[1000:]

# for i in range(1000):
#    data.append([i])
#    target.append(1 if i & 1 == 1 else 0)

for name, mdl in mdls:
   mdl.fit(data, target)

for name, mdl in mdls:
   total = len(pTarget)
   passed = 0
   for res, target in zip(mdl.predict(predict),  pTarget):
      if res == target:
         passed += 1
   print(f"{name} Passed: {passed} in {total}")

"""
KNeighborsClassifier Passed: 763 in 797
SVC Passed: 256 in 797
Linear SVC Passed: 751 in 797
MLPClassifier Passed: 732 in 797
DecisionTreeClassifier Passed: 610 in 797
RandomForestClassifier Passed: 709 in 797
AdaBoostClassifier Passed: 211 in 797
"""