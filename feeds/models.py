from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
    #owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=40)
    feed = models.ForeignKey("Feed", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
