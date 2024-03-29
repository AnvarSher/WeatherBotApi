from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
	path('', TemplateView.as_view(template_name='index.html')),
	path('api/', include('weatherbotapi.urls')),
	path('admin/', admin.site.urls),
	path('api-auth/', include('rest_framework.urls'))
]
