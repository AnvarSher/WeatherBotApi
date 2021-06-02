import os
import requests


class OpenWeatherApi:
	KEY = os.environ.get("OPENWEATHER_KEY")

	@staticmethod
	def get_weather(latitude: float, longitude: float):
		try:
			return OpenWeatherApi._request_weather(latitude, longitude)
		except Exception as ex:
			# TODO: add logging
			return False, {'error': 'OpenWeatherApi Error: ' + str(ex) }

	@staticmethod
	def _request_weather(latitude: float, longitude: float):
		url = OpenWeatherApi._get_url(latitude, longitude)
		json = requests.get(url).json()
		return OpenWeatherApi._handle_response(json)

	@staticmethod
	def _handle_response(json):
		if OpenWeatherApi._validate_response(json):
			return True, OpenWeatherApi._extract_weather(json)
		else:
			return False, {'error': 'OpenWeatherApi Error: Not valid call'}

	# TODO: upgrade validation: add messages
	@staticmethod
	def _validate_response(json):
		if 'cod' not in json:
			return False

		if json['cod'] != 200:
			return False

		if 'name' not in json:
			return False

		if 'weather' not in json:
			return False

		if len(json['weather']) == 0:
			return False

		if 'description' not in json['weather'][0]:
			return False

		if 'main' not in json:
			return False

		if 'temp' not in json['main']:
			return False

		return True

	@staticmethod
	def _extract_weather(json):
		return {
			'placeName': json['name'],
			'description': json['weather'][0]['description'],
			'temp': round(json['main']['temp'] - 273.15),
		}

	@staticmethod
	def _get_url(latitude: float, longitude: float):
		return 'https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}'\
			.format(latitude, longitude, OpenWeatherApi.KEY)
