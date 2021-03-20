from sklearn import datasets, svm, metrics
from sklearn.metrics import roc_curve,auc,classification_report
import sys
from flask import Flask
from flask import request, Response
import os
import numpy as np
import time
from sklearn.externals import joblib

app = Flask(__name__)

def data_predict(filename):
    FeatureMat = []
    fr = open(filename)
    for line in fr.readlines():
        lineArr = line.strip().split(',')
        FeatureMat.append(lineArr)
    return FeatureMat

def data_preprocess(filename1, filename2):
    FeatureMat = []
    LabelMat = []
    fr= open(filename1)
    fp = open(filename2)
    for line in fr.readlines():
        lineArr = line.strip().split(',')
        FeatureMat.append(lineArr)
        LabelMat.append(-1)
    for line in fp.readlines():
        lineArr = line.strip().split(',')
        FeatureMat.append(lineArr)
        LabelMat.append(1)
    return FeatureMat, LabelMat

def svmMail(k1):
    file1 = 'phishing.txt'
    file2 = 'legitimate.txt'
    print(file1)
    start = time.process_time()
    trainDataArr,trainLabelArr=data_preprocess(file1, file2)
    #svc = SVC(kernel='rbf', gamma = 1.3)
    clf_rbf = svm.SVC(kernel='rbf',gamma=k1)
    clf_rbf.fit(trainDataArr,trainLabelArr)
    predicted = clf_rbf.predict(trainDataArr)
    end = time.process_time()
    print (end-start)
    fpr, tpr, thresholds = roc_curve(trainLabelArr, predicted)
    roc_auc = auc(fpr, tpr)
    TP = np.sum(np.multiply(trainLabelArr, predicted))
    print(TP)
    print(tpr)
    print(fpr)
    print(roc_auc)
    score_train = clf_rbf.score(trainDataArr, trainLabelArr)
    print(metrics.classification_report(trainLabelArr, predicted))
    print(metrics.confusion_matrix(trainLabelArr, predicted))
    print("The train score is: %f" %score_train)
#    for i in predicted:
#        if(i == -1):
#            print('0')
#        if(i == 1):
#            print('1')
    file3 = 'phishing_test.txt'
    file4 = 'legitimate_test.txt'
    start = time.process_time()
    dataArr,labelArr = data_preprocess(file3, file4)
    predicted = clf_rbf.predict(dataArr)
    fpr, tpr, thresholds = roc_curve(labelArr, predicted)
    roc_auc = auc(fpr, tpr)
    TP = np.sum(np.multiply(labelArr, predicted))
    print(TP)
    print(tpr)
    print(fpr)
    print(roc_auc)
    score_rbf = clf_rbf.score(dataArr,labelArr)
#    coef = clf_rbf.coef_
#    print(coef)
    print("The score of rbf is: %f"%score_rbf)
    end = time.process_time()
    print (end-start)
    print(metrics.classification_report(labelArr, predicted))
    print(metrics.confusion_matrix(labelArr, predicted))
#        if(i == -1):
#            print('0')
#        if(i == 1):
#            print('1')
    return clf_rbf




@app.route('/<path:path>')
def show_index(path):
    X_predict = []
    print(path)
    X_predict = data_predict(path)
    #X_predict = vectorizer.transform(X_predict)
    y_Predict = clf.predict(X_predict)
    if y_Predict == 1:
        result = 'good email'
    if y_Predict == -1:
        result = 'bad email'
    return '''
You asked for %s

AI output: %s 
 
''' % (path, str(result))    

port = os.getenv('VCAP_APP_PORT', 5000)

if __name__ == '__main__':
    gamma = 0.1
    print(gamma)
    clf = svmMail(gamma)
    app.run(host='0.0.0.0',port=int(port), debug=True)
