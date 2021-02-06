from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register(r'feeds', views.FeedViewSet)
router.register(r'channels', views.ChannelViewSet)

urlpatterns = [
    path('', include(router.urls))
]