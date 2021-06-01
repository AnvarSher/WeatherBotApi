from .models import ClientRequest, Weather, Client
from .weatherService import WeatherService
from .telegramApi import TelegramApi

class BotMessageService:
	def __init__(self):
		self.userId = ''
		self.message = {}
		self.isText = False
		self.isLocation = False
		self.welcomeMessage = "Welcome!\nWhere do you want to know the weather?"
		self.errorMessage = "Sorry, I can't help you :("


	def handleMessage(self, messageData: dict):
		try:
			self._handleMessage(messageData)
		except Exception as ex:
			print(ex)


	def _handleMessage(self, messageData: dict):
		if(not self._validateMessageData(messageData)):
			chatId = self._tryGetChatId(messageData)
			if chatId:
				TelegramApi.sendMessage(chatId, self.errorMessage)
			return

		self._extractMessageData(messageData)

		if(self.isText and self.message['text'] == '/start'):
			TelegramApi.sendMessage(self.userId, self.welcomeMessage)
			return

		weatherInfo = self._getWeatherInfo()
		
		if(weatherInfo.success):
			TelegramApi.sendMessage(self.userId, weatherInfo.result)
		else:
			TelegramApi.sendMessage(self.userId, self.errorMessage)


	def _getWeatherInfo(self):
		client = self._getOrCreateClient()
		weatherInfo = self._findWeatherInfoByWeatherService()

		if(not weatherInfo.success):
			return weatherInfo

		weather = self._createWeather(weatherInfo)
		self._createClientRequest(
			client = client, 
			success = weatherInfo.success, 
			weather = weather, 
			error = weatherInfo.result
		)
		return weatherInfo


	def _findWeatherInfoByWeatherService(self):
		weatherService = WeatherService()
		
		if(self.isText):
			text = self.message['text']
			weatherService.findInfoByPlaceName(text)
		else:
			longitude = self.message['location']['longitude']
			latitude = self.message['location']['latitude']
			weatherService.findInfoByCoordinates(longitude, latitude)

		return weatherService


	## TODO: upgrade validation: add messages
	def _validateMessageData(self, messageData: dict):
		if(not 'message' in messageData):
			return False

		if(not 'chat' in messageData['message']):
			return False

		if(not 'id' in messageData['message']['chat']):
			return False

		if(not 'from' in messageData['message']):
			return False

		if(not 'username' in messageData['message']['from']):
			return False

		if(not 'text' in messageData['message'] and not 'location' in messageData['message']):
			return False

		if('text' in messageData['message'] and not 'text' in messageData['message']):
			return False

		if('location' in messageData['message']): 
			if(not 'location' in messageData['message']):
				return False

			if(not 'longitude' in messageData['message']['location']):
				return False

			if(not 'latitude' in messageData['message']['location']):
				return False

		return True

	def _tryGetChatId(self, messageData: dict):
		try:
			return messageData['message']['chat']['id']
		except:
			return None 


	def _extractMessageData(self, messageData: dict):
		self.message = messageData['message']
		self.userId = self.message['chat']['id']
		self.isText = 'text' in self.message
		self.isLocation = 'location' in self.message


	def _getOrCreateClient(self):
		clients = Client.objects.filter(userid = self.userId)
		if(len(clients) > 0):
			return clients[0]
		
		tUser = self.message['from']
		client = Client()
		client.userid = self.userId
		client.name = tUser['username']
		if('first_name' in tUser):
			client.firstname = tUser['first_name']
		if('last_name' in tUser):
			client.lastname = tUser['last_name']
		client.save()
		return client


	def _createWeather(self, weatherInfo):
		return Weather.objects.create(
			name = weatherInfo.placeName,
			description = weatherInfo.result,
			longitude = weatherInfo.longitude,
			latitude = weatherInfo.latitude
		)


	def _createClientRequest(self, client, success, weather, error):
		req = ClientRequest()
		req.name = 'Request from ' + client.name
		req.client = client
		req.success = success
		
		if(self.isText):
			req.text = self.message['text']
		else:
			req.longitude = self.message['location']['longitude']
			req.latitude = self.message['location']['latitude']

		if(success):
			req.weather = weather
		else:
			req.error = error

		req.save()