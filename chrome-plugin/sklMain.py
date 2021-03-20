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
    file1 = './train/phishing.txt'
    file2 = './train/normal.txt'
    print(file1)
    start = time.process_time()
    trainDataArr,trainLabelArr=data_preprocess(file1, file2)
    #svc = SVC(kernel='rbf', gamma = 1.3)
    clf_rbf = svm.SVC(kernel='rbf',gamma=k1)
    clf_rbf.fit(trainDataArr,trainLabelArr)
    return clf_rbf

def predict(path):
    X_predict = data_predict(path)
    update(0.1)
    clf = joblib.load('svm.pkl')
    y_Predict = clf.predict(X_predict)
    print(y_Predict)
    if y_Predict == 1:
        result = "Good email"
    if y_Predict == -1:
        result = "phishing email"
    return result

def update(k1):
    DIR = './email/' #要统计的文件夹
    number = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    print('number')
    print(number)
    if number % 20 == 1:
        file1 = './train/phishing.txt'
        file2 = './train/normal.txt'
        #print(file1)
        start = time.process_time()
        trainDataArr,trainLabelArr=data_preprocess(file1, file2)
    #svc = SVC(kernel='rbf', gamma = 1.3)
        clf_rbf = svm.SVC(kernel='rbf',gamma=k1)
        clf_rbf.fit(trainDataArr,trainLabelArr)
        joblib.dump(clf_rbf, 'svm.pkl')
        # updt = 1
        print("update")
    else:
        print("No update")