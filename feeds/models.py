from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
    #owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
