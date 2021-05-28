from django.views.decorators.common import no_append_slash
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .bot import Bot
from .weather import WeatherApi
from .models import Client, Weather, ClientRequest
from .serializers import ClientSerializer, WeatherSerializer, ClientRequestSerializer


@csrf_exempt
@no_append_slash
@api_view(['POST'])
@parser_classes([JSONParser])
def bot(request, format=None):
	bot = Bot()
	message = request.data['message'];
	chat_id = message['chat']['id']

	try:
		handleMessage(chat_id, message)
	except:
		bot.sendMessage(chat_id, "Sorry, I can't help you")

	return Response("Ok")


def handleMessage(chat_id, message):
	bot = Bot()
	req = ClientRequest()
	weatherApi = WeatherApi()

	isMessage = 'text' in message
	isLocation = 'location' in message

	client = getOrCreateClient(chat_id, message)
	req.name = 'Request from ' + client.name
	req.client = client

	if(isMessage and message['text'] == '/start'):
		return bot.sendMessage(chat_id, "Welcome!\nWhere do you want to know the weather?")

	if(not isMessage and not isLocation):
		return bot.sendMessage(chat_id, "Unsupported message!")

	if(isMessage):
		req.text = message['text']
		resultMessage = weatherApi.getByPlaceName(req.text)
	else:
		req.longitude = message['location']['longitude']
		req.latitude = message['location']['latitude']
		resultMessage = weatherApi.getByCoordinates(req.longitude, req.latitude)

	req.success = weatherApi.success

	if(weatherApi.success):
		req.weather = Weather.objects.create(
			name = weatherApi.placeName,
			description = weatherApi.weather,
			longitude = weatherApi.longitude,
			latitude = weatherApi.latitude
		)
	else:
		req.error = weatherApi.weather

	req.save()
	bot.sendMessage(chat_id, resultMessage)


def getOrCreateClient(userid, message):
	clients = Client.objects.filter(userid = userid)
	if(len(clients) > 0):
		return clients[0]
	else:
		tUser = message['from']
		client = Client()
		client.userid = userid
		client.name = tUser['username']
		if('first_name' in tUser):
			client.firstname = tUser['first_name']
		if('last_name' in tUser):
			client.lastname = tUser['last_name']
		client.save()
		return client



class ClientViewSet(viewsets.ModelViewSet):
	queryset = Client.objects.all().order_by('name')
	serializer_class = ClientSerializer

class WeatherViewSet(viewsets.ModelViewSet):
	queryset = Weather.objects.all().order_by('name')
	serializer_class = WeatherSerializer

class ClientRequestViewSet(viewsets.ModelViewSet):
	queryset = ClientRequest.objects.all().order_by('name')
	serializer_class = ClientRequestSerializer