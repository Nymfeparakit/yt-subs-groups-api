from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
    #owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Channel(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default='id')
    name = models.CharField(max_length=40, blank=True, null=True)
    feed = models.ForeignKey("Feed", related_name='channels', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
