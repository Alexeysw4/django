from django.conf import settings
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.text import slugify


class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='tweets_created',
                             on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, blank=True, db_index=True)
    reply_to = models.ForeignKey("Tweet",
                                 related_name="replies",
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('tweets:detail', args=[self.id, ])


class Like(models.Model):
    post = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = (('post', 'user'),)

    def __str__(self):
        return self.post.text + ': ' + self.user.username


class Dislike(models.Model):
    post = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='dislikes')

    class Meta:
        unique_together = (('post', 'user'),)

    def __str__(self):
        return self.post.text + ': ' + self.user.username

