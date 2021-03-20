from keras.models import Sequential, load_model
from keras.layers import Dense

import numpy as np

dataset = np.loadtxt('data.csv',delimiter=',')
print("dataset loaded")
X = dataset[:,1:6]
Y = dataset[:,6]

def kfold(k, X, y):
	test = []
	train = []
	test_y = []
	train_y = []
	for i in range(0, len(X)):
		if i%10==k:
			test.append(X[i])
			test_y.append(y[i])
		else:
			train.append(X[i])
			train_y.append(y[i])

	return np.array(train), np.array(test), np.array(train_y), np.array(test_y)


model = Sequential()
model.add(Dense(5,input_dim=5,activation='relu'))
model.add(Dense(10,activation='relu'))
model.add(Dense(1,activation='sigmoid'))

model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
print("model compiled")

accuracy_sum = 0
for i in range(0, 10):
	X_train, X_test, Y_train, Y_test = kfold(i, X, Y)
	model.fit(X_train,Y_train,epochs=10,batch_size=100,verbose=2)
	scores = model.evaluate(X_test,Y_test)
	#print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
	accuracy_sum = accuracy_sum + scores[1]*100

print("accuracy is ")
print(accuracy_sum/10.0)




	


