from rest_framework import viewsets

from .serializers import FeedSerializer, ChannelSerializer
from .models import Feed, Channel


class FeedViewSet(viewsets.ModelViewSet):
    serializer_class = FeedSerializer
    queryset = Feed.objects.all()    


class ChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all() 