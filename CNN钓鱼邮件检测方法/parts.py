import os
import csv
import mailparser
import subprocess

urlList=[]
flag=0
print("Reading all file names in sorted order")
dirname = 'E:\Projects\Detection-of-Phishing-Emails\spam/'
files = os.listdir(dirname)
for filename in files:
	count = 0
	if flag!=0:
		
		
		path1 = 'sudo mailparser -f '

		path2 = path1+filename

		

		pathb = path2+' -b'

		body = subprocess.check_output(pathb, shell=True)
		
		if body:
			count = count + 1

		patha = path2+' -a'
		attach = subprocess.check_output(patha, shell=True)
		if attach:
			count = count + 1

		patht = path2+' -t'
		to = subprocess.check_output(patht, shell=True)
		if to:
			count = count + 1

		pathdt = path2+' -dt'
		deliver = subprocess.check_output(pathdt, shell=True)
		if deliver:
			count = count + 1

		pathfrom = path2+' -m'
		from_ = subprocess.check_output(pathfrom, shell=True)
		if from_ :
			count = count + 1

		pathsub = path2+' -u'
		subject = subprocess.check_output(pathsub, shell=True)
		if subject:
			count = count + 1

		pathrec = path2+' -c'
		recv = subprocess.check_output(pathrec, shell=True)
		if recv:
			count = count + 1
		print "File Name = " + filename
		print "Number of parts= ",count
	urlList.append(count)
	flag = flag+1

finalurlList = urlList[1:]
print finalurlList


with open('parts.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for val in finalurlList:
        wr.writerow([val])


