from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Feed, Channel


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name', 'feed_id')


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    channels = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Feed
        # fields = ('id', 'name', 'channel_set')
        fields = ('id', 'name', 'channels')
