from __future__ import unicode_literals

from django.db import models

class Farmer(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)
	number = models.CharField(max_length=100, blank=True, null=True)
	lat = models.CharField(max_length=100, blank=True, null=True)
	lng = models.CharField(max_length=100, blank=True, null=True)

class LendTractor(models.Model):
	number = models.CharField(max_length=100, blank=True, null=True)
	date = models.CharField(max_length=100, blank=True, null=True)
	from_time = models.CharField(max_length=100, blank=True, null=True)
	to_time = models.CharField(max_length=100, blank=True, null=True)
	quantity = models.CharField(max_length=100, blank=True, null=True)
	fullfilled = models.CharField(max_length=100, blank=True, null=True)

class BorrowTractor(models.Model):
	number = models.CharField(max_length=100, blank=True, null=True)
	date = models.CharField(max_length=100, blank=True, null=True)
	from_time = models.CharField(max_length=100, blank=True, null=True)
	to_time = models.CharField(max_length=100, blank=True, null=True)
	quantity = models.CharField(max_length=100, blank=True, null=True)
	fullfilled = models.CharField(max_length=100, blank=True, null=True)

class Location(models.Model):
	lat = models.CharField(max_length=100, blank=True, null=True)
	lng = models.CharField(max_length=100, blank=True, null=True)	

class Crop(models.Model):
	mintemp = models.CharField(max_length=100, blank=True, null=True)
	maxtemp = models.CharField(max_length=100, blank=True, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	def __str__(self):
		return self.name

class Truck(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    number_plate = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.CharField(max_length=100, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    currently_occupied_by = models.CharField(max_length=100, blank=True, null=True)
    occupied = models.CharField(max_length=100, blank=True, null=True)

class Order(models.Model):
    farmer1 = models.CharField(max_length=100, blank=True, null=True)
    farmer2 = models.CharField(max_length=100, blank=True, null=True)
    demand_date = models.CharField(max_length=100, blank=True, null=True)
    truck = models.CharField(max_length=100, blank=True, null=True)
class FarmerDemand(models.Model):
    demanding_farmer = models.CharField(max_length=100, blank=True, null=True)
    demand_capacity  = models.CharField(max_length=100, blank=True, null=True)
    demand_date      = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=100, blank=True, null=True)

class recommendedCrops(models.Model):
	name = models.CharField(max_length=18)
	season = models.CharField(max_length=10)
	city = models.CharField(max_length=60)
	state = models.CharField(max_length=30)

	def __str__(self):
		return self.name
