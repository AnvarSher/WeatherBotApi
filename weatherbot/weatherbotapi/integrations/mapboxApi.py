import os
import requests


class MapboxApi:
	TOKEN = os.environ.get("MAPBOX_TOKEN")

	@staticmethod
	def get_coordinates(place_name: str):
		try:
			return MapboxApi._request_coordinates(place_name)
		except Exception as ex:
			# TODO: add logging
			return False, {'error': 'MapboxApi Error: ' + str(ex)}

	@staticmethod
	def _request_coordinates(place_name: str):
		url = MapboxApi._get_url(place_name)
		json = requests.get(url).json()
		return MapboxApi._handle_response(json)

	@staticmethod
	def _handle_response(json):
		if MapboxApi._validate_response(json):
			return True, MapboxApi._extract_coordinates(json)
		else:
			return False, { 'error': 'MapboxApi Error: Not valid call' }

	# TODO: upgrade validation: add messages
	@staticmethod
	def _validate_response(json):
		if 'features' not in json:
			return False

		if len(json['features']) == 0:
			return False

		if 'center' not in json['features'][0]:
			return False

		if len(json['features'][0]['center']) < 2:
			return False

		return True

	@staticmethod
	def _extract_coordinates(json):
		return {
			'longitude': json['features'][0]['center'][0],
			'latitude': json['features'][0]['center'][1]
		}

	@staticmethod
	def _get_url(place_name: str):
		return 'https://api.mapbox.com/geocoding/v5/mapbox.places/{0}.json?access_token={1}'\
			.format(place_name, MapboxApi.TOKEN)
