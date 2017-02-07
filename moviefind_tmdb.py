#!/usr/bin/env python
#
#
import os
import re
import json
import urllib
import csv
import time

#Extensions we want to parse
goodExt = (".avi",".m2ts",".mkv",".mp4")


#Takes the input passed runs it through the Open Movie Database API and resturns the movie name
def getImdbResponse(title):
	apiKey = "asdf12341234"
	titleSplit = title.split()
	count = len(titleSplit)
	while count > 0:
		words = titleSplit[:count]	
		encoded = urllib.quote(str(words))
		print(str(words))
		imdbApi = "https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s&page=1&include_adult=false" % (apiKey, str(words))
      		imdbResponse = urllib.urlopen(imdbApi)
	    	imdbJson = imdbResponse.read()
	        imdbDetails = json.loads(imdbJson)
		#print(imdbDetails)
		if imdbDetails['total_results'] == 0:
                	count -= 1
			time.sleep(1)
	        else:
                	movietitle = imdbDetails['results'][0]['title']
                	print(movietitle)
                	count = 0
			return movietitle
			time.sleep(1)
	        

#Parses all the paths/dirnames/files recursively from /media/movies then iterates through the list and if it finds files with the good extension and removes some useless info, then calls getImdbResponse, when it gets a response it stores it in a csv file.
for dirpath, dirnames, files in os.walk("/media/movies"):
       for filename in files:
         if filename.endswith(goodExt):
                moviePath = (os.path.join(dirpath, filename))
		filename = re.sub(r'^([a-zA-Z]+?-)',' ', filename)
                filename = re.sub('\W', ' ', filename)
                #filename = re.sub(r"\D(\d{4})\D",' ', filename) #Replaces sets of four numbers with a space
                #filename = re.sub(r"\D(\d{3})\D",' ', filename) #Replaces sets of three numbers with a space
		filename = re.sub('.avi',' ', filename.rstrip(), flags=re.IGNORECASE) #all the below replace w space
		filename = re.sub('.mp4',' ', filename.rstrip(), flags=re.IGNORECASE) 
		filename = re.sub('.mkv',' ', filename.rstrip(), flags=re.IGNORECASE)
		filename = re.sub('AC3',' ', filename.rstrip(), flags=re.IGNORECASE)
		filename = re.sub('DVDRIP',' ', filename.rstrip(), flags=re.IGNORECASE)
		filename = re.sub('1080p',' ', filename.rstrip(), flags=re.IGNORECASE)
		filename = re.sub('720p',' ', filename.rstrip(), flags=re.IGNORECASE)
		file = str(filename)
		print file
		if "sample" not in filename.lower():
			movieDetails = getImdbResponse(file)
	                print(moviePath)
			movieName = movieDetails 
			csvFile = open('addons.csv', 'a')
			csvWriter = csv.writer(csvFile)
			csvData = [[movieName, moviePath]]
			csvWriter.writerows(csvData)
			csvFile.close()
