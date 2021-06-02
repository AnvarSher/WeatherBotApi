from weatherbotapi.integrations.mapboxApi import MapboxApi
from weatherbotapi.integrations.openweatherApi import OpenWeatherApi


class WeatherService:
	def __init__(self, latitude=0, longitude=0):
		self.coordinates_indicated = True
		self.latitude = latitude
		self.longitude = longitude
		self.placeName = ''
		self.result = ''
		self.success = False

	def find_info_by_coordinates(self, longitude, latitude):
		self.coordinates_indicated = True
		self.latitude = latitude
		self.longitude = longitude
		self._find_info()

	def find_info_by_place_name(self, place_name):
		self.coordinates_indicated, data = MapboxApi.get_coordinates(place_name)
		if self.coordinates_indicated:
			self.latitude = data['latitude']
			self.longitude = data['longitude']
			self._find_info()
		else:
			self.result = data['error']

	def _find_info(self):
		if self._check_coordinates_not_indicated():
			return

		self.success, data = OpenWeatherApi.get_weather(self.latitude, self.longitude)
		if self.success:
			self.placeName = data['placeName']
			self.result = self._get_formatted_result(data)
		else:
			self.result = data['error']

	def _check_coordinates_not_indicated(self):
		if not self.coordinates_indicated:
			self.success = False
			self.result = "Error: Coordinates not indicated!"
		return not self.coordinates_indicated

	def _get_formatted_result(self, data):
		return 'Weather in {0}:\n{1}°C & {2}'\
			.format(data['placeName'], data['temp'], data['description'])
