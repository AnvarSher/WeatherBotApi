from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'client-requests', views.ClientRequestViewSet)
router.register(r'weather', views.WeatherViewSet)

urlpatterns = [
	path('', include(router.urls)),
	path('bot/', views.bot)
]