from django.contrib import admin
from .models import Tweet, Like, Dislike


# Register your models here.


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'pub_date', 'reply_to']
    list_filter = ['pub_date']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post',)
    list_filter = ('user', 'post',)


@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post',)
    list_filter = ('user', 'post',)
