import os, requests

def requestOpenWeather(latitude, longitude):
	key = os.environ.get("OPENWEATHER_KEY")
	url = 'https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}'.format(latitude, longitude, key)
	return requests.get(url).json()