from .mapbox import getCoordinates
from .openweather import requestOpenWeather

class WeatherApi:
	def __init__(self, latitude=0, longitude=0):
		self.coordinatesIndivated = True
		self.latitude = latitude
		self.longitude = longitude
		self.placeName = ''
		self.result = ''
		self.success = False

	def get(self):
		if(self.validateCoordinates()):
			response = requestOpenWeather(self.latitude, self.longitude)
			if(self.validateWeather(response)):
				self.writeFormatedText(response)
		return self.result

	def getByCoordinates(self, longitude, latitude):
		self.coordinatesIndivated = True
		self.latitude = latitude
		self.longitude = longitude
		return self.get()

	def getByPlaceName(self, placeName):
		self.coordinatesIndivated, self.longitude, self.latitude = getCoordinates(placeName)
		return self.get()

	def validateCoordinates(self):
		if(not self.coordinatesIndivated):
			self.result = "Error: Coordinates not indicated!"
			self.success = False
			return False
		return True

	def validateWeather(self, data):
		if(data['cod'] != 200):
			self.success = False
			self.result = "Error: Wrong coordinates!"
			return False;
		return True;

	def writeFormatedText(self, data):
		placeName = data['name']
		temp = round(data['main']['temp'] - 273.15)
		description = data['weather'][0]['description']
		self.result = 'Weather in {0}:\n{1}°C & {2}'.format(placeName, temp, description)
		self.success = True
		self.placeName = placeName