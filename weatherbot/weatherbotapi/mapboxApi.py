import os, requests

class MapboxApi:
	TOKEN = os.environ.get("MAPBOX_TOKEN")


	def getCoordinates(placeName: str):
		try:
			return MapboxApi._requestCoordinates(placeName)
		except Exception as ex:
			return (False, {'error': 'MapboxApi Error: ' + str(ex) }) ## TODO: add logging


	def _requestCoordinates(placeName: str):
		url = MapboxApi._getUrl(placeName)
		json = requests.get(url).json()
		return MapboxApi._handleResponse(json)


	def _handleResponse(json):
		if(MapboxApi._validateResponse(json)):
			return True, MapboxApi._extractCoordinates(json)
		else:
			return (False, { 'error': 'MapboxApi Error: Not valid call' })


	## TODO: upgrade validation: add messages
	def _validateResponse(json):
		if(not 'features' in json):
			return False

		if(len(json['features']) == 0):
			return False

		if(not 'center' in json['features'][0]):
			return False

		if(len(json['features'][0]['center']) < 2):
			return False

		return True


	def _extractCoordinates(json):
		return {
			'longitude': json['features'][0]['center'][0],
			'latitude': json['features'][0]['center'][1]
		}


	def _getUrl(placeName: str):
		return 'https://api.mapbox.com/geocoding/v5/mapbox.places/{0}.json?access_token={1}'.format(placeName, MapboxApi.TOKEN)