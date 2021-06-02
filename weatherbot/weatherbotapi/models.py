from django.db import models
from django.utils.timezone import now


class Client(models.Model):
	name = models.CharField(max_length=100)
	userid = models.CharField(max_length=10)
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Weather(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	longitude = models.FloatField()
	latitude = models.FloatField()
	date = models.DateTimeField(default=now, editable=False)

	def __str__(self):
		return self.name


class ClientRequest(models.Model):
	name = models.CharField(max_length=100)
	text = models.CharField(max_length=100)
	longitude = models.FloatField(null=True)
	latitude = models.FloatField(null=True)
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	success = models.BooleanField()
	weather = models.OneToOneField(Weather, null=True, on_delete=models.CASCADE)
	error = models.CharField(max_length=500)
	date = models.DateTimeField(default=now, editable=False)

	def __str__(self):
		return self.name
