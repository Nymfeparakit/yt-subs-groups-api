# Generated by Django 3.1.6 on 2021-02-06 10:27

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0002_channel'),
    ]

    operations = [
        migrations.AlterField('Channel', 'id', models.CharField(max_length=255))
    ]
