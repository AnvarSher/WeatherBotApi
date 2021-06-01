from django.http import HttpResponseBadRequest, HttpResponse

from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

from .models import Client, Weather, ClientRequest
from .serializers import ClientSerializer, WeatherSerializer, ClientRequestSerializer

from .botMessageService import BotMessageService


@csrf_exempt
@api_view(['POST'])
@parser_classes([JSONParser])
def bot(request, format=None):
	botMessageService = BotMessageService()
	botMessageService.handleMessage(request.data)
	return HttpResponse("Accepted")


class ClientViewSet(viewsets.ModelViewSet):
	queryset = Client.objects.all().order_by('name')
	serializer_class = ClientSerializer


class WeatherViewSet(viewsets.ModelViewSet):
	queryset = Weather.objects.all().order_by('name')
	serializer_class = WeatherSerializer


class ClientRequestViewSet(viewsets.ModelViewSet):
	queryset = ClientRequest.objects.all().order_by('name')
	serializer_class = ClientRequestSerializer