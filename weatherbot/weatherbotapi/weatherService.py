from .mapboxApi import MapboxApi
from .openweatherApi import OpenWeatherApi

class WeatherService:
	def __init__(self, latitude=0, longitude=0):
		self.coordinatesIndicated = True
		self.latitude = latitude
		self.longitude = longitude
		self.placeName = ''
		self.result = ''
		self.success = False


	def findInfoByCoordinates(self, longitude, latitude):
		self.coordinatesIndicated = True
		self.latitude = latitude
		self.longitude = longitude
		self._findInfo()


	def findInfoByPlaceName(self, placeName):
		self.coordinatesIndicated, data = MapboxApi.getCoordinates(placeName)
		if(self.coordinatesIndicated):
			self.latitude = data['latitude']
			self.longitude = data['longitude']
			self._findInfo()
		else:
			self.result = data['error']


	def _findInfo(self):
		if(self._checkCoordinatesNotIndicated()):
			return

		self.success, data = OpenWeatherApi.getWeather(self.latitude, self.longitude)

		if(self.success):
			self.placeName = data['placeName']
			self.result = self._getFormatedResult(data)
		else:
			self.result = data['error']


	def _checkCoordinatesNotIndicated(self):
		if(not self.coordinatesIndicated):
			self.success = False
			self.result = "Error: Coordinates not indicated!"
		return not self.coordinatesIndicated


	def _getFormatedResult(self, data):
		return 'Weather in {0}:\n{1}°C & {2}'.format(data['placeName'], data['temp'], data['description'])