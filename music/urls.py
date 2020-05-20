from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from music import views

app_name = 'music'

urlpatterns = [
    path('create_album/', login_required(views.AlbumCreate.as_view()), name='album_create'),
    path('create_singer/', login_required(views.SingerCreate.as_view()), name='singer_create'),
    path('create_song/', login_required(views.SongCreate.as_view()), name='song_create'),
    path('add_song/', views.add_song, name='add-song'),
    path('singer/<int:id>/', views.SingerDetailView.as_view(), name='singer_detail'),
    re_path(r'^song/(?P<pk>[0-9]+)/', views.SongDetailView.as_view(), name='song_detail'),
    re_path(r'^album/(?P<pk>[0-9]+)/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('', views.song_list, name='song_list'),
    path('<slug:genre_slug>/', views.song_list, name='song_list_by_genre'),
]
