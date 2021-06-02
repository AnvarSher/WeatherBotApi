from django.contrib import admin
from .models import Client, Weather, ClientRequest

admin.site.register(Client)
admin.site.register(Weather)
admin.site.register(ClientRequest)
