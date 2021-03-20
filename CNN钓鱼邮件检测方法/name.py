import os
import csv
import re



filename = os.listdir(os.getcwd())
print (filename)
print("Reading all file names into a variable")
filename = sorted(filename)
print (filename)
print("Sorting the file names")

final = filename[1:]
#csv for filename
print(final)
print("Saving all file names into name.csv file")
with open('name.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for val in final:
        wr.writerow([val])

print("CSV file generated")


