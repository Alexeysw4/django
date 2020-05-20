from django import forms

from common.validators import validate_file_extension
from music.models import Album, Singer, Song


class SongForm(forms.ModelForm):
    track = forms.FileField(validators=[validate_file_extension], label='Файл с треком')
    published = forms.DateField(required=False,
                                label='Дата публикации',
                                help_text='В формате YYYY-mm-dd')

    class Meta:
        model = Song
        widgets = {
            'genre': forms.RadioSelect,
        }
        fields = ('title', 'track', 'singers', 'image', 'album', 'published', 'genre', 'clip_link')


class SingerForm(forms.ModelForm):
    class Meta:
        model = Singer
        fields = ('name', 'image',)


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('title', 'image', 'author', 'published')





