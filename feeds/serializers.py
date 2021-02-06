from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Feed, Channel


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name')


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    channel_set = ChannelSerializer(many=True)

    class Meta:
        model = Feed
        fields = ('id', 'name', 'channel_set')
