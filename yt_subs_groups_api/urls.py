from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('feeds.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
