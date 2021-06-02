from rest_framework import serializers

from .models import Client, Weather, ClientRequest


class ClientSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Client
		fields = ('name', 'userid', 'firstname', 'lastname')


class WeatherSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Weather
		exclude = ('date', )


class ClientRequestSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ClientRequest
		exclude = ('date', )
