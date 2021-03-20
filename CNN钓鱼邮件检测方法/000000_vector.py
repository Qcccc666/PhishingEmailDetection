import gensim
from nltk.corpus import brown
import os
import gensim.models.keyedvectors as word2vec
import numpy as np
import csv
final = []
print("Reading all files in sorted order...")
dirname = 'E:\Projects\Detection-of-Phishing-Emails\spam/'
files = os.listdir(dirname)
flag = 0
for x in files:
    if(flag==0):
        flag = flag+1
            
    else:
    	print("Filename :- ")
    	print(x)
        inputfile = open(dirname+x,'rb',encoding='UTF-8',errors='ignore')
        content = inputfile.read()
        inputfile.close()
        words = content.split()
        wor = np.unique(words)
        unique = list(wor)
        unique = np.array([s.decode(‘UTF-8’) for s in unique])

        if unique:
        	vector1 = []
        	flag1 = 0
        	model = gensim.models.Word2Vec([unique],min_count=1,size=32)
        	for y in unique:
        		vector = model[y]
        		vector1.append(vector)
        		flag1=flag1+1
        	avg = np.average(vector1)
        	final.append(avg)
        	print("Vector Average is ")
        	print(avg)
        else:
			avg = 0
			final.append(avg)
			print("Vector Average is ")
			print(avg)

with open('vector.csv','w') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	for val in final:
		wr.writerow([val])
