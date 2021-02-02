from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Feed


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feed
        fields = ['name']
