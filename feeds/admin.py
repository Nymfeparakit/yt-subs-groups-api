from django.contrib import admin
from .models import Feed, Channel

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ('name',)

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    pass
