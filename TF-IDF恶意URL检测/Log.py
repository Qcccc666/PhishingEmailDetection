from functools import wraps
from flask import Flask
from flask import request, Response
from subprocess import call
from flask import render_template

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import os
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve,auc,classification_report
import math
from collections import Counter
from sklearn import datasets, svm, metrics

app = Flask(__name__)


def entropy(s):
	p, lns = Counter(s), float(len(s))
	return -sum( count/lns * math.log(count/lns, 2) for count in p.values())

def getTokens(input):
	tokensBySlash = str(input.encode('utf-8')).split('/')	
	allTokens = []
	for i in tokensBySlash:
		tokens = str(i).split('-')
		tokensByDot = []
		for j in range(0,len(tokens)):
			tempTokens = str(tokens[j]).split('.')	
			tokensByDot = tokensByDot + tempTokens
		allTokens = allTokens + tokens + tokensByDot
	allTokens = list(set(allTokens))	
	if 'com' in allTokens:
		allTokens.remove('com')	#
	return allTokens

def TL():
	allurls = './data/data.csv'	#path to our all urls file
	allurlscsv = pd.read_csv(allurls,',',error_bad_lines=False)	#reading file
	allurlsdata = pd.DataFrame(allurlscsv)	#converting to a dataframe

	allurlsdata = np.array(allurlsdata)	#converting it into an array
	random.shuffle(allurlsdata)	

	y = [d[1] for d in allurlsdata]	 
	corpus = [d[0] for d in allurlsdata]	
	vectorizer = TfidfVectorizer(tokenizer=getTokens)	#get a vector for each url but use our customized tokenizer
	print("******")
	print(vectorizer)
	X = vectorizer.fit_transform(corpus)	#get the X vector

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)	#split into training and testing set 80/20 ratio
	# print("x")
	# print(X_train)
	#print("y")
	#print(y_train)
	lgs = LogisticRegression()	
	lgs.fit(X_train, y_train)
	print(lgs.score(X_test, y_test))	
	predicted = lgs.predict(X_test)
	print(metrics.classification_report(y_test, predicted))
	print(metrics.confusion_matrix(y_test, predicted))
	return vectorizer, lgs

@app.route('/<path:path>')
def show_index(path):
	X_predict = []
	X_predict.append(str(path))
	print(X_predict)
	print('*****')
	X_predict = vectorizer.transform(X_predict)
	print(X_predict)
	print('-----')
	y_Predict = lgs.predict(X_predict)
	print("///")
	print(y_Predict)
	return '''
You asked for %s

AI output: %s 
Entropy: %s 
''' % (path, str(y_Predict), str(entropy(path)))	

port = os.getenv('VCAP_APP_PORT', 5000)
if __name__ == "__main__":
	vectorizer, lgs  = TL()
	t1 = getTokens('wikipedia.com')
	print(t1)
	t1 = getTokens('google.com/search=faizanahad')
	print(t1)
	t1 = getTokens('pakistanifacebookforever.com/getpassword.php/')
	print(t1)
	app.run(host='0.0.0.0',port=int(port), debug=True)


