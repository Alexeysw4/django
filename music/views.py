from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView

from account.models import Profile
from common.decorators import ajax_required
from music.forms import AlbumForm, SingerForm, SongForm
from music.models import Album, Singer, Song, Genre, TrackUser


class AlbumCreate(CreateView):
    form_class = AlbumForm
    model = Album
    template_name = 'music/album_create.html'

    def get_success_url(self):
        return reverse('dashboard')


class SingerCreate(CreateView):
    form_class = SingerForm
    model = Singer
    template_name = 'music/singer_create.html'

    def get_success_url(self):
        return reverse('dashboard')


class SongCreate(CreateView):
    form_class = SongForm
    model = Song
    template_name = 'music/song_create.html'

    def get_success_url(self):
        return reverse('dashboard')


def song_list(request, genre_slug=None, ):
    genre = None
    genres = Genre.objects.all()
    songs = Song.objects.all()
    search_q = request.GET.get('q')
    if search_q:
        songs = songs.filter(Q(title__icontains=search_q) | Q(singers__name__icontains=search_q)).distinct()
    if genre_slug:
        genre = get_object_or_404(Genre, slug=genre_slug)
        songs = songs.filter(genre=genre)
    return render(request, 'music/song_list.html',
                  {'genre': genre,
                   'genres': genres,
                   'songs': songs,
                   'section': 'songs', })


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'music/album_detail.html'


class SingerDetailView(DetailView):
    model = Singer
    pk_url_kwarg = 'id'
    template_name = 'music/singer_detail.html'


# class AlbumListView(ListView):
#     template_name = 'music/album_list.html'
#     model = Album
#     context_object_name = 'albums'
#
#
# class SingerListView(ListView):
#     template_name = 'music/singer_list.html'
#     model = Singer
#     context_object_name = 'singers'


class SongDetailView(DetailView):
    model = Song
    template_name = 'music/song_detail.html'


@ajax_required
@login_required
@require_POST
def add_song(request):
    song_id = request.POST.get('id')
    action = request.POST.get('action')
    cur_user = request.user
    if song_id and action:
        try:
            song = Song.objects.get(id=song_id)
            if action == 'add':
                TrackUser.objects.get_or_create(user=request.user,
                                                track=song)
                Profile.objects.filter(user=cur_user).update(track_counts=F('track_counts') + 1)

            else:
                TrackUser.objects.filter(user=request.user,
                                         track=song).delete()
                Profile.objects.filter(user=cur_user).update(track_counts=F('track_counts') - 1)
            return JsonResponse({'status': 'ok', })
        except Song.DoesNotExist:
            return JsonResponse({'status': 'ok', })
    return JsonResponse({'status': 'ok'})
