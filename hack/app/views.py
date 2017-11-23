from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
import re
from models import Farmer, BorrowTractor, LendTractor, Location, Crop, Truck, Order, FarmerDemand, recommendedCrops
from twilio.rest import TwilioRestClient 
import urllib2
import numpy as np
import requests
import json
from scipy import asarray as ar
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scipy.signal import find_peaks_cwt
import matplotlib.pyplot as plt
import pandas
from math import pow, atan2, radians, sin, cos, sqrt
# Create your views here.

import json
from math import radians, asin, sin, cos, sqrt, ceil
from operator import itemgetter

def send_sms(message,number):
	number = number[3:]
	print number
	key = " YOUR KEY HERE "
	urltosend = 'https://control.msg91.com/api/sendhttp.php?authkey='+key+'&mobiles='+number+'&message='+message+'&sender=MSGIND&route=4'
	response = urllib2.urlopen(urltosend).read()
	print response

@csrf_exempt
def sms(request):
	print request.body
	sms_body = request.POST.get('Body')
	sms_id = request.POST.get('SmsMessageSid')
	sender,body = retrieve_messages(sms_id)
	list_of_numbers = re.findall('\\b\\d+\\b', body)
	
	if 'available' in body:
		lending = LendTractor.objects.create()
		lending.quantity = str(list_of_numbers[0])
		lending.date = str(list_of_numbers[1])
		lending.from_time = str(list_of_numbers[2])
		lending.to_time = str(list_of_numbers[3])
		lending.number = str(sender)
		farmer_number = str(sender)
		lending.fullfilled = str(0)
		lending.save()
		needed_tractors = BorrowTractor.objects.all()
		for tractor in needed_tractors:
			if tractor.quantity <= lending.quantity and tractor.date == lending.date and tractor.from_time >= lending.from_time and tractor.to_time <= lending.to_time and tractor.fullfilled=="0":
				lender_farmer = Farmer.objects.get(number=farmer_number)
				borrower_farmer_number = tractor.number
				borrower_farmer = Farmer.objects.get(number=borrower_farmer_number)
				distance = get_distance(lender_farmer.lat, lender_farmer.lng, borrower_farmer.lat, borrower_farmer.lng)
				distance = (ceil(distance*100)/100) 
				borrower_text = 'THE FARMER IS' + str(distance) + ' KM away. Number is =  ' + str(lender_farmer.number) 
				lender_text = 'THE FARMER IS'   + str(distance) + ' KM away. Number is =  ' + str(borrower_farmer.number)
				borrower_farmer.fullfilled = "1"
				borrower_farmer.save()
				lender_farmer.fullfilled = "1"
				lender_farmer.save()
				send_sms(borrower_text,borrower_farmer.number)
				send_sms(lender_text,lender_farmer.number)
				break

	elif 'needed' in body:
		print ' IN NEEDED CONDITION '
		borrow = BorrowTractor.objects.create()
		borrow.quantity = str(list_of_numbers[0])
		borrow.date = str(list_of_numbers[1])
		borrow.from_time = str(list_of_numbers[2])
		borrow.to_time = str(list_of_numbers[3])
		borrow.number = str(sender)
		borrow.fullfilled = str(0)
		farmer_number = str(sender)
		borrow.save()
		lending_tractors = LendTractor.objects.all()
		for tractor in lending_tractors:
			if tractor.quantity >= borrow.quantity and tractor.date == borrow.date and tractor.from_time <= borrow.from_time and tractor.to_time >= borrow.to_time and tractor.fullfilled=="0":
				print 'LOGIC PASSED'
				borrower_farmer = Farmer.objects.get(number=farmer_number)
				lender_farmer_number = tractor.number
				lender_farmer = Farmer.objects.get(number=lender_farmer_number)
				distance = get_distance(lender_farmer.lat, lender_farmer.lng, borrower_farmer.lat, borrower_farmer.lng)
				distance = (ceil(distance*100)/100) 
				print distance
				borrower_text = 'THE FARMER IS  ' + str(distance) + ' KM away. Number is =  ' + str(lender_farmer.number) 
				lender_text = 'THE FARMER IS  ' + str(distance) + ' KM away. Number is =  '+ str(borrower_farmer.number)
				lender_farmer.fullfilled = "1"
				lender_farmer.save()
				borrower_farmer.fullfilled = "1"
				borrower_farmer.save()
				print borrower_farmer.fullfilled
				print lender_farmer.fullfilled
				send_sms(borrower_text,borrower_farmer.number)
				send_sms(lender_text,lender_farmer.number)
				break
	else:
		print "Incorrect format"

def get_distance(lat1, lng1, lat2, lng2):
	radius_earth = 6371
	adwyze_lat = radians(float(lat1))
	adwyze_long = radians(float(lng1))
	friend_lat = radians(float(lat2))
	friend_long = radians(float(lng2))
	d_lat = friend_lat - adwyze_lat
	d_long = friend_long - adwyze_long
	under_root = sin(d_lat / 2)**2 + cos(adwyze_lat) * \
		cos(friend_lat) * ((sin(d_long) / 2)**2)
	d_sigma = 2 * asin(sqrt(under_root))
	distance = radius_earth * d_sigma
	return distance

def parse(string):
	pattern = ''

def retrieve_messages(message_id):
	ACCOUNT_SID = "SID here" 
	AUTH_TOKEN = "auth token here" 
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
	smss = client.sms.messages.list()
	sender = ''
	for sms in smss:
		if sms.sid == message_id:
			sender =  sms.from_
			body = sms.body
	return sender, body
def register_farmer(request):
	if(request.method == 'POST'):
		farmer = Farmer.objects.create()
		farmer.name = request.POST.get('name')
		farmer.number = request.POST.get('number')
		id = farmer.id
		farmer.save()
		return HttpResponseRedirect('getlocation/'+str(id))
	return render(request, 'register_farmer.html')

def get_location(request, id):
	if(request.method == 'POST'):
		lat = request.POST.get('glat')
		lng = request.POST.get('glng')
		farmer = Farmer.objects.get(id=id)
		farmer.lat = lat
		farmer.lng = lng
		farmer.save()
		return HttpResponseRedirect('/admin')
	return render(request, 'get_location.html',{'id':id})

def enter_location_data(request):
	if(request.method == 'POST'):
		lat = request.POST.get('glat')
		lng = request.POST.get('glng')
		location = Location.objects.create()
		location.lat = lat
		location.lng = lng
		location.save()
		location_id = location.id
		return HttpResponseRedirect('/home/'+str(location_id))
	return render(request, 'get_location2.html',{'id':id})



def stress_location(request,locationid, cropid):
	location = Location.objects.get(id=locationid)
	lat = location.lat
	lng = location.lng
	key = "YOUR KEY HERE"
	url = 'http://api.openweathermap.org/data/2.5/forecast?lat='+lat+'&lon='+lng+'&APPID='+key
	response = urllib2.urlopen(url).read()
	json_response = json.loads(response)
	print json_response
	days_list =  json_response['list']
	crop = Crop.objects.get(id=cropid)
	print crop.maxtemp
	print crop.mintemp
	above_maximum = []
	below_minimum = []
	for day in days_list:
		if (float(day['main']['temp_max']-273.0) > float(crop.maxtemp)):
			tup = (day['dt_txt'], day['main']['temp_max']-273)
			above_maximum.append(tup)
		if float(day['main']['temp_min']-273.0) < float(crop.mintemp):
			tup = (day['dt_txt'], day['main']['temp_min']-273)
			below_minimum.append(tup)
	print above_maximum
	print below_minimum
	return render(request,'stress.html',{'above_maximum':above_maximum,'below_minimum':below_minimum})

def vegetation_outlier(request,id):
	location = Location.objects.get(id=id)
	longitude = location.lng
	latitude = location.lat
	print latitude
	print longitude
	url = "http://vedas.sac.gov.in:8080/LeanGeo/api/band_val/NDVI_PROBA?latitude="+latitude+"&longitude="+longitude
	print url
	response = urllib2.urlopen(url).read()
	json_response = json.loads(response)
	#print json_response
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
			outliers.append(index+1)
	y_plot = [(response['value']) for response in json_response]
	x_plot = [str(response['time']) for response in json_response]
	#print y_plot
	#print x_plot
	x_outlier = [json_response[outlier]['time'] for outlier in outliers]
	y_outlier = [json_response[outlier]['value'] for outlier in outliers]
	list_to_render = []
	print x_outlier
	print y_outlier
	for x,y in zip(x_outlier, y_outlier):
		temp_dict = {}
		temp_dict['name'] = 'cloud'
		temp_dict['xAxis'] = x
		temp_dict['yAxis'] = y
		temp_dict['value'] = 25
		list_to_render.append(temp_dict)
	return render(request, 'vegetation_outlier.html',{'x_plot':x_plot,'y_plot':y_plot,'x_outlier':x_outlier, 'y_outlier':y_outlier,'to_render':list_to_render})

def moisture_outlier(request):
	longitude = "72.14477539062501"
	latitude = "24.279174804687507"
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
	
	y_plot = [str(response['value']) for response in json_response]
	x_plot = [response['time'] for response in json_response]
	print y_plot
	print x_plot
	x_outlier = [json_response[outlier]['time'] for outlier in outliers]
	y_outlier = [json_response[outlier]['value'] for outlier in outliers]
	return render(request, 'moisture_outlier.html',{'x_plot':x_plot,'y_plot':y_plot,'x_outlier':x_outlier, 'y_outlier':y_outlier})



def index(request):
	return render(request, 'base.html')

@csrf_exempt
def curve(request, id): 
	farmer = Location.objects.get(id=id)
	longitude = farmer.lng 
	latitude = farmer.lat
	url = "http://vedas.sac.gov.in:8080/LeanGeo/api/band_val/NDVI_PROBA?latitude="+latitude+"&longitude="+longitude
	r = requests.get(url)
	data =  r.json()
	x = []
	y = []
	num = 0
	for dat in data:
		x.append(dat["time"])
		y.append(dat["value"])
	#x = [index for index in xrange(0,len(data))]
	x = ar(x)
	y = ar(y)
	box = np.ones(3)/3
	js = []
	yhat = np.convolve(y, box, mode='same')
	old_y = list(y)
	new_x = []
	x = list(x)
	for nx in x:
		new_x.append(str(nx))
	new_y = []
	yhat = list(yhat)
	for ny in yhat:
		new_y.append(ny)
	data = {"x": new_x, "y" : new_y, "old_y" : old_y} 
	return JsonResponse(data)

def display_curve(request,id):
	return render(request, 'chart.html',{'id':id})

def find_peak(request,id):
	location = Location.objects.get(id=id)
	longitude = location.lng
	latitude = location.lat
	print latitude
	print longitude
	url = "http://vedas.sac.gov.in:8080/LeanGeo/api/band_val/NDVI_PROBA?latitude="+latitude+"&longitude="+longitude
	response = urllib2.urlopen(url).read()
	json_response = json.loads(response)
	print len(json_response)
	t = np.arange(0,len(json_response))
	y_values = [json_object['value'] for json_object in json_response]
	peaks = find_peaks_cwt(y_values,widths=np.arange(1,50))
	
	plt.plot(t,y_values)
	for peak in peaks:
		plt.plot(t[peak+1],y_values[peak+1],'ro')
	#plt.show()
	plt.savefig('/home/rudresh/Desktop/plot.png')

#######################################################################################
def findDistance(latitudes, longitudes):
	radius = 6371.00
	centralAngle = (haversine(latitudes[1] - latitudes[0]) \
					+ cos(radians(latitudes[1])) * cos(radians(latitudes[0])) * \
					haversine(longitudes[1] - longitudes[0]))
	distance = 2.0 * radius * atan2(sqrt(centralAngle), sqrt(1-centralAngle))
	return distance

def recommend(request,locationid):
	city_details = pandas.read_csv('app/statelocation.csv', encoding='utf-8', delimiter=',')
	location = Location.objects.get(id=locationid)
	city_list = []
	lat = location.lat
	lng = location.lng
	for i in range(len(city_details)):
		city_name = city_details.iloc[i]['city_name']
		city_distance = findDistance([float(lat), city_details.iloc[i]['latitude']], \
			[float(lng), city_details.iloc[i]['longitude']])
		
		city_list.append([city_distance, city_name])
	
	city_list.sort()
	querySet = recommendedCrops.objects.filter(city=city_list[0][1])
	
	if city_list[0][1] == 'AHMADABAD':
		return HttpResponseRedirect("/jamnagar")

	return HttpResponseRedirect("/ahmedabad")

def haversine(angle):
	return pow(sin(radians(angle)/2.0), 2)

def index(request):
	return render(request, 'base.html')

def ahmedabad (request):
	return render(request, 'ahmedabad.html')

def jamnagar (request):
	return render(request, 'jamnagar.html')

def wheat (request):
	return render(request, 'WHEAT.html')

def bajra (request):
	return render(request, 'Bajra.html')

def home(request,id):
	return render(request, 'home.html', {'id':id})

def information(request):
	return render(request, 'information.html')



