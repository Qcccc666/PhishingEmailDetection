from sklearn import datasets, svm, metrics
from sklearn.metrics import roc_curve,auc,classification_report
from sklearn.naive_bayes import GaussianNB 
import sys
from flask import Flask
from flask import request, Response
import os
import numpy as np

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
#        lineArr.append(pre[a])
        FeatureMat.append(lineArr)
        LabelMat.append(-1)
#        a = a+1
    for line in fp.readlines():
        lineArr = line.strip().split(',')
#        lineArr.append(pre[a])
        FeatureMat.append(lineArr)
        LabelMat.append(1)
#        a = a+1
    return FeatureMat, LabelMat

def data_preprocess1(filename1, filename2,filename3):
    FeatureMat = []
    LabelMat = []
    pre = []
    a = 0
    ft = open(filename3)
    fr= open(filename1)
    fp = open(filename2)
    for line in ft.readlines():
        pre.append(line)
    for line in fr.readlines():
        lineArr = line.strip().split(',')
        lineArr.append(pre[a])
        FeatureMat.append(lineArr)
        LabelMat.append(-1)
        a = a+1
    for line in fp.readlines():
        lineArr = line.strip().split(',')
        lineArr.append(pre[a])
        FeatureMat.append(lineArr)
        LabelMat.append(1)
        a = a+1
    return FeatureMat, LabelMat

def Navie():
    target_names = ['phishing', 'legitimate']
    file1 = 'phishing.txt'
    file2 = 'legitimate.txt'
    file3='pre1.txt'
    print(file1)
    trainDataArr,trainLabelArr=data_preprocess(file1, file2)
    trainDataArr=np.array(trainDataArr,dtype = 'float_')
    mnb=GaussianNB()
    mnb.fit(trainDataArr,trainLabelArr)
    predicted = mnb.predict(trainDataArr)
    fpr, tpr, thresholds = roc_curve(trainLabelArr, predicted)
    roc_auc = auc(fpr, tpr)
    TP = np.sum(np.multiply(trainLabelArr, predicted))
    print(TP)
    print(tpr)
    print(fpr)
    print(roc_auc)
    score_train = mnb.score(trainDataArr, trainLabelArr)
    print("The train score is: %f" %score_train)
    print(classification_report(trainLabelArr, predicted))
    print(metrics.confusion_matrix(trainLabelArr, predicted))
    file3 = 'phishing_test.txt'
    file4 = 'legitimate_test.txt'
    file5='pre.txt'
    dataArr,labelArr = data_preprocess(file3, file4)
    dataArr=np.array(dataArr,dtype = 'float_')
    print(dataArr)
    predicted = mnb.predict(dataArr)
    fpr, tpr, thresholds = roc_curve(labelArr, predicted)
    roc_auc = auc(fpr, tpr)
    TP = np.sum(np.multiply(labelArr, predicted))
    print(TP)
    print(tpr)
    print(fpr)
    print(roc_auc)
    score_test = mnb.score(dataArr,labelArr)
    print("The score of rbf is : %f"%score_test)
    print(classification_report(labelArr, predicted))
    print(metrics.confusion_matrix(labelArr, predicted))
    return mnb

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
    mnb = Navie()
    app.run(host='0.0.0.0',port=int(port), debug=True)



    