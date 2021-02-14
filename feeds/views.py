from rest_framework import viewsets
from rest_framework.response import Response
from googleapiclient.discovery import build
import google_auth_oauthlib.flow
import googleapiclient
import os
import pickle 
from rest_framework_tracking.mixins import LoggingMixin

from .serializers import FeedSerializer, ChannelSerializer
from .models import Feed, Channel


DEVELOPER_KEY = 'AIzaSyDYghYX7EkpFhXEp1nQaYu3ImljdMmoo0w'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
client_secrets_file = "../client_secret_desktop.json"

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def get_authenticated_service():
    if os.path.exists("../credentials_pickle_file"):
        with open("../credentials_pickle_file", "rb") as f:
            credentials = pickle.load(f)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file,
            scopes
        )
        credentials = flow.run_console()
        with open("../credentials_pickle_file", "wb") as f:
            pickle.dump(credentials, f)
    return googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        credentials=credentials
    )


class FeedViewSet(viewsets.ModelViewSet):
    serializer_class = FeedSerializer
    queryset = Feed.objects.all()    


class ChannelViewSet(LoggingMixin, viewsets.ModelViewSet):
    logging_methods = ['POST', 'PUT']
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all() 

    def list(self, request):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        youtube = get_authenticated_service()
        
        request = youtube.subscriptions().list(
            part="snippet,contentDetails",
            mine=True,
            maxResults=50,
        )
        response = request.execute()
        #subscriptions = response["items"]
        snippets = [sub["snippet"] for sub in response["items"]]
        channels = [
            {
                "id": snippet["resourceId"]["channelId"],
                "title": snippet["title"],
                "icon_url": snippet["thumbnails"]["default"]["url"]
            } 
            for snippet in snippets]

        return Response(channels)        
        #return Response(response)        

    def update(self, request, pk=None):
        if not Channel.objects.filter(id=pk).exists():
            Channel.objects.create(
                id=pk, 
                name=request.data["name"], 
                feed=Feed.objects.get(pk=request.data["feed_id"]))
