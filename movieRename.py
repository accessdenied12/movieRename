#!/usr/bin/env python
#


import shutil
import csv
import re
import time

destination = "/media/movies/"

def move(src, dest):
	shutil.move(src, dest)


with open('addons.csv', 'rb') as movies:
	reader = csv.reader(movies)
	for row in reader:
		moviePath =  row[1]
		movieName =  row[0]
		movieExtension = moviePath[-4:]
	        movieName = re.sub('/','-', movieName.rstrip())
		movieName = re.sub(',','', movieName.rstrip())
		movieName = re.sub('\'','', movieName.rstrip())
		movieName = re.sub(':',' -', movieName.rstrip())
		fullDest = destination+movieName+movieExtension
		print(fullDest)
		move(moviePath, fullDest)
		csvFile = open('output.csv', 'a')
		csvWriter = csv.writer(csvFile)
		csvData = [[moviePath, fullDest]]
		csvWriter.writerows(csvData)
		csvFile.close()
		time.sleep(1)

