from weatherbotapi.models import ClientRequest, Weather, Client
from weatherbotapi.services.weatherService import WeatherService
from weatherbotapi.integrations.telegramApi import TelegramApi


class BotMessageService:
	def __init__(self):
		self.user_id = ''
		self.message = {}
		self.is_text = False
		self.is_location = False
		self.welcome_message = "Welcome!\nWhere do you want to know the weather?"
		self.error_message = "Sorry, I can't help you :("

	def handle_message(self, message_data: dict):
		try:
			self._handle_message(message_data)
		except Exception as ex:
			print(ex)

	def _handle_message(self, message_data: dict):
		if not self._validate_message_data(message_data):
			chat_id = self._try_get_chat_id(message_data)
			if chat_id:
				TelegramApi.send_message(chat_id, self.error_message)
			return

		self._extract_message_data(message_data)

		if self.is_text and self.message['text'] == '/start':
			TelegramApi.send_message(self.user_id, self.welcome_message)
			return

		weather_info = self._get_weather_info()

		if weather_info.success:
			TelegramApi.send_message(self.user_id, weather_info.result)
		else:
			TelegramApi.send_message(self.user_id, self.error_message)

	def _get_weather_info(self):
		client = self._get_or_create_client()
		weather_info = self._find_weather_info_by_weather_service()

		if not weather_info.success:
			return weather_info

		weather = self._create_weather(weather_info)
		self._create_client_request(
			client=client,
			success=weather_info.success,
			weather=weather,
			error=weather_info.result
		)
		return weather_info

	def _find_weather_info_by_weather_service(self):
		weather_service = WeatherService()

		if self.is_text:
			text = self.message['text']
			weather_service.find_info_by_place_name(text)
		else:
			longitude = self.message['location']['longitude']
			latitude = self.message['location']['latitude']
			weather_service.find_info_by_coordinates(longitude, latitude)

		return weather_service

	# TODO: upgrade validation: add messages
	def _validate_message_data(self, message_data: dict):
		if 'message' not in message_data:
			return False

		if 'chat' not in message_data['message']:
			return False

		if 'id' not in message_data['message']['chat']:
			return False

		if 'from' not in message_data['message']:
			return False

		if 'username' not in message_data['message']['from']:
			return False

		if 'text' not in message_data['message'] and 'location' not in message_data['message']:
			return False

		if 'text' in message_data['message'] and 'text' not in message_data['message']:
			return False

		if 'location' in message_data['message']:
			if 'location' not in message_data['message']:
				return False

			if 'longitude' not in message_data['message']['location']:
				return False

			if 'latitude' not in message_data['message']['location']:
				return False

		return True

	def _try_get_chat_id(self, message_data: dict):
		try:
			return message_data['message']['chat']['id']
		except KeyError:
			return None

	def _extract_message_data(self, message_data: dict):
		self.message = message_data['message']
		self.user_id = self.message['chat']['id']
		self.is_text = 'text' in self.message
		self.is_location = 'location' in self.message

	def _get_or_create_client(self):
		clients = Client.objects.filter(userid=self.user_id)
		if len(clients) > 0:
			return clients[0]

		t_user = self.message['from']
		client = Client()
		client.userid = self.user_id
		client.name = t_user['username']
		if 'first_name' in t_user:
			client.firstname = t_user['first_name']
		if 'last_name' in t_user:
			client.lastname = t_user['last_name']
		client.save()
		return client

	def _create_weather(self, weather_info):
		return Weather.objects.create(
			name=weather_info.placeName,
			description=weather_info.result,
			longitude=weather_info.longitude,
			latitude=weather_info.latitude
		)

	def _create_client_request(self, client, success, weather, error):
		req = ClientRequest()
		req.name = 'Request from ' + client.name
		req.client = client
		req.success = success

		if self.is_text:
			req.text = self.message['text']
		else:
			req.longitude = self.message['location']['longitude']
			req.latitude = self.message['location']['latitude']

		if success:
			req.weather = weather
		else:
			req.error = error

		req.save()
