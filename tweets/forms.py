from django import forms
from django.utils.text import slugify

from .models import Tweet


class TweetForm(forms.ModelForm):
    text = forms.CharField(required=True,
                           widget=forms.widgets.Textarea())

    class Meta:
        model = Tweet
        exclude = ('user', 'reply_to',)
