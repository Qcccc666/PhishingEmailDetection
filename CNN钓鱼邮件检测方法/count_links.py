# -*- coding: utf-8 -*-
import os
import csv
import re

wordsInLine = []
tempWord = []
urlList = []


def count():
    flag = 0
    print("Reading all file names in sorted order")
    dirname = 'E:\Projects\Detection-of-Phishing-Emails\spam/'
    files = os.listdir(dirname)
    for filename in files:
        #open up the file containing the email
        file=open(dirname+filename, 'r',encoding='UTF-8',errors='ignore')
        count1 = 0
        for line in file:
            #create a list that contains is each word in each line
            
            wordsInLine = line.split(' ')
            #For each word try to split it with :
            for word in wordsInLine:
                
                if re.search('href="http',word,re.I):
                    count1=count1+1

        file.close()
        urlList.append(count1)
        if flag!=0:
            print ("File Name = " + filename)
            print ("Number of links = ",count1)
        flag = flag + 1

count()
final = urlList[1:]
print("List of number of links in each email")
print (final)

with open('count_links.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for val in final:
        #val.encode()
        wr.writerow([val])

print("CSV file generated")