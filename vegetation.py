latitude = "24.279174804687507"
import urllib2
import json
import numpy as np
np.set_printoptions(suppress=True)
import pandas as pd
import decimal
D = decimal.Decimal
longitude = "72.14477539062501"
latitude = "24.279174804687507"

def vegetation_outlier(latitude, longitude):
	url = "http://vedas.sac.gov.in:8080/LeanGeo/api/band_val/NDVI_PROBA?latitude="+latitude+"&longitude="+longitude
	response = urllib2.urlopen(url).read()
	json_response = json.loads(response)
	location_difference = []
	outliers = []
	for index in xrange(1,len(json_response)-1):
		value = json_response[index]["value"]
		difference = abs(json_response[index-1]["value"]-value) + abs(json_response[index+1]["value"]-value)
		location_difference.append(difference)
	
	location_difference_numpy = np.array(location_difference)
	mean_difference = np.mean(location_difference_numpy)
	std_difference = np.std(location_difference_numpy)
	#print location_difference_numpy
	for index, value in enumerate(location_difference):
		if value> (mean_difference + std_difference*2):
			outliers.append(index)
	return outliers

def moisture_outlier(latitude, longitude):
	url = "http://vedas.sac.gov.in:8080/LeanGeo/api/band_val/SMAP_SWI?latitude="+latitude+"&longitude="+longitude
	response = urllib2.urlopen(url).read()
	json_response = json.loads(response)
	outliers = []
	location_difference = []
	for index in xrange(1,len(json_response)-1):
		value = float(json_response[index]["value"])
		difference = abs(float(D(json_response[index-1]["value"]))-value) + abs(float(D(json_response[index+1]["value"]))-value)
		location_difference.append(difference)

	location_difference_numpy = np.array(location_difference)
	mean_difference = np.mean(location_difference_numpy)
	std_difference = np.std(location_difference_numpy)
	print location_difference
	for index, value in enumerate(location_difference):
		if value> (mean_difference + std_difference*2):	
			outliers.append(index+1)
	return outliers
'''
def area_data(latitude, longitude):
	latitude1 = float(latitude) + 0.01
	latitude2 = float(latitude) - 0.01
	longitude1 = float(longitude) + 0.01
	longitude2 = float(longitude) - 0.01
'''
