from rest_framework import viewsets

from .serializers import FeedSerializer
from .models import Feed

class FeedViewSet(viewsets.ModelViewSet):
    serializer_class = FeedSerializer
    queryset = Feed.objects.all()    
