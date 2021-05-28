import os, requests

def getCoordinates(placeName):
	token = os.environ.get("MAPBOX_TOKEN")
	url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/{0}.json?access_token={1}'.format(placeName, token)
	response = requests.get(url)
	json = response.json()
	features = json['features']
	if(len(features) > 0):
		return True, json['features'][0]['center'][0], json['features'][0]['center'][1]
	else:
		return False, 0, 0