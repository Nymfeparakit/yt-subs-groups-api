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

    def retrieve(self, request, pk=None):

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        youtube = get_authenticated_service()

        feed = Feed.objects.get(id=pk)
        # get channel ids in this feed
        channel_ids = [
            channel.id for channel in Channel.objects.filter(feed=feed)]
        # get channels by id from yt
        request = youtube.channels().list(
            part="contentDetails",
            id=channel_ids
        )
        response = request.execute()
        channels = response["items"]
        
        # get playlists of latest uploaded videos
        upload_playlist_ids = [
            channel["contentDetails"]["relatedPlaylists"]["uploads"] for channel in channels]

        # get videos from playlist
        videos_request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=upload_playlist_ids[0]
        )
        videos_response = videos_request.execute()
        videos_items = videos_response["items"]
        videos_list = [{
            "id": item["contentDetails"]["videoId"],
            "title": item["snippet"]["title"],
            "video_img_url": item["snippet"]["thumbnails"]["default"]["url"],
            "channel_title": item["snippet"]["videoOwnerChannelTitle"],
            } for item in videos_items]

        return Response(videos_list)


class ChannelViewSet(LoggingMixin, viewsets.ModelViewSet):
    logging_methods = ['POST', 'PUT']
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()

    def list(self, request):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        youtube = get_authenticated_service()

        # get all channels from yt account
        request = youtube.subscriptions().list(
            part="snippet,contentDetails",
            mine=True,
            maxResults=50,
        )
        response = request.execute()

        # get ids of all saved channels
        saved_channels = Channel.objects.all()

        snippets = [sub["snippet"] for sub in response["items"]]

        channels_to_return = {}
        for feed in Feed.objects.all():
            channels_to_return[feed.name] = []
        channels_to_return['_other'] = []  # for channel not inside any group
        for snippet in snippets:
            curr_channel = {
                "id": snippet["resourceId"]["channelId"],
                "title": snippet["title"],
                "icon_url": snippet["thumbnails"]["default"]["url"]
            }
            # is channel saved
            if curr_channel["id"] in [channel.id for channel in saved_channels]:
                channel_feed = Channel.objects.get(
                    id=curr_channel["id"]).feed.name
                channels_to_return[channel_feed].append(curr_channel)
            else:
                channels_to_return["_other"].append(curr_channel)

        return Response(channels_to_return)
        # return Response(response)

    def create(self, request):
        # if channel with id exists, just update it's feed_id field
        # if Channel.objects.filter(id=request.data["id"]).exists():
        # Channel.objects.get(id=request.data["id"]).feed_id = request.data["feed_id"]
        channel = Channel.objects.create(
            id=request.data["id"],
            name=request.data["name"],
            feed_id=request.data["feed_id"],
        )
        return Response({
            'id': request.data["id"],
            'name': request.data["name"],
            'feed_id': request.data["feed_id"],
        })
