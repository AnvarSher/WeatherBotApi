import os, requests

class OpenWeatherApi:
	KEY = os.environ.get("OPENWEATHER_KEY")


	def getWeather(latitude: float, longitude: float):
		try:
			return OpenWeatherApi._requestWeather(latitude, longitude)
		except Exception as ex:
			return (False, {'error': 'OpenWeatherApi Error: ' + str(ex) }) ## TODO: add logging


	def _requestWeather(latitude: float, longitude: float):
		url = OpenWeatherApi._getUrl(latitude, longitude)
		json = requests.get(url).json()
		return OpenWeatherApi._handleResponse(json)


	def _handleResponse(json):
		if(OpenWeatherApi._validateResponse(json)):
			return True, OpenWeatherApi._extractWeather(json)
		else:
			return (False, { 'error': 'OpenWeatherApi Error: Not valid call' })


	## TODO: upgrade validation: add messages
	def _validateResponse(json):
		if(not 'cod' in json):
			return False

		if(json['cod'] != 200):
			return False

		if(not 'name' in json):
			return False

		if(not 'weather' in json):
			return False

		if(len(json['weather']) == 0):
			return False

		if(not 'description' in json['weather'][0]):
			return False

		if(not 'main' in json):
			return False

		if(not 'temp' in json['main']):
			return False

		return True


	def _extractWeather(json):
		return {
			'placeName': json['name'],
			'description': json['weather'][0]['description'],
			'temp': round(json['main']['temp'] - 273.15),
		}


	def _getUrl(latitude: float, longitude: float):
		return 'https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}'.format(latitude, longitude, OpenWeatherApi.KEY)